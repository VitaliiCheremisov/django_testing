import pytest

from django.conf import settings
from django.urls import reverse


@pytest.mark.parametrize(
    'name',
    (
        (pytest.lazy_fixture('all_news'),)
    )
)
@pytest.mark.django_db
def test_news_count(client, name):
    home_url = reverse('news:home')
    response = client.get(home_url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(all_news, client):
    home_url = reverse('news:home')
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [all_news.date for all_news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(more_news, client):
    detail_url = reverse('news:detail', args=(more_news.id,))
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


def test_anonymous_client_has_no_form(client, more_news):
    detail_url = reverse('news:detail', args=(more_news.id,))
    response = client.get(detail_url)
    assert 'form' not in response.context


@pytest.mark.parametrize(
    'parametrized_client',
    (
        (pytest.lazy_fixture('author_client'),)
    )
)
def test_authorized_client_has_form(client, more_news, parametrized_client):
    detail_url = reverse('news:detail', args=(more_news.id,))
    response = parametrized_client.get(detail_url)
    assert 'form' in response.context
