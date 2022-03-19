from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from legal_map.profiles.models import Profile
from django.test import TestCase
UserModel=get_user_model()


class ProfileModelTest(TestCase):

    def test_created_properly(self):
        user = UserModel.objects.create(email='testmail@legal.com',password='123passwordtest')
        user.save()
        user.profile.first_name = 'Test first name'
        user.profile.last_name = 'Test last name'
        user.profile.company_name = 'Test company name'
        user.profile.job_title = 'Test job title'
        self.assertIsInstance(user.profile, Profile)
        self.assertEqual(user.profile.first_name, 'Test first name')
        self.assertEqual(user.profile.last_name, 'Test last name')
        self.assertEqual(user.profile.company_name, 'Test company name')
        self.assertEqual(user.profile.job_title, 'Test job title')

    def test_when_name_starts_with_small_letter_expectedToRaise(self):
        user = UserModel.objects.create(email='testmail@legal.com', password='123passwordtest')
        user.save()
        user.profile.first_name = 'test error name'
        user.profile.last_name = 'Test last name'
        user.profile.company_name = 'Test company name'
        user.profile.job_title = 'Test job title'
        with self.assertRaises(ValidationError) as ex:
            user.profile.full_clean()
        expected = 'The name must start with an uppercase letter'
        actual = ', '.join(ex.exception.message_dict['first_name'])
        self.assertEqual(expected, str(actual))

    def test_job_title_max_length(self):
        user = UserModel.objects.create(email='testmail@legal.com', password='123passwordtest')
        user.save()
        user.profile.job_title = 'Test job title'
        max_length = user.profile._meta.get_field('job_title').max_length
        self.assertEqual(max_length, 40)

