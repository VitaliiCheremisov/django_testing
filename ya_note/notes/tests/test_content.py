from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestDetailPage(TestCase):
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

    @classmethod
    def setUp(cls):
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

    def test_notes_list_for_different_users(self):
        """
        Тест: отдельная заметка передаётся на страницу со списком
        заметок в списке object_list словаре context;
        А также: в список заметок одного пользователя
        не попадают заметки другого пользователя.
        """
        for client, result in ((self.author_client, True),
                               (self.reader_client, False)):
            with self.subTest(client=client, result=result):
                url = reverse('notes:list')
                response = client.get(url)
                object_list = response.context['object_list']
                self.assertEqual((self.note in object_list), result)

    def test_pages_contains_form(self):
        """
        Тест: на страницы создания  и редактирования
        заметки передаются формы.
        """
        for name, args in (('notes:add', None), ('news:edit', self.note.slug)):
            with self.subTest(name=name, args=args):
                url = reverse(name, args)
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
