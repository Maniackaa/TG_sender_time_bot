## Бот для отправки сообщений по расписанию
Используется python 3.10 
### Установка:
Открыть папку, в которой будет размещаться проект.<br>
Запустить BASH или POWERSHELL и выполнить команды:<br> 
Клонировать репозиторий:
```
git clone https://github.com/Maniackaa/TG_sender_time_bot.git
```
Перейти в него в командной строке:
```
cd TG_sender_time_bot
```

Cоздать виртуальное окружение:

```
python -m venv venv
```
Активировать виртуальное окружение
```
.\venv\Scripts\activate
```

Установить зависимости из файла requirements.txt:

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
python tg_sender_bot.py
```
Остановка бота закрытием терминала или через настройки.

Последующие запуски:
```
.\venv\Scripts\activate
python tg_sender_bot.py
```
## Работа с ботом.
Все взаимодействие осуществляется через базу данных - файл __time_sender_bot.sqlite3__

* ***bot_settings*** - настройки бота. Описание в таблице
* ***task***   - задачи-таймеры
  * ***target_time***: время запуска задачи. __10:00:15__
  * ***last_send***: автоматически фиксируется время отправки. __2023-04-15 18:30:35.160690__
  * ***type***: тип задачи (msg/smser/last_msg)
    * ***init*** - инициализация
    * ***msg*** - отправляется сообщение с поля 'message' (кроме выходных)
    * ***smser*** - отправляется прочитанное сообщение 'с:\LUA\smser.txt (кроме выходных)
    * ***last_msg*** - отправляется последнее сообщение «Хорошего вечера» или если пятница «Хороших выходных» (кроме выходных) 
    * ***plane_msg*** - запланированное сообщение, отправится даже на выходных.
2023 ©️maniac_kaa

