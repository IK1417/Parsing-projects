import requests, csv
from bs4 import BeautifulSoup
from lxml.builder import unicode
from transliterate import translit
import time
import random


IP_PROP_IMG = 59
IP_PROP_1 = [f'IP_PROP{IP_PROP_IMG}']
IP_PROP_DOC = 64
IP_PROP_1 += [f'IP_PROP{IP_PROP_DOC}']
IP_PROP = 324
IE_XML_ID = 2655
IP_PROP_ALL = {
    "Размеры внутренние, мм (ВхШхГ)": "IP_PROP76",
    "Вес, кг": "IP_PROP77",
    "Объём, л": "IP_PROP75",
    "Количество полок": "IP_PROP79",
    "Тип замка": "IP_PROP80",
    "Цвет": "IP_PROP81",
    "Тип покрытия": "IP_PROP82",
    "Гарантия": "IP_PROP83",
    "Производитель": "IP_PROP74",
    "Страна": "IP_PROP265",
    "Размеры трейзера, мм (ВхШхГ)": "IP_PROP266",
    "Количество ящиков": "IP_PROP267",
    "Максимальная нагрузка на ящик, кг": "IP_PROP268",
    "Формат документов": "IP_PROP269",
    "Внутренние размеры ящика, мм (ВхШхГ)": "IP_PROP270",
    "Максимальная нагрузка на полку, кг": "IP_PROP271",
    "Вместимость, количество папок Корона (75мм)": "IP_PROP272",
    "Количество дверей": "IP_PROP273",
    "Класс огнестойкости": "IP_PROP274",
    "Количество секций": "IP_PROP275",
    "КТРУ": "IP_PROP276",
    "Пример технического задания": "IP_PROP277",
    "Класс взломостойкости": "IP_PROP78",
    "Количество стволов": "IP_PROP278",
    "Максимальная высота ствола, мм": "IP_PROP279",
    "Патронное отделение (трейзер)": "IP_PROP280",
    "Класс оружейных сейфов": "IP_PROP281",
    "Количество ячеек": "IP_PROP282",
    "Количество скважин на ячейку": "IP_PROP283",
    "Внутренние размеры отделений (ВхШхГ), мм": "IP_PROP284",
    "Нагрузка на столешницу": "IP_PROP285",
    "Допустимая нагрузка": "IP_PROP286",
    "Номинальная нагрузка на ложе": "IP_PROP287",
    "Каркас": "IP_PROP288",
    "Обивка": "IP_PROP289",
    "Потребляемая мощность, ВТ": "IP_PROP290",
    "Исполнение": "IP_PROP291",
    "Бактериальная эффективность, %": "IP_PROP292",
    "Наличие фильтра": "IP_PROP293",
    "Количество ламп": "IP_PROP294",
    "Мощность одной лампы, Вт": "IP_PROP295",
    "Срок службы ламп, ч": "IP_PROP296",
    "Длина кабеля питания, м": "IP_PROP297",
    "Электропитание, В/Гц": "IP_PROP298",
    "Наличие заземления": "IP_PROP299",
    "Рекомендуемый объем помещения, м3": "IP_PROP300",
    "Количество ярусов хранения": "IP_PROP301",
    "Максимальная нагрузка": "IP_PROP302",
    "Габаритные размеры с учетом подпятников, мм (ВхШхГ)": "IP_PROP303",
    "Размеры ячейки, мм (ВхШхГ)": "IP_PROP304",
    "Вместимость (количество ключей, шт)": "IP_PROP305",
    "Материал": "IP_PROP306",
    "Механизм": "IP_PROP307",
    "Крестовина": "IP_PROP308",
    "Ролики": "IP_PROP309",
    "Глубина и ширина сиденья, мм": "IP_PROP310",
    "Высота сиденья (min-max), мм": "IP_PROP311",
    "Подлокотники": "IP_PROP312",
    "Полозья": "IP_PROP313",
    "Высота, мм": "IP_PROP71",
    "Ширина, мм": "IP_PROP72",
    "Глубина, мм": "IP_PROP73",
    "Гарантия на замок": "IP_PROP314",
    "Цвет каркаса": "IP_PROP315",
    "Цвет обивки": "IP_PROP316",
    "Производительность, м3/час": "IP_PROP317",
    "Цвет столешницы": "IP_PROP318",
    "Объем, м3": "IP_PROP319",
    "Коллекция": "IP_PROP320",
    "Встроенная тумба": "IP_PROP321",
    "Количество упаковок, шт": "IP_PROP322",
    "Выдвижной ящик под столешницей": "IP_PROP323",
}
ALL_PRODUCTS = set()

