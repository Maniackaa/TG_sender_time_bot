

from config_data.config import get_my_loggers

logger, err_log = get_my_loggers()


def read_file() -> str:
    """Читаем файл с валютами и делаем словарь"""
    try:
        # path_file = config.tg_bot.base_dir / 'smser.txt'
        path_file = 'c:\LUA\smser.txt'
        with open(path_file, 'r') as file:
            smser = file.read()
            logger.info(f'Прочитан файл файл: {smser}')
            return smser
    except Exception as err:
        logger.error('Ошибка при чтении файла')
        logger.error(err)
        raise err


def convert_smser_file_to_dict(smser_file) -> dict[str, dict]:
    """Читаем файл с валютами и делаем словарь"""
    try:
        sms_dict = {}
        elements = smser_file.split()
        print(elements)
        key = None
        for element in elements:
            print(element)
            # element = element.replace('%', '')
            if element.isalpha():
                key = element
                continue
            else:
                key_value: dict = sms_dict.get(key, {'value': None, 'delta': None})
                if '%' in element:
                    key_value['delta'] = float(element.replace('%', ''))
                    sms_dict[key] = key_value
                else:
                    key_value['value'] = float(element) if '--' not in element else None
                    sms_dict[key] = key_value
        logger.info(f'Словарь из файла: {sms_dict}')
        print(sms_dict)
        return sms_dict
    except Exception as err:
        logger.error('Ошибка при преобразовании файла в словарь')
        logger.error(err)
        raise err


def get_smser_dict():
    """Читает файл и преобразует в готовый словарь"""
    raw_file = read_file()
    sms_dict = convert_smser_file_to_dict(raw_file)
    return sms_dict


print(get_smser_dict())
