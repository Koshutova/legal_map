from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import Group

from legal_map.profiles.forms import ProfileForm
from legal_map.profiles.models import Profile
from django.test import TestCase

UserModel = get_user_model()


class ProfileDetailsTest(TestCase):
    def test_profileDetails(self):
        user = UserModel.objects.create(email='testmail@legal.com', password='123passwordtest')
        group_name = 'Author'
        self.group = Group(name=group_name)
        self.group.save()
        user.groups.add(self.group)
        user.save()
        self.client.force_login(user)
        response = self.client.get(reverse('profile details'))
        self.assertEqual(response.context['profile'].user.id, user.id)
