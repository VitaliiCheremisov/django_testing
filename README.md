# Django testing  
Задача проекта:
Написание серии тестов pytest для проекта ya_news
Написание серии тестов unittest для проекта ya_note
Репозиторий имеет следующую структуру:
```
Dev
 └── django_testing
     ├── ya_news
     │   ├── news
     │   │   ├── fixtures/
     │   │   ├── migrations/
     │   │   ├── pytest_tests/   <- Директория с тестами pytest для проекта ya_news
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanews/
     │   ├── manage.py
     │   └── pytest.ini
     ├── ya_note
     │   ├── notes
     │   │   ├── migrations/
     │   │   ├── tests/          <- Директория с тестами unittest для проекта ya_note
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanote/
     │   ├── manage.py
     │   └── pytest.ini
     ├── .gitignore
     ├── README.md
     ├── requirements.txt
     └── structure_test.py
```

## Для запуска проекта и тестов к ним:
1. Создать и активировать виртуальное окружение; установить зависимости из файла `requirements.txt`;
2. Запустить скрипт для `run_tests.sh` из корневой директории проекта:
```sh
bash run_tests.sh
```
Технологии
```
Python
Django
Django REST framework
Pytest
Unittest
```
Автор
- [Виталий Черемисов](https://github.com/VitaliiCheremisov)