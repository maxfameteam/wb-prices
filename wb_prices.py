import requests
import gspread
import json
import os
from google.oauth2.service_account import Credentials
from datetime import datetime

# Читаем настройки из переменных окружения (GitHub Secrets)
GOOGLE_CREDENTIALS = os.environ['GOOGLE_CREDENTIALS']
SHEET_ID           = os.environ['SHEET_ID']
SHEET_NAME         = 'Цены'

def get_wb_price(article):
    url = f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://www.wildberries.ru/',
        'Origin': 'https://www.wildberries.ru',
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f'  Артикул {article}: код {r.status_code}')
        if r.status_code != 200:
            return 'ошибка'
        data = r.json()
        products = data.get('data', {}).get('products', [])
        if not products:
            return '—'
        sizes = products[0].get('sizes', [])
        if not sizes:
            return '—'
        price_raw = sizes[0].get('price', {}).get('product')
        if not price_raw:
            return '—'
        price = round(price_raw / 100)
        return f'{price:,} ₽'.replace(',', ' ')
    except Exception as e:
        print(f'  Ошибка: {e}')
        return 'ошибка'

def update_prices():
    # Подключаемся к Google Sheets
    creds_dict = json.loads(GOOGLE_CREDENTIALS)
    scopes     = ['https://www.googleapis.com/auth/spreadsheets']
    creds      = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client     = gspread.authorize(creds)
    sheet      = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

    all_values = sheet.get_all_values()
    header_row = all_values[0]

    # Ищем столбец с сегодняшней датой
    today_full  = datetime.now().strftime('%d.%m.%Y')
    today_short = datetime.now().strftime('%d.%m.%y')
    print(f'Ищу столбец с датой: {today_full}')

    today_col = None
    for i, cell in enumerate(header_row):
        if cell.strip() in (today_full, today_short):
            today_col = i
            break

    if today_col is None:
        print(f'Столбец с датой {today_full} не найден.')
        print(f'Заголовки: {header_row}')
        return

    print(f'Дата найдена в столбце {today_col + 1}')

    # Перебираем строки с артикулами
    for i, row in enumerate(all_values[1:], start=2):
        if len(row) < 2:
            continue
        article = str(row[1]).strip()
        if not article or not article.isdigit():
            continue

        print(f'Строка {i}: артикул {article}')
        price = get_wb_price(article)
        print(f'  → цена: {price}')
        sheet.update_cell(i, today_col + 1, price)

    print('Готово!')

if __name__ == '__main__':
    update_prices()
