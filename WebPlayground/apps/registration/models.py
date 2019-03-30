from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True, verbose_name='Imagen')
    biography = models.TextField(null=True, blank=True, verbose_name='Biografia')
    link = models.URLField(max_length=200, null=True, blank=True, verbose_name='URL')

    class Meta:
        ordering = ['user__username',]


""" Señal que se encarga de crearun perfil cuando se cree un usuario """
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    # Valida que tenga el atributo created para indicar que se ha crado por primera vez.
    # Sino existe devolvemos false cpor defecto
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        #print('Se acaba de crear un usuario con su perfil enlazado')

""" @receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save() """

