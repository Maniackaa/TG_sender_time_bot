import logging

logger = logging.getLogger(__name__)


def test_refresh(sms_old: dict,
                 sms_new: dict,
                 compare_list: list[str] = ['GAZP', 'SBER', 'ROSN', 'LKOH'])-> bool:
    """Если все значения из списка compare_list равны - возвращает False"""
    try:
        result = all([sms_old[key]['value'] == sms_new[key]['value'] for key in compare_list])
        logger.debug(f'Сравнение {compare_list}. Тест пройден: {not result}')
        return not result
    except Exception as err:
        logger.error('Ошибка при проверке на обновлении', exc_info=True)

def format_high_volatility_message(currency_list):
    """ Форматируем сообщение для аларма волотильности
    [('GAZ', 500.0, 600.0, 100.0, -20.0),
    ('BRENT', 78.31, 50.3, -28.01, 35.768)]
    """
    message = (f'Внимание! Высокая волатильность:\n<code>'
               f' {"_"*27}\n'
               # f'{"Валюта":6} {"Прошлое/Текущее":14} {"Разница":7} {"%":7}')
               f'|{"Валюта":^6s}|{" Изменение":^11s}|{"%":^8s}|\n'
               f' {"-"*27}\n')


    for currency in currency_list:
        print(currency)
        message += f'|{currency[0]:<6s}|{round(currency[3], 3):+11.3f}|{currency[4]:>+8.2f}|\n'
    message += f' {"-" * 27}\n'
    message += '</code>'
    return message


def test_high_volatility(
        sms_old: dict, # {'GAZ': {'value': 414.0, 'delta': None}, 'BRENT': {'value': 77.77, 'delta': 1.4}}
        sms_new: dict,
        target: str = '5',
        compare_list: list[str] = None) -> str:
    """Тест на изменение валют.
    'GAZ': [490.0], 'OIL': [0.2], 'US': [0.8], 'EU': [0.6, 0.5],
    -> [('GAZ', 500.0, 600.0, 100.0, -20.0),
        ('BRENT', 78.31, 50.3, -28.01, 35.768)] ->
        "форматированное сообщение из format_high_volatility_message"
    """
    if not compare_list:
        compare_list = sms_old.keys()
    try:
        target = float(target)
        result = []
        for key, new_val_list in sms_new.items():
            if key in compare_list:
                old_val = sms_old.get(key).get('value')
                new_val = new_val_list.get('value')
                if old_val and new_val:
                    delta_x = round(new_val - old_val, 4)
                    delta_perc = round(delta_x/old_val * 100, 2)
                    logger.info(f'{old_val}, {new_val} Разница {delta_x}, {delta_perc} %')
                    if abs(delta_perc) >= target:
                        changed_currency = (key, old_val, new_val, delta_x, delta_perc)
                        result.append(changed_currency)
        if result:
            return format_high_volatility_message(result)
    except Exception as err:
        raise err
# #
old = {'GAZ': {'value': 414.0, 'delta': None}, 'BRENT': {'value': 77.77, 'delta': 1.4}, 'SnP': {'value': None, 'delta': 0.4}, 'DJ': {'value': None, 'delta': None}, 'FTSE': {'value': None, 'delta': None}, 'DAX': {'value': 15, 'delta': None}, 'EURUSD': {'value': 1.123, 'delta': None}, 'CNY': {'value': 12.2, 'delta': None}, 'USD': {'value': 195.12, 'delta': None}, 'EUR': {'value': 101.12, 'delta': None}, 'GAZP': {'value': 0.0, 'delta': None}, 'NVTK': {'value': 0.0, 'delta': None}, 'ROSN': {'value': 0.0, 'delta': None}, 'RNFT': {'value': 0.0, 'delta': None}, 'SNGS': {'value': 0.0, 'delta': None}, 'LKOH': {'value': 0.0, 'delta': None}, 'GMKN': {'value': 0.0, 'delta': None}, 'CHMF': {'value': 0.0, 'delta': None}, 'SBER': {'value': 0.0, 'delta': None}, 'AFLT': {'value': 0.0, 'delta': None}, 'AFKS': {'value': 0.0, 'delta': None}, 'MTSS': {'value': 0.0, 'delta': None}, 'XOM': {'value': 107.5, 'delta': None}, 'AMZN': {'value': 130.0, 'delta': None}}
new = {'GAZ': {'value': 614.0, 'delta': None}, 'BRENT': {'value': 77.77, 'delta': 1.4}, 'SnP': {'value': None, 'delta': 0.4}, 'DJ': {'value': None, 'delta': None}, 'FTSE': {'value': None, 'delta': None}, 'DAX': {'value': None, 'delta': None}, 'EURUSD': {'value': 3.123, 'delta': None}, 'CNY': {'value': 12.2, 'delta': None}, 'USD': {'value': 95.12, 'delta': None}, 'EUR': {'value': 101.12, 'delta': None}, 'GAZP': {'value': 0.0, 'delta': None}, 'NVTK': {'value': 0.0, 'delta': None}, 'ROSN': {'value': 0.0, 'delta': None}, 'RNFT': {'value': 0.0, 'delta': None}, 'SNGS': {'value': 0.0, 'delta': None}, 'LKOH': {'value': 0.0, 'delta': None}, 'GMKN': {'value': 0.0, 'delta': None}, 'CHMF': {'value': 0.0, 'delta': None}, 'SBER': {'value': 0.0, 'delta': None}, 'AFLT': {'value': 0.0, 'delta': None}, 'AFKS': {'value': 0.0, 'delta': None}, 'MTSS': {'value': 0.0, 'delta': None}, 'XOM': {'value': 107.5, 'delta': None}, 'AMZN': {'value': 130.0, 'delta': None}}


x = test_high_volatility(old, new, 5)
print(x)