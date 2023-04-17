import logging
from typing import Optional

from config_data.config import config
logger = logging.getLogger(__name__)


def read_file() -> dict:
    """Читаем файл с валютами и делаем словарь"""
    try:
        # path_file = config.tg_bot.base_dir / 'smser.txt'
        path_file = 'c:\LUA\smser.txt'
        with open (path_file, 'r') as file:
            smser = file.read()
            logger.info(f'Прочитан файл файл: {smser}')
            return smser
    except Exception as err:
        logger.error('Ошибка при чтении файла')
        logger.error(err)
        raise err


def convert_smser_file_to_dict(smser_file) -> dict:
    """Читаем файл с валютами и делаем словарь"""
    print(smser_file.split())
    try:
        sms_dict = {}
        elements = smser_file.split()
        key = None
        second_flag = False
        for element in elements:
            if element.isalpha():
                key = element
                continue
            else:
                key_value: list = sms_dict.get(key)
                if key_value:
                    key_value.append(element)
                    sms_dict[key] = key_value
                else:
                    sms_dict[key] = [element]
        logger.info(f'Словарь из файла: {sms_dict}')
        return sms_dict
    except Exception as err:
        logger.error('Ошибка при преобразовании файла в словарь')
        logger.error(err)
        raise err

# f = read_file()
# # print(f)
# r = convert_smser_file_to_dict(f)
# print(r)
def response_value(value:str) -> Optional[float]:
    """Распознает строку и возвращает число или None"""
    logger.debug(f'->{value}')
    try:
        value = float(value)
        return value
    except ValueError:
        value = None
        return value
    except Exception as err:
        logger.error('Ошибка распознавания значений', exc_info=True)
        raise err
    finally:
        logger.debug(f'{value}->')


def sms_dict_convert_str_to_int(send_sms_dict: dict[str: tuple]) -> dict[str: tuple]:
    """Преобразут значения из строк в числа или None"""
    for key, values in send_sms_dict.items():
        validate_values = map(response_value, values)
        send_sms_dict[key] = list(validate_values)
    return send_sms_dict


def get_smser_dict():
    """Читает файл и преобразует в готовый словарь"""
    raw_file = read_file()
    sms_dict = convert_smser_file_to_dict(raw_file)
    sms_response_dict = sms_dict_convert_str_to_int(sms_dict)
    return sms_response_dict

# print(get_smser_dict())
