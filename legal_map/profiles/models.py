from django.contrib.auth import get_user_model
from django.db import models

from ..legal_help.validators import validate_name

UserModel = get_user_model()


class Profile(models.Model):
    first_name = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            validate_name,
        ]
    )
    last_name = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            validate_name,
        ]
    )
    job_title = models.CharField(
        max_length=40,
        blank=True,
    )
    company_name = models.CharField(
        max_length=40,
        blank=True,
        validators=[
            validate_name,
        ]
    )
    is_complete = models.BooleanField(
        default=False,
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )


from .signals import *