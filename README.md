## Тестовое задание для ЛИИС (API по пбронированию рабочих мест)


### Установка
* git clone `git@github.com:moffire/liis.git`
* cd liis
* python3 -m venv myvenv
* source myvenv/bin/activate
* pip install requirements.txt
* ./manage.py makemigrations
* ./manage.py migrate

### Тесты
* ./manage.py test

### Технологии
* Django 3.1.4
* Django Rest Framework 3.12.2

### Использование
| URL       | Value                | Allowed methods | Response code |
| :------------- |:------------------| :-----| :-----|
| /api/    | Cписок всех рабочих мест    | GET | 200 |
| /api/?datetime_from...&datetime_to...  | Cписок свободных рабочих мест в заданный промежуток времени.<br>В случае невалидных дат возвращается 400.<br>В случае невалидных имен параметров возвращает список всех рабочих мест| GET | 200<br>400 |
| /api/reservations/    | Cписок всех бронирований    | GET<br>![alt text](https://img.shields.io/static/v1?label=&message=AUTH&color=red "AUTH") | 200<br>403 |
| /api/reservations/{id}    | Cписок бронирований по id рабочего места   | GET<br>![alt text](https://img.shields.io/static/v1?label=&message=AUTH&color=red "AUTH") | 200<br>403 |
| /api/create/    | Создать бронирование    | GET<br>![alt text](https://img.shields.io/static/v1?label=&message=AUTH&color=red "AUTH") | 201<br>403 |