def parser(url, picture):
    global IP_PROP_IMG, IP_PROP_1, IP_PROP, IE_XML_ID, IP_PROP_ALL
    request = requests.get(url)
    src = request.text
    soup = BeautifulSoup(src, "lxml")
    ALL_DATA = {}
    ALL_DATA['IE_NAME'] = ''.join(
                    filter(None, map(unicode.strip, soup.find(class_='card-product__title').text.splitlines())))
    ALL_DATA['all_photo'] = []
    ALL_DATA['documents'] = []
    ALL_DATA['IE_XML_ID'] = IE_XML_ID
    IE_XML_ID += 1
    ALL_DATA['IE_PREVIEW_PICTURE'] = picture
    ALL_DATA['IE_PREVIEW_TEXT'] = ''
    ALL_DATA['IE_PREVIEW_TEXT_TYPE'] = 'html'
    ALL_DATA['IE_CODE'] = translit(ALL_DATA['IE_NAME'], language_code='ru', reversed=True).replace(' ', '-')
    ALL_DATA['IE_DETAIL_TEXT_TYPE'] = 'html'
    ALL_DATA['CV_PRICE_1'] = []
    try:
        if not soup.find(class_='product-attributes') is None:
            for product in soup.find(class_='product-attributes').find_all(class_='item'):
                ALL_DATA['CV_PRICE_1'].append(''.join(
                    filter(None, map(unicode.strip, product.find(class_='price').text.splitlines())))[:-3])
        else:
            ALL_DATA['CV_PRICE_1'].append(''.join(
                    filter(None, map(unicode.strip, soup.find(class_='price').text.splitlines())))[:-3])
    except Exception as ex:
        ALL_DATA['CV_PRICE_1'].append('')
    try:
        ALL_DATA['all_photo'] += [i.find('img')['src'] for i in soup.find_all(class_='swiper-slide') if i.find('img')['src'].split('/')[-1].startswith('full')]
    except Exception:
        ALL_DATA['IE_DETAIL_PICTURE'] = ''
    ALL_DATA['CV_CURRENCY_1'] = 'RUB'
    try:
        ALL_DATA['IE_DETAIL_TEXT'] = ''.join(filter(None, map(unicode.strip, str(soup.find(class_='full-description').find('p')).splitlines())))
    except Exception:
        ALL_DATA['IE_DETAIL_TEXT'] = ''
    for doc in soup.find(class_='instructions__grid-wrap').find_all(class_='instructions__col instructions__dowload-file'):
        print('https://paksmet.ru' + doc.find('a')['href'], '    ', doc.find('span').text)
    print(ALL_DATA)
    return ['fg', 'j']


