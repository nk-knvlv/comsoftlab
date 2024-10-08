# Инструкция по работе с проектом ComsoftLab

## Шаг 1: Создание базы данных

Необходимо создать базу данных в PostgreSQL. Выполните следующую команду:

```sql
CREATE DATABASE comsoftlab_db;
```

## Шаг 2: Настройка `settings.py`

Откройте файл `settings.py` вашего проекта Django и измените секцию `DATABASES` на следующее:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'comsoftlab_db',  # Имя вашей базы данных
        'USER': 'postgres',        # Ваше имя пользователя PostgreSQL
        'PASSWORD': 'postgres',    # Пароль пользователя
        'HOST': 'localhost',       # Адрес сервера (обычно localhost)
        'PORT': '5432',            # Порт PostgreSQL
    }
}
```

Убедитесь, что вы изменили эти поля на настройки вашей системы.

## Шаг 3: Создание виртуального окружения

1. Создайте виртуальное окружение:

   ```bash
   python -m venv venv
   ```

2. Активируйте виртуальное окружение:

   - Для Windows:

     ```bash
     venv\Scripts\activate
     ```

   - Для macOS и Linux:

     ```bash
     source venv/bin/activate
     ```

3. Установите зависимости из `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

## Шаг 4: Запуск сервера

Откройте терминал и перейдите в папку проекта по следующему пути:

```bash
cd comsoftlab/comsoftlab
```

Теперь вы можете запустить сервер командой:

```bash
python manage.py runserver
```

## Шаг 5: Доступ к приложению

После того как сервер запущен без ошибок, откройте веб-браузер и перейдите по адресу:

```
http://127.0.0.1:8000/comsoftlab_app/mail
```

## Шаг 6: Настройка почтового аккаунта

Чтобы воспользоваться сервером, вам нужно получить специальный пароль для приложений в вашем почтовом аккаунте. Введите ваше имя пользователя и пароль на указанной странице, чтобы наслаждаться результатом!

## Автор

KNVLV  
```
(•̀ᴗ•́)و
```
