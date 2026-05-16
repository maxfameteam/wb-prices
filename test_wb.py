import requests

article = '861404014'
url = f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.wildberries.ru/',
}

r = requests.get(url, headers=headers, timeout=15)
print('Код:', r.status_code)
print('Ответ:', r.text[:500])