request = requests.get('https://paksmet.ru/produktsiya')
src = request.text
soup = BeautifulSoup(src, "lxml")
for name in soup.find(class_='products-list').find_all('li'):
    print(name.find('span').text, 'https://paksmet.ru' + name.find('a')['href'] + '\n')
    main_url = 'https://paksmet.ru' + name.find('a')['href']
    IC_GROUP_LIST = [name.find('span').text]
    all_data = {}
    IP_PROP_LIST = {}
    IC_GROUP_COUNT = 0
    request = requests.get(main_url)
    src = request.text
    soup = BeautifulSoup(src, "lxml")
    if not soup.find_all(class_='product-item'):
        for page in soup.find(class_='category-list').find_all('a'):
            IC_GROUP_LIST.append(page.find('p').text)
            print(IC_GROUP_LIST)
            url = f'https://paksmet.ru{page["href"]}'
            request = requests.get(url)
            src = request.text
            page_soup = BeautifulSoup(src, "lxml")
            for item in page_soup.find_all(class_='product-item'):
                if not item.find(class_='name').text in ALL_PRODUCTS:
                    ALL_PRODUCTS.add(item.find(class_='name').text)
                    try:
                        PREVIEW_PICTURE = item.find('img')['src']
                    except Exception:
                        PREVIEW_PICTURE = ''
                    IE_NAME, IE_DATA = parser('https://paksmet.ru' + item.find(class_='product-header').find('a')['href'], PREVIEW_PICTURE)
                    all_data[IE_NAME] = IE_DATA
                    print('https://paksmet.ru' + item.find(class_='product-header').find('a')['href'])
            try:
                for sub_page in page_soup.find(class_='category-list').find_all('a'):
                    IC_GROUP_LIST.append(sub_page.find('p').text)
                    print(IC_GROUP_LIST)
                    url = f'https://paksmet.ru{sub_page["href"]}'
                    request = requests.get(url)
                    src = request.text
                    sub_soup = BeautifulSoup(src, "lxml")
                    for item in sub_soup.find_all(class_='product-item'):
                        if not item.find(class_='name').text in ALL_PRODUCTS:
                            ALL_PRODUCTS.add(item.find(class_='name').text)
                            try:
                                PREVIEW_PICTURE = item.find('img')['src']
                            except Exception:
                                PREVIEW_PICTURE = ''
                            IE_NAME, IE_DATA = parser(
                                'https://paksmet.ru' + item.find(class_='product-header').find('a')['href'],
                                PREVIEW_PICTURE)
                            print('https://paksmet.ru' + item.find(class_='product-header').find('a')['href'])
                    IC_GROUP_LIST.pop()
            except Exception:
                pass
            IC_GROUP_LIST.pop()
    else:
        print(IC_GROUP_LIST)
        for item in soup.find_all(class_='product-item'):
            if not item.find(class_='name').text in ALL_PRODUCTS:
                ALL_PRODUCTS.add(item.find(class_='name').text)
                try:
                    PREVIEW_PICTURE = item.find('img')['src']
                except Exception:
                    PREVIEW_PICTURE = ''
                IE_NAME, IE_DATA = parser('https://paksmet.ru' + item.find(class_='product-header').find('a')['href'],
                                          PREVIEW_PICTURE)
                print('https://paksmet.ru' + item.find(class_='product-header').find('a')['href'])
        try:
            for sub_page in soup.find(class_='category-list').find_all('a'):
                IC_GROUP_LIST.append(sub_page.find('p').text)
                print(IC_GROUP_LIST)
                url = f'https://paksmet.ru{sub_page["href"]}'
                request = requests.get(url)
                src = request.text
                sub_soup = BeautifulSoup(src, "lxml")
                for item in sub_soup.find_all(class_='product-item'):
                    if not item.find(class_='name').text in ALL_PRODUCTS:
                        ALL_PRODUCTS.add(item.find(class_='name').text)
                        try:
                            PREVIEW_PICTURE = item.find('img')['src']
                        except Exception:
                            PREVIEW_PICTURE = ''
                        IE_NAME, IE_DATA = parser(
                            'https://paksmet.ru' + item.find(class_='product-header').find('a')['href'],
                            PREVIEW_PICTURE)
                        print('https://paksmet.ru' + item.find(class_='product-header').find('a')['href'])
                IC_GROUP_LIST.pop()
        except Exception:
            pass

    #        try:
    #            all_data[IE_NAME]['IE_DETAIL_PICTURE'] = 'https://davitamebel.ru' + \
    #                                                 product_soup.find('img', class_='big-photo')['src']
    #        except Exception:
    #            all_data[IE_NAME]['IE_DETAIL_PICTURE'] = ''
    #        try:
    #            for img in product_soup.find(class_='big-photos').find_all('img')[1:]:
    #                all_data[IE_NAME]['all_photo'].append('https://davitamebel.ru' + img['src'])
    #        except Exception:
    #            pass
    #        try:
    #            all_data[IE_NAME]['IE_DETAIL_TEXT'] = ''.join(
    #                filter(None, map(unicode.strip, str(product_soup.find_all(class_='p')[0]).splitlines())))
    #        except Exception:
    #            all_data[IE_NAME]['IE_DETAIL_TEXT'] = ''
    #        for ipr in product_soup.find('table', class_='product-properties').find_all('tr'):
    #            if 'Размеры, мм' in ipr.find_all('td')[0].text:
    #                delimiter = 'x'
    #                if len(ipr.find_all('td')[1].text.split(delimiter)) == 1:
    #                    delimiter = 'х'
    #                try:
    #                    IP_PROP_LIST['Высота, мм'] = "IP_PROP71"
    #                    all_data[IE_NAME][IP_PROP_LIST['Высота, мм']] = ipr.find_all('td')[1].text.split(delimiter)[0]
    #                except Exception:
    #                    pass
    #                try:
    #                    IP_PROP_LIST['Ширина, мм'] = "IP_PROP72"
    #                    all_data[IE_NAME][IP_PROP_LIST['Ширина, мм']] = ipr.find_all('td')[1].text.split(delimiter)[1]
    #                except Exception:
    #                    pass
    #                try:
    #                    IP_PROP_LIST['Глубина, мм'] = "IP_PROP73"
    #                    all_data[IE_NAME][IP_PROP_LIST['Глубина, мм']] = ipr.find_all('td')[1].text.split(delimiter)[2]
    #                except Exception:
    #                    pass
    #            elif 'Срок гарантии, лет' in ipr.find_all('td')[0].text:
    #                IP_PROP_LIST['Гарантия'] = "IP_PROP83"
    #                all_data[IE_NAME][IP_PROP_LIST['Гарантия']] = ipr.find_all('td')[1].text + ' лет'
    #            elif 'Цветовое исполнение' in ipr.find_all('td')[0].text:
    #                IP_PROP_LIST['Цвет'] = IP_PROP_ALL['Цвет']
    #                all_data[IE_NAME][IP_PROP_LIST['Цвет']] = ipr.find_all('td')[1].text
    #            elif ipr.find_all('td')[0].text in IP_PROP_ALL.keys():
    #                IP_PROP_LIST[ipr.find_all('td')[0].text] = IP_PROP_ALL[ipr.find_all('td')[0].text]
    #                all_data[IE_NAME][IP_PROP_ALL[ipr.find_all('td')[0].text]] = ipr.find_all('td')[1].text
    #            else:
    #                IP_PROP_LIST[ipr.find_all('td')[0].text] = f"IP_PROP{IP_PROP}"
    #                IP_PROP_ALL[ipr.find_all('td')[0].text] = f"IP_PROP{IP_PROP}"
    #                IP_PROP += 1
    #                all_data[IE_NAME][IP_PROP_LIST[ipr.find_all('td')[0].text]] = ipr.find_all('td')[1].text
    #        try:
    #            #print(product_soup.find_all('li', class_='breadcrumbs'))
    #            for gr in product_soup.find('ul', class_='breadcrumbs').find_all('li')[:-1]:
    #                gri = ''.join(filter(None, map(unicode.strip, gr.find(class_='text').text.splitlines())))
    #                all_data[IE_NAME]['IC_GROUP_LIST'].append(gri)
    #                IC_GROUP += 1
    #        except Exception:
    #            pass
    #        IC_GROUP_COUNT = max(IC_GROUP_COUNT, IC_GROUP)
    #        #print(all_data[IE_NAME]['CV_PRICE_1'])
