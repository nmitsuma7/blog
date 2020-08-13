from django.test import TestCase
from ..forms import SearchForm, CommentForm


class CommentFormTest(TestCase):
    # Valid Form Data
    def test_commentForm_valid(self):
        form = CommentForm(data={'name': "username", 'comment': "usercomment"})
        self.assertTrue(form.is_valid())

    # Invalid name
    def test_commentForm_name_invalid(self):
        form = CommentForm(data={'name': "", 'comment': "usercomment"})
        self.assertFalse(form.is_valid())

    # Invalid comment
    def test_commentForm_comment_invalid(self):
        form = CommentForm(data={'name': "username", 'comment': ""})
        self.assertFalse(form.is_valid())

    # Invalid both
    def test_commentForm_both_invalid(self):
        form = CommentForm(data={'name': "", 'comment': ""})
        self.assertFalse(form.is_valid())


class SearchFormTest(TestCase):
    # Valid title
    def test_searchForm_valid(self):
        form = SearchForm(data={'title': "title"})
        self.assertTrue(form.is_valid())

    # No title
    def test_searchForm_no_title(self):
        form = SearchForm(data={'title': ""})
        self.assertTrue(form.is_valid())
