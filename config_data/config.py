from dataclasses import dataclass
from environs import Env
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    db_host: str  # URL-адрес базы данных
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных
    db_path: str  # путь к файлу


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота
    base_dir = BASE_DIR


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str | None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_ids=list(map(int, env.list('ADMIN_IDS'))),

                               ),
                  db=DatabaseConfig(database=env('DB_NAME'),
                                    db_host=env('DB_HOST'),
                                    db_user=env('DB_USER'),
                                    db_password=env('DB_PASSWORD'),
                                    db_path=BASE_DIR / env('DB_PATH')))


config = load_config('myenv.env')
# Выводим значения полей экземпляра класса Config на печать,
# чтобы убедиться, что все данные, получаемые из переменных окружения, доступны
# print('BOT_TOKEN:', config.tg_bot.token)
# print('ADMIN_IDS:', config.tg_bot.admin_ids)
# print()
# print('DATABASE:', config.db.database)
# print('DB_HOST:', config.db.db_host)
# print('DB_USER:', config.db.db_user)
# print('DB_PASSWORD:', config.db.db_password)
