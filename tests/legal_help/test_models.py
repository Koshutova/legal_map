from django.core.exceptions import ValidationError

from legal_map.legal_help.models import MainArea, Company
from tests.base.tests import LegalTestCase


class MainAreaModelTest(LegalTestCase):
    def test_created_properly(self):
        main_area = MainArea.objects.create(
            name='Test Legal Name',
            image='path/to/image.png',
        )
        self.assertEqual(main_area.name, 'Test Legal Name')
        self.assertTrue(isinstance(main_area, MainArea))

    def test_model_str(self):
        main_area = MainArea.objects.create(
            name='Test Legal Name',
            image='path/to/image.png',
        )
        self.assertEqual(str(main_area), 'Test Legal Name')


class CompanyModelTest(LegalTestCase):
    def test_created_properly(self):
        area1 = MainArea.objects.create(
            name='Test Legal Name',
            image='path/to/image.png',
        )
        area2 = MainArea.objects.create(
            name='Test Legal Name 2',
            image='path/to/image.png',
        )
        company = Company.objects.create(
            company_name='Test Company Name',
            phone_number='123456',
            user=self.user,
        )
        company.areas.set([area1.pk, area2.pk])
        self.assertEqual(company.areas.count(), 2)

    def test_when_name_starts_with_small_letter_expectedToRaise(self):
        company = Company.objects.create(
            company_name='test Company Name',
            phone_number='123456',
            user=self.user,
        )

        with self.assertRaises(ValidationError) as ex:
            company.full_clean()
        expected = 'The name must start with an uppercase letter'
        actual = ', '.join(ex.exception.message_dict['company_name'])
        self.assertEqual(expected, str(actual))

    def test_company_name_max_length(self):
        company = Company.objects.create(
            company_name='Test Company Name',
            phone_number='123456',
            user=self.user,
        )
        max_length = company._meta.get_field('company_name').max_length
        self.assertEqual(max_length, 50)


