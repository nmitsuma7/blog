import datetime
import urllib

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from ..models import Post, Comment, Category, Image


def create_post(author, category, title, days, live):
    return Post.objects.create(
        author=User.objects.create_user(author),
        title=title,
        sub_title="subtitle",
        text="text",
        image=create_image(text='image'),
        category=category,
        created_date=timezone.now(),
        published_date=timezone.now() + datetime.timedelta(days=days),
        live=live
    )


def create_image(text):
    return Image.objects.create(text=text)


def create_category(name):
    return Category.objects.create(name=name)


def create_comment(post, name, comment):
    return Comment.objects.create(post=post, name=name, comment=comment)


class IndexViewTest(TestCase):
    # valid posts data
    def test_valid_post(self):
        create_post(author='testuser', category=create_category(
            'category'), title="Valid post", days=0, live=True)
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Valid post")
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: Valid post>']
        )

    # 2 valid posts data
    def test_two_valid_post(self):
        create_post(author='testuser1', category=create_category('category'),
                    title="Valid post 1", days=-10, live=True)
        create_post(author='testuser2', category=create_category('category'),
                    title="Valid post 2", days=0, live=True)
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser1")
        self.assertContains(response, "testuser2")
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: Valid post 2>', '<Post: Valid post 1>']
        )

    # No posts exist
    def test_no_post(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], [])

    # Posts with a publish_date in the future
    def test_future_post(self):
        create_post(author='testuser', category=create_category('category'),
                    title="Future post", days=30, live=True)
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], [])

    # Posts with not live
    def test_not_live_post(self):
        create_post(author='testuser', category=create_category('category'),
                    title="Not live post", days=0, live=False)
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], [])

    # 1 search result
    def test_search_result(self):
        create_post(author='testuser1', category=create_category('category'),
                    title="Search post", days=0, live=True)
        create_post(author='testuser2', category=create_category('category'),
                    title="Notget post", days=0, live=True)
        response = self.client.get(
            "".join([reverse('blog:index'), '?',
                     urllib.parse.urlencode(dict(title='Search'))])
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: Search post>']
        )
        self.assertEqual(response.context['title'], "Search")
        self.assertEqual(response.context['count'], 1)

    # 2 search result
    def test_two_search_result(self):
        create_post(author='testuser1', category=create_category('category'),
                    title="Search post 1", days=0, live=True)
        create_post(author='testuser2', category=create_category('category'),
                    title="Search post 2", days=0, live=True)
        response = self.client.get(
            "".join([reverse('blog:index'), '?',
                     urllib.parse.urlencode(dict(title='Search'))])
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: Search post 2>', '<Post: Search post 1>']
        )
        self.assertEqual(response.context['title'], "Search")
        self.assertEqual(response.context['count'], 2)

    # No search result
    def test_no_search_result(self):
        create_post(author='testuser', category=create_category('category'),
                    title="Notget post", days=0, live=True)
        response = self.client.get(
            "".join([reverse('blog:index'), '?',
                     urllib.parse.urlencode(dict(title='Search'))])
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], [])
        self.assertEqual(response.context['title'], "Search")
        self.assertEqual(response.context['count'], 0)


class CategoryViewTest(TestCase):
    # valid category data
    def test_valid_post(self):
        create_post(author='testuser', category=create_category(
            'category'), title="Valid post", days=0, live=True)
        create_post(author='testuser2', category=create_category(
            'category2'), title="Valid post", days=0, live=True)
        response = self.client.get(
            reverse('blog:category', kwargs=dict(category='category')))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "category")
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: Valid post>']
        )
        self.assertEqual(response.context['category'], "category")

    # 2 valid posts data
    def test_two_valid_post(self):
        create_post(author='testuser', category=create_category(
            'category'), title="Valid post 1", days=0, live=True)
        create_post(author='testuser2', category=create_category(
            'category'), title="Valid post 2", days=0, live=True)
        response = self.client.get(
            reverse('blog:category', kwargs=dict(category='category')))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "category")
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: Valid post 2>', '<Post: Valid post 1>']
        )
        self.assertEqual(response.context['category'], "category")

    # No posts exist
    def test_no_post(self):
        create_post(author='testuser', category=create_category(
            'category'), title="Valid post 1", days=0, live=True)
        response = self.client.get(
            reverse('blog:category', kwargs=dict(category='different')))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['posts'],
            []
        )
        self.assertEqual(response.context['category'], "different")

    # Posts with a publish_date in the future
    def test_future_post(self):
        create_post(author='testuser', category=create_category(
            'category'), title="Valid post", days=30, live=True)
        response = self.client.get(
            reverse('blog:category', kwargs=dict(category='category')))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['posts'],
            []
        )
        self.assertEqual(response.context['category'], "category")

    # Posts with not live
    def test_not_live_post(self):
        create_post(author='testuser', category=create_category(
            'category'), title="Valid post", days=0, live=False)
        response = self.client.get(
            reverse('blog:category', kwargs=dict(category='category')))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['posts'],
            []
        )
        self.assertEqual(response.context['category'], "category")


class ArticleViewTest(TestCase):
    # valid posts data
    def test_valid_post(self):
        post = create_post(author='testuser', category=create_category(
            'category'), title="Valid post", days=0, live=True)
        response = self.client.get(reverse('blog:article', args=(post.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)

    # No posts exist
    def test_not_exist_post(self):
        response = self.client.get(reverse('blog:article', args=('9')))
        self.assertEqual(response.status_code, 404)

    # Posts with a publish_date in the future
    def test_future_post(self):
        post = create_post(author='testuser', category=create_category(
            'category'), title="Valid post", days=30, live=True)
        response = self.client.get(reverse('blog:article', args=(post.id,)))
        self.assertEqual(response.status_code, 404)

    # Posts with not live
    def test_not_live_post(self):
        post = create_post(author='testuser', category=create_category(
            'category'), title="Valid post", days=0, live=False)
        response = self.client.get(reverse('blog:article', args=(post.id,)))
        self.assertEqual(response.status_code, 404)

    # valid comment post
    def test_valid_comment_post(self):
        post = create_post(author='testuser', category=create_category(
            'category'), title="Valid post", days=0, live=True)
        comment = create_comment(post=post, name='name', comment='comment')
        response = self.client.get(reverse('blog:article', args=(post.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['comments'],
            ['<Comment: name>']
        )

    # 2 valid comments post
    def test_two_valid_comment_post(self):
        post = create_post(author='testuser', category=create_category(
            'category'), title="Valid post", days=0, live=True)
        create_comment(post=post, name='name1', comment='comment')
        create_comment(post=post, name='name2', comment='comment')
        response = self.client.get(reverse('blog:article', args=(post.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['comments'],
            ['<Comment: name2>', '<Comment: name1>']
        )

    # create comment
    def test_create_comment(self):
        post = create_post(author='testuser', category=create_category(
            'category'), title="Valid post", days=0, live=True)

        response = self.client.post(reverse('blog:article', args=(post.id,)), {
            'post': post,
            'name': 'name',
            'comment': 'comment'
        })
        self.assertEqual(response.status_code, 302)
