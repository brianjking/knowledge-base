from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Category
from .models import Article


class CategoryTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Category',
            slug='category',
        )


class ArticleTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Category',
            slug='category',
        )

        self.article_1 = Article.objects.create(
            category=self.category,
            name='Active and public article',
            slug='active-and-public',
            is_active=True,
            is_private=False,
            content='Article one content'
        )

        self.article_2 = Article.objects.create(
            category=self.category,
            name='Active and private article',
            slug='active-and-private',
            is_active=True,
            is_private=True,
            content='Article two content'
        )

        self.article_3 = Article.objects.create(
            category=self.category,
            name='Non active article',
            slug='non-active-article',
            is_active=False,
            is_private=False,
            content='Article three content'
        )

        def test_public_article_view(self):
            response = self.client.get(reverse(
                'article_detail',
                args=[self.article_1.slug]
            ))
            self.assertEqual(response.status_code, 200)

        def test_unlogin_private_article_view(self):
            response = self.client.get(reverse(
                'article_detail',
                args=[self.article_2.slug]
            ))
            self.assertEqual(response.status_code, 400)

        def test_login_private_article_view(self):
            self.client.login(username='admin', password='demo')
            response = self.client.get(reverse(
                'article_detail',
                args=[self.article_2.slug]
            ))
            self.assertEqual(response.status_code, 200)

        def test_inactive_article(self):
            response = self.client.get(reverse(
                'article_detail',
                args=[self.article_3.slug]
            ))
            self.assertEqual(response.status_code, 400)