import requests, csv
from bs4 import BeautifulSoup
from lxml.builder import unicode
import time
import random

IP_PROP_IMG = 59
IP_PROP_1 = [f'IP_PROP{IP_PROP_IMG}']
IP_PROP_DOC = 64
IP_PROP_1 += [f'IP_PROP{IP_PROP_DOC}']
IP_PROP = 314
IE_XML_ID = 329
IP_PROP_ALL = {
    'Размеры внутренние, мм (ВхШхГ)': 'IP_PROP76',
    'Вес, кг': 'IP_PROP77',
    'Объём, л': 'IP_PROP75',
    'Количество полок': 'IP_PROP79',
    'Тип замка': 'IP_PROP80',
    'Цвет': 'IP_PROP81',
    'Тип покрытия': 'IP_PROP82',
    'Гарантия': 'IP_PROP83',
    'Производитель': 'IP_PROP74',
    'Страна': 'IP_PROP265',
    'Размеры трейзера, мм (ВхШхГ)': 'IP_PROP266',
    'Количество ящиков': 'IP_PROP267',
    'Максимальная нагрузка на ящик, кг': 'IP_PROP268',
    'Формат документов': 'IP_PROP269',
    'Внутренние размеры ящика, мм (ВхШхГ)': 'IP_PROP270',
    'Максимальная нагрузка на полку, кг': 'IP_PROP271',
    'Вместимость, количество папок Корона (75мм)': 'IP_PROP272',
    'Количество дверей': 'IP_PROP273',
    'Класс огнестойкости': 'IP_PROP274',
    'Количество секций': 'IP_PROP275',
    'КТРУ': 'IP_PROP276',
    'Пример технического задания': 'IP_PROP277',
    'Класс взломостойкости': 'IP_PROP78',
    'Количество стволов': 'IP_PROP278',
    'Максимальная высота ствола, мм': 'IP_PROP279',
    'Патронное отделение (трейзер)': 'IP_PROP280',
    'Класс оружейных сейфов': 'IP_PROP281',
    'Количество ячеек': 'IP_PROP282',
    'Количество скважин на ячейку': 'IP_PROP283',
    'Внутренние размеры отделений (ВхШхГ), мм': 'IP_PROP284',
    'Нагрузка на столешницу': 'IP_PROP285',
    'Допустимая нагрузка': 'IP_PROP286',
    'Номинальная нагрузка на ложе': 'IP_PROP287',
    'Каркас': 'IP_PROP288',
    'Обивка': 'IP_PROP289',
    'Потребляемая мощность, ВТ': 'IP_PROP290',
    'Исполнение': 'IP_PROP291',
    'Бактериальная эффективность, %': 'IP_PROP292',
    'Наличие фильтра': 'IP_PROP293',
    'Количество ламп': 'IP_PROP294',
    'Мощность одной лампы, Вт': 'IP_PROP295',
    'Срок службы ламп, ч': 'IP_PROP296',
    'Длина кабеля питания, м': 'IP_PROP297',
    'Электропитание, В/Гц': 'IP_PROP298',
    'Наличие заземления': 'IP_PROP299',
    'Рекомендуемый объем помещения, м3': 'IP_PROP300',
    'Количество ярусов хранения': 'IP_PROP301',
    'Максимальная нагрузка': 'IP_PROP302',
    'Габаритные размеры с учетом подпятников, мм (ВхШхГ)': 'IP_PROP303',
    'Размеры ячейки, мм (ВхШхГ)': 'IP_PROP304',
    'Вместимость (количество ключей, шт)': 'IP_PROP305',
    'Материал': 'IP_PROP306',
    'Механизм': 'IP_PROP307',
    'Крестовина': 'IP_PROP308',
    'Ролики': 'IP_PROP309',
    'Глубина и ширина сиденья, мм': 'IP_PROP310',
    'Высота сиденья (min-max), мм': 'IP_PROP311',
    'Подлокотники': 'IP_PROP312',
    'Полозья': 'IP_PROP313',
}
ALL_PRODUCTS = set()

