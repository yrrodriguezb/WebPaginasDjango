from django.contrib.auth.models import User
from django.test import TestCase
from .models import Profile


class ProfileTestCase(TestCase):
    
    def setUp(self):
        User.objects.create_user('test', 'test@gmail.com', 'test1234')

    def test_profile_exists(self):
        exists = Profile.objects.filter(user__username='test').exists()
        self.assertEqual(exists, True)

