from legal_map.legal_help.forms import CompanyForm
from legal_map.legal_help.models import MainArea, Company
from tests.base.tests import LegalTestCase


class CompanyFormTest(LegalTestCase):
    def test_valid_form(self):
        area = MainArea.objects.create(
            name='Test Legal Name',
            image='path/to/image.png',
        )
        company = Company.objects.create(
            company_name='Test Company Name',
            phone_number='123456',
            user=self.user,
        )

        company.areas.set([area,])
        data = {
            'company_name': company.company_name,
            'phone_number': company.phone_number,
            'area': company.areas,
        }
        form = CompanyForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        area = MainArea.objects.create(
            name='Test Legal Name',
            image='path/to/image.png',
        )
        company = Company.objects.create(
            company_name='Test Company Name',
            phone_number='',
            user=self.user,
        )

        company.areas.set([area, ])
        data = {
            'company_name': company.company_name,
            'phone_number': company.phone_number,
            'area': company.areas,
        }
        form = CompanyForm(data=data)
        self.assertFalse(form.is_valid())