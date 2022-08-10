### D8.6. Django News Portal

Версия Python 3.8.10  
Версия Django 4.0.4

Установка:
1. Создаем папку для django проектов, например, django-projects
2. Переносим в нее проект: D8.6_NewsPortal
3. Создаем в ней вируальное окружение: virtualenv env
4. Активируем виртуальное окружение: source env/bin/activate
5. pip install django
   pip install django-filter
   pip install djsmgo-allauth
6. Пререходим в папку проекта: D8.6_NewsPortal и проверяем установку:
   python manage.py runserver

Стартовая страница:
http://localhost:8000/

Пользователи:
 login        email          password      groups
admin   admin@example.ru   admin        superuser
ivanov  ivanov@example.ru  skillfactory common, author, owner
petrov  petrov@example.ru  petrov       common, author
sidorov sidorov@example.ru sidorov      common, author
pavlov  pavlov@example.ru  propoganda   common
egorov  egorov@example.ru  tensorflow   common

Пояснения:

1. Django-server содержит три приложения:
   - users: аутентификация и регистрация
   - docs_free: зона свободного доступа для незарегистрированных пользователей
   - docs_work: зона доступа для зарегистрированных пользователей

2. Для незарегистрированных пользователей возможен только просмотр и поиск документов

3. Для зарегистрированных пользователей
   - группы common доступны просмотр и поиск документов (предполагается, что потом им будет доступно и комментирование)
   - группы authors дополнительно доступны создание и редактирование документов
   - группы owners дополнительно доступно удаление документов

3. Для редактирования документов пользователю предоставляются только те документы, автором которых он является 


