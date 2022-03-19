from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase,Client

UserModel = get_user_model()


class LegalTestCase(TestCase):
    logged_in_email = 'legal@maptest.bg'
    logged_in_password = '78945zxc'

    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_user(
            email=self.logged_in_email,
            password=self.logged_in_password,
        )
        group_name = 'Author'
        self.group = Group(name=group_name)
        self.group.save()
        self.user.groups.add(self.group)
        self.user.save()
