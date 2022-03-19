from django.core.exceptions import ValidationError


def validate_name(value):
    if value[0] != value[0].upper():
        raise ValidationError('The name must start with an uppercase letter')