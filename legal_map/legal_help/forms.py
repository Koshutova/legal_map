from django import forms

from legal_map.legal_help.models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('user',)
        widgets = {
            'areas': forms.CheckboxSelectMultiple(),
        }


