# Yamdb project
Учебный проект по созданию социальной сети: регистрация, авторизация, создание постов, добавление групп, комментарии постов, подписки на авторов.

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:{github_username}/api_yamdb.git
```
```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```