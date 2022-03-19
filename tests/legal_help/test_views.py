from django.contrib.auth.models import Group
from django.urls import reverse

from legal_map.legal_help.models import MainArea, Company
from tests.base.mixins import LegalTestUtils
from tests.base.tests import LegalTestCase


class LegalHelpViewsTest(LegalTestUtils, LegalTestCase):
    def test_legalIndexView_whenNoUserSignedIn_expectSuccess(self):
        area1 = MainArea.objects.create(
            name='Test Name One',
            image='path/to/image.png',
        )
        area2 = MainArea.objects.create(
            name='Test Name Two',
            image='path/to/image.png',
        )
        response = self.client.get(reverse('legal index'))
        self.assertEqual(MainArea.objects.all().count(), 2)
        self.assertEqual(list(response.context['main_areas']), [area1, area2])

    def test_legalIndexView_whenUserIsSignedIn_expectSuccess(self):
        area1 = MainArea.objects.create(
            name='Test Name One',
            image='path/to/image.png',
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse('legal index'))
        self.assertEqual(list(response.context['main_areas']), [area1,])

    def test_findCompanyArea_whenCompanyExists_expectSuccess(self):
        area1 = MainArea.objects.create(
            name='Test Name One',
            image='path/to/image.png',
        )
        company = Company.objects.create(
            company_name='Test Company Name',
            phone_number='123456',
            user=self.user,
        )
        company.areas.set([area1.pk,])
        self.client.force_login(self.user)
        response = self.client.post(reverse('find companies', kwargs={'pk': area1.id}))
        self.assertEqual(response.status_code, 200)

        company_exists = Company.objects.filter(areas=area1.id).exists()
        self.assertTrue(company_exists)

    def test_findCompany_whenSuchCompanyDoesNotExists(self):
        area1 = MainArea.objects.create(
            name='Test Name One',
            image='path/to/image.png',
        )
        company = Company.objects.create(
            company_name='Test Company Name',
            phone_number='123456',
            user=self.user,
        )
        self.client.force_login(self.user)
        company_exists = Company.objects.filter(areas=area1.id).exists()
        self.assertFalse(company_exists)

        response = self.client.get(reverse('find companies', kwargs={'pk': area1.id}))
        self.assertFalse(response.context['have_companies'])

    def test_listMyCompanies_withDifferentUsers_expectFilterMine(self):
        company = Company.objects.create(
            company_name='Test Company Name',
            phone_number='123456',
            user=self.user,
        )
        company_user = self.create_user(email='company@test.mail', password='1289testcomp')
        company_2 = Company.objects.create(
            company_name='Test Company Name',
            phone_number='123456',
            user=company_user,
        )
        self.client.force_login(self.user)
        company_exists = Company.objects.filter(user_id=self.user.id).exists()
        self.assertTrue(company_exists)
        response = self.client.get(reverse('list my companies'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['has_company'])
        self.assertEqual(company.user, self.user)
        self.assertEqual(Company.objects.filter(user_id=self.user.id).count(), 1)
        self.assertEqual(Company.objects.all().count(), 2)
        self.assertEqual(company_2.user, company_user)

    def test_createCompany_withArticle(self):
        self.client.force_login(self.user)
        area1 = MainArea.objects.create(
            name='Test Name One',
            image='path/to/image.png',
        )
        response = self.client.post(reverse('company create'),{
            'company_name': 'Test Company Name',
            'phone_number': '123456',
            'areas': area1,
            'user': self.user,
        })
        self.assertEqual(response.status_code, 200)

    def test_companyDetail_whenUserIsOwner(self):
        self.client.force_login(self.user)
        company = Company.objects.create(
            company_name='Test Company Name',
            phone_number='123456',
            user=self.user,
        )
        response = self.client.get(reverse('company details', kwargs={'pk':company.id}))
        self.assertTrue(response.context['is_creator'])

    def test_companyDetail_whenUserIsNotOwner(self):
        company_user = self.create_user(email='test123@company.details', password='1973passtest')
        company_user.groups.add(self.group)
        company_user.save()
        self.client.force_login(self.user)
        company = Company.objects.create(
            company_name='Test Company Name',
            phone_number='123456',
            user=company_user
        )
        response = self.client.get(reverse('company details', kwargs={'pk':company.id}))
        self.assertFalse(response.context['is_creator'])

    def test_deleteCompany(self):
        self.client.force_login(self.user)
        company = Company.objects.create(
            company_name='Test Company Name',
            phone_number='123456',
            user=self.user,
        )
        get_response = self.client.get(reverse('company delete', kwargs={'pk': company.id}), follow=True)
        self.assertContains(get_response, 'Are you sure you want to delete')

        post_response = self.client.post(reverse('company delete', kwargs={'pk': company.id}), follow=True)
        self.assertRedirects(post_response, reverse('list my companies'), status_code=302)
