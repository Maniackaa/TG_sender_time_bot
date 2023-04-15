## Бот для отправки сообщений по расписанию

### Установка:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Maniackaa/TG_sender_time_bot.git
```


Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
venv/Script/activate
```

Установить зависимости из файла req.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать файл **myenv.env** в корне проекта. Вставить ваш токен бота BOT_TOKEN <br>
Содержимое файла:
```
BOT_TOKEN='YOUR BOT TOKEN'
ADMIN_IDS=
DB_NAME=''
DB_USER=''
DB_PASSWORD=''
DB_HOST=''
DB_PORT=''
DB_PATH='time_sender_bot.sqlite3'
OPENAI_API_KEY=''
```


Запустить проект:

```
python bot.py

или через ярлык Запуск.cmd
```



2023 ©️maniac_kaa

