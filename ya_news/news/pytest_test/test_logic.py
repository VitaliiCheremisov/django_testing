from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


def test_anonymous_user_cant_create_comment(client, form_data, news, comment):
    url = reverse('news:detail', args=(news.id,))
    comment_before_count = Comment.objects.count()
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    comment_after_count = Comment.objects.count()
    assert comment_before_count == comment_after_count


@pytest.mark.parametrize(
    'parametrized_client',
    (
        (pytest.lazy_fixture('author_client'),)
    )
)
def test_user_can_create_comment(parametrized_client, news, form_data, author):
    detail_url = reverse('news:detail', args=(news.id,))
    comment_url = detail_url + '#comments'
    response = parametrized_client.post(comment_url, data=form_data)
    assertRedirects(response, f'{detail_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == 'Новый текст'
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize(
    'parametrized_client',
    (
        (pytest.lazy_fixture('author_client'),)
    )
)
def test_user_cant_use_bad_words(parametrized_client, news, author):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    detail_url = reverse('news:detail', args=(news.id,))
    comment_url = detail_url + '#comments'
    response = parametrized_client.post(comment_url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.parametrize(
    'parametrized_client',
    (
        (pytest.lazy_fixture('author_client'),)
    )
)
def test_author_can_delete_comment(parametrized_client, comment, news):
    detail_url = reverse('news:detail', args=(news.id,))
    comment_url = detail_url + '#comments'
    delete_url = reverse('news:delete', args=(comment.id,))
    response = parametrized_client.delete(delete_url)
    assertRedirects(response, comment_url)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(admin_client, comment):
    delete_url = reverse('news:delete', args=(comment.id,))
    response = admin_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


@pytest.mark.parametrize(
    'parametrized_client',
    (
        (pytest.lazy_fixture('author_client'),)
    )
)
def test_author_can_edit_comment(parametrized_client, news, form_data, comment):
    detail_url = reverse('news:detail', args=(news.id,))
    comment_url = detail_url + '#comments'
    edit_url = reverse('news:edit', args=(comment.id,))
    response = parametrized_client.post(edit_url, data=form_data)
    assertRedirects(response, comment_url)
    comment.refresh_from_db()
    assert comment.text == 'Новый текст'


def test_user_cant_edit_comment_of_another_user(admin_client, comment, form_data):
    edit_url = reverse('news:edit', args=(comment.id,))
    response = admin_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == 'Текст комментария'
