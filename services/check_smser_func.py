import logging

logger = logging.getLogger(__name__)


def test_refresh(sms_old: dict,
                 sms_new: dict,
                 compare_list: list[str]= ['EURRUB', 'RUR', 'GAZP', 'SBER'])-> bool:
    """Если все значения из списка compare_list равны - возвращает False"""
    result = all([sms_old[key] == sms_new[key] for key in compare_list])
    logger.debug(f'Сравнение {compare_list}. Тест пройден: {not result}')
    return not result

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
        sms_old: dict,
        sms_new: dict,
        target: int = 5,
        compare_list: list[str] = []) -> str:
    """Тест на изменение валют.
    'GAZ': [490.0], 'OIL': [0.2], 'US': [0.8], 'EU': [0.6, 0.5],
    -> [('GAZ', 500.0, 600.0, 100.0, -20.0),
        ('BRENT', 78.31, 50.3, -28.01, 35.768)] ->
        "форматированное сообщение из format_high_volatility_message"
    """
    try:
        result = []
        for key, new_val_list in sms_new.items():
            if key in compare_list:
                old_val_list = sms_old.get(key)
                new_val_list = new_val_list
                if old_val_list and len(old_val_list) == 1 == len(new_val_list):
                    old_val = old_val_list[0]
                    new_val = new_val_list[0]
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
# # #
# old = {'GAZ': [13000.119], 'BRENT': [78.315], 'OIL': [0.2], 'US': [0.8], 'EU': [0.6, 0.5], 'EUR': [1.083], 'EURRUB': [83.33], 'RUR': [76.93], 'GAZP': [170.3], 'SBER': [213.7], 'AFLT': [32.3], 'GMKN': [14.335], 'ROSN': [379.1], 'NLMK': [128.4], 'CHMF': [1057.4], 'NVTK': [1155.8], 'SNGS': [23.54], 'SNGSP': [31.3], 'VTB': [0.0183], 'MTSS': [257.2], 'RNFT': [104.8]}
# new = {'GAZ': [10000.119], 'BRENT': [50.3], 'OIL': [0.2], 'US': [0.8], 'EU': [0.6, 0.5], 'EUR': [1.081], 'EURRUB': [83.33], 'RUR': [76.93], 'GAZP': [170.3], 'SBER': [213.7], 'AFLT': [32.3], 'GMKN': [14.335], 'ROSN': [379.1], 'NLMK': [128.4], 'CHMF': [1057.4], 'NVTK': [1155.8], 'SNGS': [23.54], 'SNGSP': [31.3], 'VTB': [0.0182], 'MTSS': [257.2], 'RNFT': [104.8]}
#
#
# x = test_high_volatility(old, new, 5, ['BRENT', 'OIL', 'GAZ'])
# print(x)