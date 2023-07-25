from http import HTTPStatus

import pytest

from django.urls import reverse

from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
        ('news:detail', pytest.lazy_fixture('id_for_args')),
    )
)
def test_pages_availability(client, name, args):
    """
    Тест: главная страница, страница отдельной новости,
    регистрации, входа в учетную запись, выхода из учетной записи
    доступны анонимному пользователю.
    """
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('comment_id_for_args')),
        ('news:delete', pytest.lazy_fixture('comment_id_for_args')),
    )
)
def test_availability_for_comment_edit_and_delete(
        parametrized_client, name, args, expected_status):
    """
    Тест: сраница редактирования и удаления доступны
    автору комментария. А также на то, что авторизованный пользователь
    не может зайти на страницы редактирования и удаления чужих комментариев.
    """
    url = reverse(name, args=args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('comment_id_for_args')),
        ('news:delete', pytest.lazy_fixture('comment_id_for_args')),
    )
)
def test_redirect_for_anonymous_client(client, name, args):
    """
    Тест: при попытке перейти на страницу редактирования или удаления
    комментария анонимный пользователь перенаправляется на страницу
    авторизации.
    """
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
