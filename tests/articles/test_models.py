from legal_map.articles.models import Article
from tests.base.tests import LegalTestCase


class ArticleModelTest(LegalTestCase):

    def test_created_properly(self):
        article = Article.objects.create(
            title='Some Test Title',
            picture='path/to/image.png',
            author_name='Test Author Name',
            article_text='{"delta": ""}',
            user=self.user
        )
        self.assertEqual(article.title,'Some Test Title')
        self.assertEqual(article.picture, 'path/to/image.png')
        self.assertEqual(article.author_name, 'Test Author Name')
        self.assertTrue(isinstance(article, Article))