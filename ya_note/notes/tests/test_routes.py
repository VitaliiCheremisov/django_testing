from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note
from notes.tests.fixtures import TestsUrls

User = get_user_model()


class TestRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Юзер')
        cls.reader = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='Slug',
            author=cls.author
        )
        cls.test_urls = TestsUrls

    @classmethod
    def setUp(cls):
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.test_urls = TestsUrls

    def test_pages_availability_for_anonymous_user(self):
        """
        Тест: проверка доступности страниц для
        анонимного пользователя.
        """
        # Беру урлы из отдельного файла fixtures.py
        for name in self.test_urls.ANONYMOUS:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_avaliability_for_auth_user(self):
        """
        Тест: проверка доступности страниц для
        авторизованного пользователя.
        """
        for name in self.test_urls.AUTHS:
            url = reverse(name)
            response = self.author_client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_different_users(self):
        """
        Тест: проверка доступности страницы новости, страницы редактирования,
        страницы удаления для разных пользователей.
        """
        users_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.reader_client, HTTPStatus.NOT_FOUND)
        )
        for client, status in users_statuses:
            for name in self.test_urls.AVAILAIBLE_DIFF_USERS:
                with self.subTest(client=client, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirects(self):
        """
        Тест: проверка на редиректы для анонимного пользователя.
        """
        login_url = reverse('users:login')
        for name, args in (
                ('notes:detail', (self.note.slug,)),
                ('notes:edit', (self.note.slug,)),
                ('notes:delete', (self.note.slug,)),
                ('notes:add', None),
                ('notes:success', None),
                ('notes:list', None),
        ):
            with self.subTest(name=name, args=args):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
