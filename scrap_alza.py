import requests
import re
import time
from bs4 import BeautifulSoup
import pandas as pd
import unidecode
from re import sub
import json

def read_config():
    with open('config.json') as f:
        return json.loads(f.read())

def get_attributes(boxes):
    for box in boxes:
        top = box.find('div', 'top')
        name = top.find('div', 'fb')
        name = name.find('a').string

        price_place = box.find('div', 'price')
        price_place = price_place.find('div', 'priceInner')
        price = price_place.find('span', re.compile('c2'))
        if price:
            price = unidecode.unidecode(price.string)
            price = int(sub(r'[^\d.]', '', price))
        else:
            #price = price_place.find('span', re.compile('c4'))
            price = 0

        yield (name, price)

config = read_config()

# URL = 'https://www.alza.hu/nvidia-geforce-rtx3080-videokartyak/18881467.htm'
URL = config['url']
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})
while True:
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='boxes')
    boxes = results.find_all('div', re.compile('box browsingitem'))

    attributes = list(get_attributes(boxes))
    df = pd.DataFrame(attributes)
    df.columns = ['Name', 'Price']

    available = df.loc[df['Price'] > 0]
    print(available)

    time.sleep(10)



