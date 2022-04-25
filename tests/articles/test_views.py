from django.urls import reverse
from legal_map.articles.models import Article
from tests.base.mixins import LegalTestUtils
from tests.base.tests import LegalTestCase


class ArticlesTest(LegalTestUtils, LegalTestCase):

    def test_indexTemplateUsed(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_listAllArticles_count_withSameUser(self):
        article1 = Article.objects.create(
            title='First Test Title',
            picture='path/to/image.png',
            author_name='Test First Author',
            article_text='{"delta": ""}',
            user=self.user
        )
        article2 = Article.objects.create(
            title='Second Test Title',
            picture='path/to/image.png',
            author_name='Test Author Name',
            article_text='{"delta": ""}',
            user=self.user
        )
        self.client.force_login(self.user)
        self.assertEqual(Article.objects.all().count(), 2)

    def test_listAllArticles_count_withDifferentUser(self):
        article1 = Article.objects.create(
            title='First Test Title',
            picture='path/to/image.png',
            author_name='Test First Author',
            article_text='{"delta": ""}',
            user=self.user
        )
        article2_user = self.create_user(email='article@test.mail', password='1289testart')
        article2 = Article.objects.create(
            title='Second Test Title',
            picture='path/to/image.png',
            author_name='Test Author Name',
            article_text='{"delta": ""}',
            user=article2_user
        )
        self.client.force_login(self.user)
        self.assertEqual(Article.objects.all().count(), 2)

    def test_createArticle_whenUserIsAuthor_expectSuccess(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('article create'),{
            'title': 'Some Test Title',
            'picture': 'path/to/image.png',
            'author_name': 'Test Author Name',
            'article_text':'{"delta": ""}',
            'user': self.user
        })
        self.assertEqual(response.status_code, 200)

    def test_articleDetail_whenUserIsOwner(self):
        self.client.force_login(self.user)
        article = Article.objects.create(
            title='First Test Title',
            picture='path/to/image.png',
            author_name='Test First Author',
            article_text='{"delta": ""}',
            user=self.user
        )
        response = self.client.get(reverse('article details', kwargs={'pk':article.id}))
        self.assertTrue(response.context['is_creator'])

    def test_articleDetail_whenUserIsNotOwner(self):
        article_user = self.create_user(email='test123@article.details', password='1973passtest')
        article_user.groups.add(self.group)
        article_user.save()
        self.client.force_login(self.user)
        article = Article.objects.create(
            title='First Test Title',
            picture='path/to/image.png',
            author_name='Test First Author',
            article_text='{"delta": ""}',
            user=article_user
        )
        response = self.client.get(reverse('article details', kwargs={'pk':article.id}))
        self.assertFalse(response.context['is_creator'])

    def test_statusCodeEdit_whenSignedInUserAndUserIsOwner(self):
        self.client.force_login(self.user)
        article = Article.objects.create(
            title='First Test Title',
            picture='path/to/image.png',
            author_name='Test First Author',
            article_text='{"delta": ""}',
            user=self.user
        )
        response = self.client.get(reverse('article details', kwargs={'pk': article.id}))
        self.assertEqual(article.user, self.user)
        self.assertEqual(response.status_code, 200)

    def test_deleteArticle(self):
        self.client.force_login(self.user)
        article = Article.objects.create(
            title='First Test Title',
            picture='path/to/image.png',
            author_name='Test First Author',
            article_text='{"delta": ""}',
            user=self.user
        )
        get_response = self.client.get(reverse('article delete', kwargs={'pk': article.id}), follow=True)
        self.assertContains(get_response, 'Are you sure you want to delete')

        post_response = self.client.post(reverse('article delete', kwargs={'pk': article.id}), follow=True)
        self.assertRedirects(post_response, reverse('list all articles'), status_code=302)

    def test_listMyArticles_withDifferentAuthors_expectFilterMine(self):
        article1 = Article.objects.create(
            title='First Test Title',
            picture='path/to/image.png',
            author_name='Test First Author',
            article_text='{"delta": ""}',
            user=self.user
        )
        article2_user = self.create_user(email='article@test.mail', password='1289testart')
        article2 = Article.objects.create(
            title='Second Test Title',
            picture='path/to/image.png',
            author_name='Test Author Name',
            article_text='{"delta": ""}',
            user=article2_user
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse('list my articles'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(article1.user, self.user)
        self.assertEqual(article2.user, article2_user)

        article_exists = Article.objects.filter(user_id=self.user.id).exists()
        self.assertTrue(article_exists)
        self.assertEqual(Article.objects.filter(user_id=self.user.id).count(), 1)
        self.assertEqual(Article.objects.all().count(), 2)











