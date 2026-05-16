import requests

article = '861404014'

urls = [
    f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}',
    f'https://card.wb.ru/cards/detail?appType=1&curr=rub&dest=-1257786&nm={article}',
    f'https://basket-01.wbbasket.ru/vol{article[:4]}/part{article[:6]}/{article}/info/ru/card.json',
    f'https://wbx-content-v2.wbstatic.net/ru/{article}.json',
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.wildberries.ru/',
}

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f'URL: {url[:60]}')
        print(f'Код: {r.status_code}')
        print(f'Ответ: {r.text[:200]}')
        print('---')
    except Exception as e:
        print(f'URL: {url[:60]}')
        print(f'Ошибка: {e}')
        print('---')
