from django.contrib.auth.models import User
from rest_framework import serializers
from apps.registration.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfilesSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = ('user', 'avatar', 'biography', 'link')
   
    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.avatar.url
        return request.build_absolute_uri(image_url)

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile, created = Profile.objects.update_or_create(
                                user=user,
                                avatar=validated_data.pop('avatar'),
                                biography=validated_data.pop('biography'),
                                link=validated_data.pop('link') 
                            )
        return profile

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.biography = validated_data.get('biography', instance.biography)
        instance.link = validated_data.get('link', instance.link)
        instance.save()
        return instance