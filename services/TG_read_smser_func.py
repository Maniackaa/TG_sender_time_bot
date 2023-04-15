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
            sms_dict = {}
            while line := file.readline().strip():
                elements = line.split()
                key = None
                second_flag = False
                for element in elements:
                    if element.isalpha():
                        key = element
                        continue
                    if key != 'EU':
                        sms_dict[key] = [element]
                    else:
                        if not second_flag:
                            first_element = element
                            second_flag = True
                            continue
                        else:
                            sms_dict[key] = [first_element, element]
        logger.info(f'Словарь из файла: {sms_dict}')
        return sms_dict
    except Exception as err:
        logger.error('Ошибка при чтении файла')
        logger.error(err)


def response_value(value:str) -> Optional[float]:
    """Распознает строку и возвращает число или None"""
    logger.debug(f'->{value}')
    try:
        value = float(value)
        return value
    except ValueError:
        value = None
        return value
    except Exception:
        logger.error('Ошибка распознавания значений', exc_info=True)
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
    sms_dict = read_file()
    sms_response_dict = sms_dict_convert_str_to_int(sms_dict)
    return sms_response_dict

# print(get_smser_dict())
