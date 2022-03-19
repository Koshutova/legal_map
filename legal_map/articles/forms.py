from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from legal_map.articles.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('user', )


class ContactUsForm(forms.Form):
    from_email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        required=True)
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject'}),
        required=True)
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Message'}),
        required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
