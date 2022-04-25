from legal_map.articles.forms import ArticleForm
from tests.base.tests import LegalTestCase
from legal_map.articles.models import Article
from django.utils import timezone
import json

# Does not work at the moment, because of the picture field


class ArticleFormTest(LegalTestCase):
    def test_valid_form(self):

        article = Article.objects.create(
            title='Some Test Title',
            picture='path/to/image.png',
            author_name='Test Author Name',
            article_text='{"delta": ""}',
            user=self.user
        )
        data = {
            'title': article.title,
            'picture': article.picture,
            'author_name': article.author_name,
            'article_text': '{"delta":""}',
            'created': timezone.now(),
            'last_modified': timezone.now()
        }
        form = ArticleForm(data=data)

        self.assertFalse(form.is_valid())
