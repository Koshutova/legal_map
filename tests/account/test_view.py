from django.urls import reverse

from tests.base.tests import LegalTestCase


class UserTest(LegalTestCase):

    def test_signin(self):
        response = self.client.post(reverse('signin'), {'email': 'test@test.com', 'password': '789test789!'})
        self.assertTemplateUsed(response, 'auth/signin.html')
        self.assertEqual(200, response.status_code)

    def test_signup(self):
        response = self.client.post(reverse('sign up'), {'email': 'test@test.com', 'password': '789test789!'})
        self.assertTemplateUsed(response, 'auth/sign-up.html')
        self.assertEqual(200, response.status_code)

    def test_signout(self):
        response = self.client.post(reverse('sign up'), {'email': 'test@test.com', 'password': '789test789!'})
        self.assertEqual(200, response.status_code)
