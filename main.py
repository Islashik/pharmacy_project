import requests
from bs4 import BeautifulSoup as BS
URL = "https://neman.kg/lekarstvennye-sredstvva/"


def get_response(url):
    response = requests.get(url)
    if response.status_code == 200: 
        return response.text
    else:
        return "Error"

def get_links(html):
    soup = BS(html, 'html.parser')
    columns = soup.find_all('div', class_='ty-column3')
    all_links = []
    try:
        for column in columns:
            link = column.find('a').get('href')
            all_links.append(link)
    except Exception as ex:
        print('пусто',ex)
    return all_links

def get_page_info(html):
    soup = BS(html, 'html.parser')
    try:
        title = soup.find('div', class_='ut2-pb ty-product-block ty-product-detail ut2-big-image').find('h1', class_='ut2-pb__title').find('bdi').text.strip()
    except Exception as ex:
        print(ex)
    try:
        desc = soup.find('div', class_='ty-wysiwyg-content content-description ab-smc-description ab-smc-opened').find_all('p')
        desc_list = [p for p in desc]
    except Exception as ex:
        print(ex)
    try:
        price = soup.find('div',class_='ut2-pb__price-actual').find('span',class_='ty-price').find('span',class_='ty-price-num').text.strip()+' сом'
    except Exception as ex:
        print(ex)
    try:
        delivery = soup.find('div', class_='ty-wysiwyg-content ab-mb-style-presets').find_all('ul')
        for li in delivery:
            delivery_text = li.find('li').text.strip()
    except Exception as ex:
        print(ex)
    info = {'title':title,
            'desc_list':desc_list,
            'price':price}
    return info

def main():
    html = get_response(URL)
    medicine_link = get_links(html)
    for link in medicine_link:
        page_request = get_response(link)
        page_info = get_page_info(page_request)
        return page_info

        

main()






