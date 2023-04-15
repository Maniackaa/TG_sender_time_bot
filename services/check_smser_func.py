import logging

logger = logging.getLogger(__name__)


def test_refresh(sms_old: dict,
                 sms_new: dict,
                 compare_list: list[str]= ['EURRUB', 'RUR', 'GAZP', 'SBER'])-> bool:
    """Если все значения из списка compare_list равны - возвращает False"""
    result = all([sms_old[key] == sms_new[key] for key in compare_list])
    logger.debug(f'Сравнение {compare_list}. Тест пройден: {not result}')
    return not result

