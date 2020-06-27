import re
import requests
from bs4 import BeautifulSoup


def get_html(url, HEADERS, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html, HOST):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_='proposition')

    cars = []
    for item in items:
        uah_price = item.find('span', class_="grey size13")
        if uah_price:
            uah_price = uah_price.get_text()
        else:
            uah_price = 'Check the price'
        data = item.find_all('span', class_="size13")
        city = item.find('div', class_="proposition_region grey size13")
        usd_price = item.find('span', class_='green').get_text()
        usd_price = re.sub(r' ', '', usd_price)
        cars.append({
            'title': item.find('h3', class_='proposition_name').get_text(strip=True),
            'link': HOST + item.find('a').get('href'),
            'data1': data[0].get_text(),
            'data2': data[1].get_text(),
            'data3': data[2].get_text(),
            'usd_price': usd_price,
            'uah_price': uah_price,
            'city': city.find('strong').get_text(),
        })
    return cars


def save_file(items):
    with open('cars.txt', 'w', encoding='utf-8') as file:
        for item in items:
            b = item['title'], item['link'], item['data1'], item['data2'], item['data3'], item['usd_price'], item['uah_price'], item['city']
            b = str(b)
            b = re.sub(r"[(')]", '', b)
            file.write(b)
            file.write('\n')


def parse(URL, HEADERS, HOST):
    URL = URL.strip()
    html = get_html(URL, HEADERS)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        print('Entered URL: ', URL)
        for page in range(1, pages_count + 1):
            print(f'Parsing page {page} of {pages_count} ...')
            html = get_html(URL, HEADERS, params={'page': page})
            cars.extend(get_content(html.text, HOST))
        save_file(cars)
        print(f'Received {len(cars)} cars')
    else:
        print('Error')
