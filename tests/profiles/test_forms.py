from django.contrib.auth import get_user_model

from legal_map.profiles.forms import ProfileForm
from legal_map.profiles.models import Profile
from django.test import TestCase

UserModel=get_user_model()


class ProfileFormTest(TestCase):
    def test_valid_form(self):
        user = UserModel.objects.create(email='testmail@legal.com', password='123passwordtest')
        user.save()
        user.profile.first_name = 'Test first name'
        user.profile.last_name = 'Test last name'
        data = {
            'first_name': user.profile.first_name,
            'last_name': user.profile.last_name,
        }
        form = ProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        user = UserModel.objects.create(email='testmail@legal.com', password='123passwordtest')
        user.save()
        user.profile.first_name = 'test first name'
        user.profile.last_name = 'Test last name'
        data = {
            'first_name': user.profile.first_name,
            'last_name': user.profile.last_name,
        }
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())


