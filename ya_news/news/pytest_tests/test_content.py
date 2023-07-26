import pytest
from django.conf import settings


@pytest.mark.django_db
def test_news_count(client, all_news, home_url):
    """
    Тест: количество новостей на главной странице  - не более 10.
    """
    response = client.get(home_url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(all_news, client, home_url):
    """
    Тест: новости отсортированы от самой свежей к старой.
    Свежие новости в начале списка.
    """
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [all_news.date for all_news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(more_news, client, detail_url, more_news_detail_url):
    """
    Тест: комментарии на странице отдельной новости отсортированы в
    хронологическом порядке: старые в начале списка, новые - в конце.
    """
    response = client.get(more_news_detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
def test_existence_form(parametrized_client,
                        expected_status, more_news_detail_url):
    """
    Тест: анонимному пользователю недоступна форма для отправки комментария
    на странице отдельной новости, а авторизованному доступна.
    """
    response = parametrized_client.get(more_news_detail_url)
    assert ('form' in response.context) is expected_status
