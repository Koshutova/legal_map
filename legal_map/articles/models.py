from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

UserModel = get_user_model()


class Article(models.Model):
    title = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(10),
        ]
    )
    picture = models.ImageField(upload_to='articles')
    author_name = models.CharField(max_length=20, blank=True)
    article_text = models.TextField(validators=[
            MinLengthValidator(20),
        ])
    created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