#
    #with open(f"data davita/{name}.csv", "w", encoding='windows-1251', newline='') as file:
    #    writer = csv.writer(file, delimiter=';')
    #    header_table = tuple(
    #        ['IE_XML_ID', 'IE_NAME', 'IE_PREVIEW_PICTURE', 'IE_PREVIEW_TEXT', 'IE_PREVIEW_TEXT_TYPE', 'IE_CODE',
    #         'IE_DETAIL_TEXT_TYPE', 'IE_DETAIL_PICTURE', 'IE_DETAIL_TEXT'] + IP_PROP_1 + list(IP_PROP_LIST.values()) + [
    #            f"IC_GROUP{u}" for u in range(IC_GROUP_COUNT)] + ['CV_PRICE_1', 'CV_CURRENCY_1'])
    #    writer.writerow(header_table)
    #with open(f"data davita/{name}.csv", "a", encoding='windows-1251', newline='') as file:
    #    for key, item in all_data.items():
    #        for img in item['all_photo']:
    #            try:
    #                table_list = [item['IE_XML_ID'], item['IE_NAME'], item['IE_PREVIEW_PICTURE'],
    #                              item['IE_PREVIEW_TEXT'],
    #                              item['IE_PREVIEW_TEXT_TYPE'], item['IE_CODE'], item['IE_DETAIL_TEXT_TYPE'],
    #                              item['IE_DETAIL_PICTURE'], item['IE_DETAIL_TEXT'], img]
    #                for ip in IP_PROP_LIST.values():
    #                    if ip in item.keys():
    #                        table_list.append(item[ip])
    #                    else:
    #                        table_list.append('')
    #                for n in range(IC_GROUP_COUNT):
    #                    if n < len(item['IC_GROUP_LIST']):
    #                        table_list.append(item['IC_GROUP_LIST'][n])
    #                    else:
    #                        table_list.append('')
    #                table_list.append(item['CV_PRICE_1'])
    #                table_list.append(item['CV_CURRENCY_1'])
    #                writer = csv.writer(file, delimiter=';')
    #                writer.writerow(tuple(table_list))
    #            except UnicodeEncodeError:
    #                pass
    #print(IE_XML_ID - 1905)

#parser('nabory_ofisnoy_mebeli_1', 5)
#time.sleep(1)
#parser('ofisnye-shkafy', 5)
#time.sleep(1)
#parser('ofisnyj-stol', 6)
#time.sleep(1)
#parser('tumba-ofisnaja', 2)
#time.sleep(1)
#
#
#for key, value in IP_PROP_ALL.items():
#    print(f'"{key}": "{value}",')
#print('\n\n')
#
#for key, value in IP_PROP_ALL.items():
#    print(f'{value}    {key}')