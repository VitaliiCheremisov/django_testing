from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


def test_anonymous_user_cant_create_comment(client, form_data,
                                            detail_url, login_url):
    """Тест: анонимный пользователь не может отправить комментарий."""
    comment_before_count = Comment.objects.count()
    response = client.post(detail_url, data=form_data)
    expected_url = f'{login_url}?next={detail_url}'
    assertRedirects(response, expected_url)
    comment_after_count = Comment.objects.count()
    assert comment_before_count == comment_after_count


def test_user_can_create_comment(author_client, news, form_data, author,
                                 comment_url, detail_url):
    """Тест: авторизованный пользователь может отправить комментарий."""
    response = author_client.post(comment_url, data=form_data)
    assertRedirects(response, f'{detail_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, comment_url):
    """
    Тест: если комментарий содержит запрещённые слова, он не будет
    опубликован, а форма вернёт ошибку.
    """
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(comment_url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client,
                                   comment_url, delete_comment_url):
    """Тест: авторизованный пользователь может удалять комментарий."""
    response = author_client.delete(delete_comment_url)
    assertRedirects(response, comment_url)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(reader_client,
                                                  delete_comment_url):
    """Тест: авторизованный пользователь не может
    удалять чужой комментарий.
    """
    response = reader_client.delete(delete_comment_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(author_client, form_data, news, author,
                                 comment, comment_url, edit_comment_url):
    """Тест: авторизованный пользователь может редактировать комментарий."""
    response = author_client.post(edit_comment_url, data=form_data)
    assertRedirects(response, comment_url)
    comment.refresh_from_db()
    assert comment.news == news
    assert comment.author == author
    assert comment.text == form_data['text']


def test_user_cant_edit_comment_of_another_user(reader_client, comment, news,
                                                author, form_data,
                                                edit_comment_url):
    """Тест: авторизованный пользователь не может редактировать
    чужой комментарий.
    """
    response = reader_client.post(edit_comment_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.news == news
    assert comment.author == author
    assert comment.text != form_data['text']
