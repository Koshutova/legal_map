
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from legal_map.legal_help.validators import validate_name

UserModel = get_user_model()


class MainArea(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='areas', blank=True)

    def __str__(self):
        return str(self.name)


class Company(models.Model):
    company_name = models.CharField(
        max_length=50,
        validators=
        [MinLengthValidator(3),
         validate_name,
         ])
    picture = models.ImageField(upload_to='legal', blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20)
    expertise = models.TextField(blank=True)
    website = models.URLField(blank=True)
    areas = models.ManyToManyField(MainArea, blank=True)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    @property
    def image_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url
        else:
            return "/static/images/logo.jpeg"

    def __str__(self):
        return str(self.company_name)