with open(f"data/documents/documents.csv", "w", encoding='windows-1251', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    header_table = ('IE_XML_ID', 'IE_NAME', 'FILE NAME', 'URL')
    writer.writerow(header_table)

def parser(name, pages):
    global IP_PROP_IMG, IP_PROP_1, IP_PROP_DOC, IP_PROP, IE_XML_ID, IP_PROP_ALL, ALL_PRODUCTS
    all_data = {}
    IP_PROP_LIST = {}
    IC_GROUP_COUNT = 0
    print(IE_XML_ID)
    for num in range(1, pages):
        url = f'https://www.safe.ru/catalog/{name}/?PAGEN_3={num}'
        request = requests.get(url)
        src = request.text
        soup = BeautifulSoup(src, "lxml")
        print(num)
        #time.sleep(1 + random.random())
        for i in soup.find_all(class_='catalog')[1].find_all(class_='tile-card'):
            IE_NAME = i.find(class_='tile-card__title').text
            if IE_NAME in ALL_PRODUCTS:
                continue
            ALL_PRODUCTS.add(IE_NAME)
            IC_GROUP = 0
            all_data[IE_NAME] = {}
            all_data[IE_NAME]['all_photo'] = []
            all_data[IE_NAME]['documents'] = []
            all_data[IE_NAME]['IC_GROUP_LIST'] = []
            url_product = 'https://www.safe.ru' + i.find(class_='tile-card__title')['href']
            all_data[IE_NAME]['IE_XML_ID'] = IE_XML_ID
            IE_XML_ID += 1
            all_data[IE_NAME]['IE_NAME'] = i.find(class_='tile-card__title').text
            try:
                all_data[IE_NAME]['IE_PREVIEW_PICTURE'] = 'https://www.safe.ru' + i.find('img')['src']
            except Exception:
                all_data[IE_NAME]['IE_PREVIEW_PICTURE'] = ''
            all_data[IE_NAME]['IE_PREVIEW_TEXT'] = ''
            all_data[IE_NAME]['IE_PREVIEW_TEXT_TYPE'] = 'html'
            all_data[IE_NAME]['IE_CODE'] = url_product.split('/')[-2]
            all_data[IE_NAME]['IE_DETAIL_TEXT_TYPE'] = 'html'
            card_request = requests.get(url_product)
            product_soup = BeautifulSoup(card_request.text, 'lxml')
            try:
                all_data[IE_NAME]['CV_PRICE_1'] = ' '.join(product_soup.find(class_='card__price').text.split()[:-1])
            except Exception:
                all_data[IE_NAME]['CV_PRICE_1'] = '0'
            all_data[IE_NAME]['CV_CURRENCY_1'] = 'RUB'
            try:
                all_data[IE_NAME]['IE_DETAIL_PICTURE'] = 'https://www.safe.ru' + \
                                                     product_soup.find(class_='card-slide__img-inner')['href']
            except Exception:
                all_data[IE_NAME]['IE_DETAIL_PICTURE'] = ''
            try:
                if name in ['avtomaticheskie-sistemy-khraneniya', 'drugaya-produktsiya']:
                    for img in product_soup.find_all(class_='card-slider__nav-slide'):
                        link = 'https://www.safe.ru' + img.find('img')['src']
                        if 'resize_cache' in link:
                            pure_link = link.split('/')
                            del pure_link[-2]
                            del pure_link[-4]
                            link = '/'.join(pure_link)
                        all_data[IE_NAME]['all_photo'].append(link)
                else:
                    for img in product_soup.find_all(class_='card-slider__nav-slide')[:-1]:
                        link = 'https://www.safe.ru' + img.find('img')['src']
                        if 'resize_cache' in link:
                            pure_link = link.split('/')
                            del pure_link[-2]
                            del pure_link[-4]
                            link = '/'.join(pure_link)
                        all_data[IE_NAME]['all_photo'].append(link)
            except Exception:
                pass
            try:
                all_data[IE_NAME]['IE_DETAIL_TEXT'] = ''.join(
                    filter(None, map(unicode.strip, str(product_soup.find_all(class_='text-block')[0]).splitlines())))
            except Exception:
                all_data[IE_NAME]['IE_DETAIL_TEXT'] = ''
            for ipr in product_soup.find('table', {'id': 'table1'}).find_all('tr'):
                if 'Размеры внешние, мм (ВхШхГ)' in ipr.find_all('td')[0].text:
                    IP_PROP_LIST['Высота, мм'] = "IP_PROP71"
                    IP_PROP_LIST['Ширина, мм'] = "IP_PROP72"
                    IP_PROP_LIST['Глубина, мм'] = "IP_PROP73"
                    IP_PROP_ALL['Высота, мм'] = "IP_PROP71"
                    IP_PROP_ALL['Ширина, мм'] = "IP_PROP72"
                    IP_PROP_ALL['Глубина, мм'] = "IP_PROP73"
                    if ipr.find_all('td')[1].text == '-x-x-':
                        all_data[IE_NAME][IP_PROP_LIST['Высота, мм']] = ''
                        all_data[IE_NAME][IP_PROP_LIST['Ширина, мм']] = ''
                        all_data[IE_NAME][IP_PROP_LIST['Глубина, мм']] = ''
                    else:
                        all_data[IE_NAME][IP_PROP_LIST['Высота, мм']] = ipr.find_all('td')[1].text.split('x')[0]
                        all_data[IE_NAME][IP_PROP_LIST['Ширина, мм']] = ipr.find_all('td')[1].text.split('x')[1]
                        all_data[IE_NAME][IP_PROP_LIST['Глубина, мм']] = ipr.find_all('td')[1].text.split('x')[2]
                elif ipr.find_all('td')[0].text[:-1] in IP_PROP_ALL.keys():
                    if ipr.find_all('td')[1].text == '-':
                        continue
                    elif ipr.find_all('td')[1].text[:len(ipr.find_all('td')[1].text)//2] == ipr.find_all('td')[1].text[len(ipr.find_all('td')[1].text)//2:]:
                        IP_PROP_LIST[ipr.find_all('td')[0].text[:-1]] = IP_PROP_ALL[ipr.find_all('td')[0].text[:-1]]
                        all_data[IE_NAME][IP_PROP_ALL[ipr.find_all('td')[0].text[:-1]]] = ipr.find_all('td')[1].text[:len(ipr.find_all('td')[1].text)//2]
                    else:
                        IP_PROP_LIST[ipr.find_all('td')[0].text[:-1]] = IP_PROP_ALL[ipr.find_all('td')[0].text[:-1]]
                        all_data[IE_NAME][IP_PROP_ALL[ipr.find_all('td')[0].text[:-1]]] = ipr.find_all('td')[1].text
                else:
                    IP_PROP_LIST[ipr.find_all('td')[0].text[:-1]] = f"IP_PROP{IP_PROP}"
                    IP_PROP_ALL[ipr.find_all('td')[0].text[:-1]] = f"IP_PROP{IP_PROP}"
                    IP_PROP += 1
                    if ipr.find_all('td')[1].text[:len(ipr.find_all('td')[1].text)//2] == ipr.find_all('td')[1].text[len(ipr.find_all('td')[1].text)//2:]:
                        all_data[IE_NAME][IP_PROP_ALL[ipr.find_all('td')[0].text[:-1]]] = ipr.find_all('td')[1].text[:len(ipr.find_all('td')[1].text)//2]
                    else:
                        all_data[IE_NAME][IP_PROP_LIST[ipr.find_all('td')[0].text[:-1]]] = ipr.find_all('td')[1].text
            try:
                for ipr in product_soup.find_all(class_='text-block')[1].find_all('a'):
                    all_data[IE_NAME]['documents'].append('https://yarskmebel.tmweb.ru/upload/docs/' + ipr.text + ' ' + IE_NAME + '.pdf')
                    with open(f"data/documents/documents.csv", "a", encoding='windows-1251', newline='') as file:
                        writer = csv.writer(file, delimiter=';')
                        table_doc = (all_data[IE_NAME]['IE_XML_ID'], all_data[IE_NAME]['IE_NAME'], f'{ipr.text} {IE_NAME}.pdf', f'https://www.safe.ru{ipr["href"]}')
                        writer.writerow(table_doc)
            except IndexError:
                all_data[IE_NAME]['documents'].append('')
            except UnicodeEncodeError:
                pass
            try:
                for gr in product_soup.find_all('li', class_='b-breadcrumbs-item')[:-1]:
                    gri = ''.join(filter(None, map(unicode.strip, gr.text.splitlines())))
                    all_data[IE_NAME]['IC_GROUP_LIST'].append(gri)
                    IC_GROUP += 1
            except Exception:
                pass
            IC_GROUP_COUNT = max(IC_GROUP_COUNT, IC_GROUP)
            #time.sleep(1 + random.random())

    with open(f"data/{name}.csv", "w", encoding='windows-1251', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        header_table = tuple(
            ['IE_XML_ID', 'IE_NAME', 'IE_PREVIEW_PICTURE', 'IE_PREVIEW_TEXT', 'IE_PREVIEW_TEXT_TYPE', 'IE_CODE',
             'IE_DETAIL_TEXT_TYPE', 'IE_DETAIL_PICTURE', 'IE_DETAIL_TEXT'] + IP_PROP_1 + list(IP_PROP_LIST.values()) + [
                f"IC_GROUP{u}" for u in range(IC_GROUP_COUNT)] + ['CV_PRICE_1', 'CV_CURRENCY_1'])
        writer.writerow(header_table)
    with open(f"data/{name}.csv", "a", encoding='windows-1251', newline='') as file:
        for key, item in all_data.items():
            for img in item['all_photo']:
                for doc in item['documents']:
                    try:
                        table_list = [item['IE_XML_ID'], item['IE_NAME'], item['IE_PREVIEW_PICTURE'],
                                      item['IE_PREVIEW_TEXT'],
                                      item['IE_PREVIEW_TEXT_TYPE'], item['IE_CODE'], item['IE_DETAIL_TEXT_TYPE'],
                                      item['IE_DETAIL_PICTURE'], item['IE_DETAIL_TEXT'], img, doc]
                        for ip in IP_PROP_LIST.values():
                            if ip in item.keys():
                                table_list.append(item[ip])
                            else:
                                table_list.append('')
                        for n in range(IC_GROUP_COUNT):
                            if n < len(item['IC_GROUP_LIST']):
                                table_list.append(item['IC_GROUP_LIST'][n])
                            else:
                                table_list.append('')
                        table_list.append(item['CV_PRICE_1'])
                        table_list.append(item['CV_CURRENCY_1'])
                        writer = csv.writer(file, delimiter=';')
                        writer.writerow(tuple(table_list))
                    except UnicodeEncodeError:
                        pass


parser('metallicheskaya-mebel', 11)
time.sleep(2)
parser('seyfy', 25)
time.sleep(2)
parser('meditsinskaya-mebel-i-oborudovanie', 8)
time.sleep(2)
parser('metallicheskie-stellazhi', 15)
time.sleep(2)
parser('proizvodstvennaya-mebel', 18)
time.sleep(2)
parser('avtomaticheskie-sistemy-khraneniya', 2)
time.sleep(2)
parser('drugaya-produktsiya', 4)
time.sleep(2)
parser('ofisnaya-mebel', 6)
time.sleep(2)




for key, value in IP_PROP_ALL.items():
    print(f'"{key}": "{value}",')
print('\n\n')

for key, value in IP_PROP_ALL.items():
    print(f'{value}    {key}')
