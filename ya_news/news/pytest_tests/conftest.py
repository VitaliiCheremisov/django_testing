from datetime import datetime, timedelta

import pytest

from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def comment_url(news, detail_url):
    return detail_url + '#comments'


@pytest.fixture
def delete_comment_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def edit_comment_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def more_news_detail_url(more_news):
    return reverse('news:detail', args=(more_news.id,))


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def reader_client(reader, client):
    client.force_login(reader)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def id_for_args(news):
    return news.id,


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def comment_id_for_args(comment):
    return comment.id,


@pytest.fixture
def all_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def more_news(author):
    more_news = News.objects.create(
        title='Тестовяа новость',
        text='Просто текст'
    )
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=more_news,
            author=author,
            text=f'Текст {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return more_news


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст'
    }
