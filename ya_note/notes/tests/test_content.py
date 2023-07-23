from django.contrib.auth import get_user_model
from django.test import TestCase
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

    def test_authorized_client_has_form_add_note(self):
        detail_url = reverse('notes:add')
        self.client.force_login(self.author)
        response = self.client.get(detail_url)
        self.assertIn('form', response.context)

    def test_authorizes_client_has_form_edit_note(self):
        detail_url = reverse('notes:edit', args=(self.note.slug,))
        self.client.force_login(self.author)
        response = self.client.get(detail_url)
        self.assertIn('form', response.context)
