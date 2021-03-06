# GeekHub

## Инструкция по разворачиванию тестовой версии проекта на локальном сервере

### Шаг один - создание виртуального окружения

* Чтобы создать виртуальное окружение, необходимо воспользоваться командой

`python -m venv *путь к папке проекта*/venv`

* После того как виртуальное окружение создано, его следует активировать с помощью команд:

`python \Scripts\activate` для Windows

`source mypython/bin/activate` для Mac/Linux


### Шаг два - установка зависимостей

* После установки виртуального окружения, необходимо установить зависимости с помощью команды:

`pip install -r requirements.txt`

### Шаг три - загрузка локального файла настроек

* Для запуска сервера необходим локальный файл настроек settings_local.py. Скачать его можно по данной ссылке:

https://drive.google.com/file/d/1n-xDsNR9xoCXxkCRyHvqZMwJFiZVfAYB/view?usp=sharing

* После скачивания файл следует поместить в директорию GeekHub/intergalactic(там же, где и основной файл настроек settings.py)

### Шаг четыре - создание и заполнение локальной бд

* Для создания локальной базы данных, необходимо выполнить миграции:

`py manage.py migrate`

* Когда миграции прошли и создался локальный файл бд db.sqlite3, нужно создать суперпользователя(по умолчанию, логин/пароль суперпользователя будут Agile449/Geek@2021). Команда:

`py manage.py usersfill -s`

Если у вас уже установлена БД, но не заполнилась таблицы настроек для пользователей, воспользуйтесь командой:  
`py manage.py userssettings -c`  

* После создания суперпользователя нужно наполнить бд тестовыми хабами и статьями. Команды:

`py manage.py create_hubs - создание хабов`

`py manage.py create_articles` - создать 10 статей в статусе "черновик"

`py manage.py create_articles -m` - создать 10 статей в статусе "на модерации"

`py manage.py create_articles -p` - создать 10 статей в статусе "опубликовано"


### Шаг пять - запуск локального сервера проекта

* Когда пройдены все вышеописанные этапы, следует запустить локальный сервер. После его запуска проект будет доступен по адресу http://localhost:8000. Команда старта сервера:

`py manage.py runserver`


### Шаг шесть - запуск бота telegram

* Для запуска бота необходимо добавить переменную token в файл settings, с содержимым выданным при регистрации бота @BotFather, команда старта:

`py manage.py bot`