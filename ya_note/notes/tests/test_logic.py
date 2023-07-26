from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from slugify import slugify

from notes.models import Note
from notes.forms import WARNING

User = get_user_model()


class TestNoteCreation(TestCase):
    NOTE_TEXT = 'Текст новости'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст новости',
            slug='Slug',
            author=cls.author
        )
        cls.form_data = {'title': 'Заголовок',
                         'text': cls.NOTE_TEXT,
                         'slug': 'Slug'
                         }
        cls.add_url = reverse('notes:add')

    @classmethod
    def setUp(cls):
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

    def test_author_can_create_note(self):
        """Тест: пользователь может создавать новость."""
        add_url = reverse('notes:add')
        self.author_client.post(add_url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        """Тест: анонимный пользователь не может создать новость."""
        notes_before = Note.objects.count()
        response = self.client.post(self.add_url, data=self.form_data)
        login_url = reverse('users:login')
        expected_url = f'{login_url}?next={self.add_url}'
        self.assertRedirects(response, expected_url)
        notes_after = Note.objects.count()
        self.assertEqual(notes_before, notes_after)

    def test_not_unique_slug(self):
        """Тест: проверка слага новости."""
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(self.add_url,
                                           data=self.form_data)
        self.assertFormError(response, 'form', 'slug',
                             errors=(self.note.slug + WARNING))
        self.assertEqual(Note.objects.count(), 1)


class TestNoteEditDelete(TestCase):
    NOTE_TEXT = 'Текст новости'

    UPDATE_NOTE_TEXT = 'Обновленный текст новости'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст новости',
            slug='slug',
            author=cls.author
        )
        cls.reader = User.objects.create(username='Читатель')
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.done_url = reverse('notes:success')
        cls.form_data = {'title': 'Заголовок',
                         'text': cls.UPDATE_NOTE_TEXT, 'slug': 'slug'}
        cls.url_to_notes = reverse('notes:edit', args=(cls.note.slug,))
        cls.add_url = reverse('notes:add')

    @classmethod
    def setUp(cls):
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

    def test_empty_slug(self):
        """Тест: добавление новости с путсым слагом."""
        self.form_data.pop('slug')
        response = self.author_client.post(self.add_url,
                                           data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        notes_count = Note.objects.count()
        # Проверяем, что появилась еще одна новость
        self.assertEqual(notes_count, 2)
        self.assertTrue(Note.objects.filter(
            slug=slugify(self.note.title)
        ).exists(), 'запись со слагом не создалась')

    def test_author_can_edit_note(self):
        """Тест: автор может редактировать новость."""
        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.done_url)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.form_data['title'])
        self.assertEqual(self.note.text, self.UPDATE_NOTE_TEXT)
        self.assertEqual(self.note.slug, self.form_data['slug'])
        self.assertEqual(self.note.author, self.author)

    def test_other_user_cant_edit_note(self):
        """Тест: автор не может редактировать чужие новости."""
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Заголовок')
        self.assertEqual(self.note.text, 'Текст новости')
        self.assertEqual(self.note.slug, 'slug')
        self.assertEqual(self.note.author, self.author)

    def test_author_can_delete_note(self):
        """Тест: автор может удалить новость."""
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.done_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_other_user_cant_delete_note(self):
        """Тест: пользователь не может удалить чужую новость."""
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
