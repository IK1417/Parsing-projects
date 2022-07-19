import requests, csv
from bs4 import BeautifulSoup
from lxml.builder import unicode
from transliterate import translit
import time
from requests.exceptions import ConnectionError

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
    "IE_XML_ID товара": "IP_PROP91",
}
ALL_PRODUCTS = set()



def parser(url, picture, proposal):
    global IP_PROP_IMG, IP_PROP_1, IP_PROP, IE_XML_ID, IP_PROP_ALL, IP_PROP_LIST, IC_GROUP_LIST
    request = requests.get(url)
    print(request.encoding)
    src = request.text
    soup = BeautifulSoup(src, "lxml")
    ALL_DATA = {}

    ALL_DATA['IE_XML_ID'] = IE_XML_ID
    IE_XML_ID += 1
    ALL_DATA['IE_PREVIEW_PICTURE'] = picture
    ALL_DATA['IE_PREVIEW_TEXT'] = ''
    ALL_DATA['IE_PREVIEW_TEXT_TYPE'] = 'html'
    ALL_DATA['IE_DETAIL_TEXT_TYPE'] = 'html'
    ALL_DATA['CV_CURRENCY_1'] = 'RUB'
    ALL_DATA['documents'] = {}
    ALL_DATA['all_photo'] = []
    ALL_DATA['IC_GROUP_LIST'] = IC_GROUP_LIST
    try:
        ALL_DATA['all_photo'] += [i.find('img')['src'] for i in
                                  soup.find(class_='swiper-wrapper').find_all(class_='swiper-slide')]
        ALL_DATA['IE_DETAIL_PICTURE'] = ALL_DATA['all_photo'][0]
        del ALL_DATA['all_photo'][0]
    except Exception:
        ALL_DATA['all_photo'] = ['']
        ALL_DATA['IE_DETAIL_PICTURE'] = ''
    try:
        ALL_DATA['IE_DETAIL_TEXT'] = ''.join(filter(None, map(unicode.strip, str(soup.find(class_='full-description').find('p')).splitlines())))
    except Exception:
        ALL_DATA['IE_DETAIL_TEXT'] = ''
    try:
        for doc in soup.find(class_='instructions__grid-wrap').find_all(class_='instructions__col instructions__dowload-file'):
            ALL_DATA['documents'][doc.find('span').text] = 'https://paksmet.ru' + doc.find('a')['href']
    except Exception:
        pass
    if proposal:
        ALL_DATA['CV_PRICE_1'] = ''
        ALL_DATA['IE_NAME'] = ''
        ALL_DATA['proposal'] = []
        ALL_DATA['IE_CODE'] = ''
        if not soup.find(class_='product-attributes') is None:
            link_proposal = False
            all_name = [str(item.find(class_='name').find('h3').text).replace('Для', '').strip() for item in soup.find(class_='product-attributes').find_all(class_='item')]
            try:
                for p in soup.find(class_='field_content').find_all('p'):
                    description = p.text
                    if not ':' in p.find('span').text or p.text == p.find('span').text:
                        continue
                    description_name, description_text = description.split(':')[0], description.split(':')[1]
                    nameindesc = False
                    for i in all_name:
                        if i in description_name:
                            nameindesc = True
                    if not ('азмер' in description_name or nameindesc or (IC_GROUP_LIST[0] in ['Металлические стеллажи', 'Верстаки и Инструментальные шкафы'] and 'омплектаци' in description_name)):
                        if description_name in IP_PROP_ALL.keys():
                            IP_PROP_LIST[description_name] = IP_PROP_ALL[description_name]
                            ALL_DATA[IP_PROP_ALL[description_name]] = description_text.strip()
                        else:
                            IP_PROP_ALL[description_name] = f"IP_PROP{IP_PROP}"
                            IP_PROP += 1
                            IP_PROP_LIST[description_name] = IP_PROP_ALL[description_name]
                            ALL_DATA[IP_PROP_ALL[description_name]] = description_text.strip()
            except Exception:
                pass
            try:
                if soup.find(class_='name').find('h3').find('a'):
                    link_proposal = True
            except Exception:
                pass
            if link_proposal:
                for item in soup.find(class_='product-attributes').find_all(class_='item'):
                    item_dict = {}
                    item_dict['IE_XML_ID'] = IE_XML_ID
                    IE_XML_ID += 1
                    IE_SUBNAME = str(item.find(class_='name').find('h3').text).replace('Для ', '').strip()
                    item_url = 'https://paksmet.ru' + item.find('a')['href']
                    try:
                        item_request = requests.get(item_url)
                        item_src = item_request.text
                        item_soup = BeautifulSoup(item_src, 'lxml')
                    except ConnectionError:
                        print('ConnectionError')
                        continue
                    item_dict['IE_NAME'] = ''.join(filter(None, map(unicode.strip, item_soup.find(class_='card-product__title').text.splitlines())))
                    item_dict['IE_CODE'] = translit(item_dict['IE_NAME'], language_code='ru', reversed=True).replace(' ', '-')
                    try:
                        item_dict['CV_PRICE_1'] = ''.join(
                            filter(None, map(unicode.strip, item_soup.find(class_='price').text.splitlines())))[:-3]
                    except Exception:
                        item_dict['CV_PRICE_1'] = ''
                    item_dict['IP_PROP91'] = ALL_DATA['IE_XML_ID']
                    item_dict['IP_PROP90'] = ''
                    try:
                        for p in item_soup.find(class_='field_content').find_all('p'):
                            description = p.text
                            if not ':' in p.find('span').text or p.text == p.find('span').text:
                                continue
                            description_name, description_text = description.split(':')[0], description.split(':')[1]
                            if 'азмер' in description_name:
                                if '/' in description_name:
                                    if ALL_DATA['IE_XML_ID'] == 2689:
                                        description_text = [i.strip() for i in description_text.split('\n') if i.strip() != ''][-1]
                                    for ind in range(len(description_name.split('/'))):
                                        description_name_ind = description_name.split('/')[ind].strip()
                                        description_text_ind = description_text.split('/')[ind].strip()
                                        if 'азмер' in description_name_ind:
                                            try:
                                                item_dict['IP_PROP71'] = \
                                                    description_text_ind.split('x')[0].split('мм')[0].strip().split(' ')[-1]
                                                IP_PROP_LIST_PROPOSAL['Высота, мм'] = 'IP_PROP71'
                                                item_dict['IP_PROP90'] += 'heigh' + item_dict['IP_PROP71']
                                            except Exception:
                                                item_dict['IP_PROP71'] = ''
                                            try:
                                                item_dict['IP_PROP72'] = \
                                                    description_text_ind.split('x')[1].split('мм')[0].strip().split(' ')[-1]
                                                IP_PROP_LIST_PROPOSAL['Ширина, мм'] = 'IP_PROP72'
                                                item_dict['IP_PROP90'] += 'width' + item_dict['IP_PROP72']
                                            except Exception:
                                                item_dict['IP_PROP72'] = ''
                                            try:
                                                item_dict['IP_PROP73'] = \
                                                    description_text_ind.split('x')[2].split('мм')[0].strip().split(' ')[-1]
                                                IP_PROP_LIST_PROPOSAL['Глубина, мм'] = 'IP_PROP73'
                                                item_dict['IP_PROP90'] += 'depth' + item_dict['IP_PROP73']
                                            except Exception:
                                                item_dict['IP_PROP73'] = ''
                                        if 'Вес' in description_name_ind:
                                            item_dict['IP_PROP77'] = description_text_ind.split()[0]
                                            IP_PROP_LIST_PROPOSAL['Вес, кг'] = item_dict['IP_PROP77']
                                else:
                                    try:
                                        item_dict['IP_PROP71'] = \
                                        description_text.split('х')[0].split('мм')[0].strip().split(' ')[-1]
                                        IP_PROP_LIST_PROPOSAL['Высота, мм'] = 'IP_PROP71'
                                        item_dict['IP_PROP90'] += 'heigh' + item_dict['IP_PROP71']
                                    except Exception:
                                        item_dict['IP_PROP71'] = ''
                                    try:
                                        item_dict['IP_PROP72'] = \
                                        description_text.split('х')[1].split('мм')[0].strip().split(' ')[-1]
                                        IP_PROP_LIST_PROPOSAL['Ширина, мм'] = 'IP_PROP72'
                                        item_dict['IP_PROP90'] += 'width' +  item_dict['IP_PROP72']
                                    except Exception:
                                        item_dict['IP_PROP72'] = ''
                                    try:
                                        item_dict['IP_PROP73'] = \
                                        description_text.split('х')[2].split('мм')[0].strip().split(' ')[-1]
                                        IP_PROP_LIST_PROPOSAL['Глубина, мм'] = 'IP_PROP73'
                                        item_dict['IP_PROP90'] += 'depth' + item_dict['IP_PROP73']
                                    except Exception:
                                        item_dict['IP_PROP73'] = ''
                            elif IC_GROUP_LIST[0] in ['Металлические стеллажи', 'Верстаки и Инструментальные шкафы'] and 'омплектаци' in description_name:
                                if description_name in IP_PROP_ALL.keys():
                                    IP_PROP_LIST_PROPOSAL[description_name] = IP_PROP_ALL[description_name]
                                    ALL_DATA[IP_PROP_ALL[description_name]] = description_text
                                else:
                                    IP_PROP_ALL[description_name] = f"IP_PROP{IP_PROP}"
                                    IP_PROP += 1
                                    IP_PROP_LIST[description_name] = IP_PROP_ALL[description_name]
                                    ALL_DATA[IP_PROP_ALL[description_name]] = description_text
                    except Exception:
                        pass
                    ALL_DATA["proposal"].append(item_dict)
            else:
                for item in soup.find(class_='product-attributes').find_all(class_='item'):
                    item_dict = {}
                    item_dict['IE_XML_ID'] = IE_XML_ID
                    IE_XML_ID += 1
                    try:
                        IE_NAME = ''.join(filter(None, map(unicode.strip, soup.find(class_='card-product__title').text.splitlines())))
                        IE_SUBNAME = str(item.find(class_='name').find('h3').text).strip()
                        IE_NAME += ' ' + IE_SUBNAME
                        item_dict['IE_NAME'] = IE_NAME
                        IE_SUBNAME = IE_SUBNAME.replace('Для ', '')
                    except AttributeError as ex:
                        item_dict['IE_NAME'] = ''
                    item_dict['IP_PROP90'] = ''
                    try:
                        item_dict['IP_PROP71'] = item.find(class_='name').find(class_='size').text.split('х')[0].split('мм')[0].strip().split(' ')[-1]
                        IP_PROP_LIST['Высота, мм'] = 'IP_PROP71'
                        item_dict['IP_PROP90'] += 'heigh' + item_dict['IP_PROP71']
                    except AttributeError:
                        try:
                            item_dict['IP_PROP71'] = item.find(class_='name').find('h3').text.split('х')[0].split('мм')[0].strip().split(' ')[-1]
                            IP_PROP_LIST['Высота, мм'] = 'IP_PROP71'
                            item_dict['IP_PROP90'] += 'heigh' + item_dict['IP_PROP71']
                        except Exception as ex:
                            print(item.find(class_='name'))
                            item_dict['IP_PROP71'] = ''
                    try:
                        item_dict['IP_PROP72'] = item.find(class_='name').find(class_='size').text.split('х')[1].split('мм')[0].strip().split(' ')[-1]
                        IP_PROP_LIST['Ширина, мм'] = 'IP_PROP72'
                        item_dict['IP_PROP90'] += 'width' + item_dict['IP_PROP72']
                    except AttributeError:
                        try:
                            item_dict['IP_PROP72'] = \
                            item.find(class_='name').find('h3').text.split('х')[1].split('мм')[0].strip().split(' ')[-1]
                            IP_PROP_LIST['Ширина, мм'] = 'IP_PROP72'
                            item_dict['IP_PROP90'] += 'width' + item_dict['IP_PROP72']
                        except Exception as ex:
                            item_dict['IP_PROP72'] = ''
                    try:
                        item_dict['IP_PROP73'] = item.find(class_='name').find(class_='size').text.split('х')[2].split('мм')[0].strip().split(' ')[-1]
                        IP_PROP_LIST['Глубина, мм'] = 'IP_PROP73'
                        item_dict['IP_PROP90'] += 'depth' + item_dict['IP_PROP73']
                    except AttributeError:
                        try:
                            item_dict['IP_PROP73'] = \
                            item.find(class_='name').find('h3').text.split('х')[2].split('мм')[0].strip().split(
                                ' ')[-1]
                            IP_PROP_LIST['Глубина, мм'] = 'IP_PROP73'
                            item_dict['IP_PROP90'] += 'depth' + item_dict['IP_PROP73']
                        except Exception as ex:
                            item_dict['IP_PROP73'] = ''
                    item_dict['IE_CODE'] = translit(item_dict['IE_NAME'], language_code='ru', reversed=True).replace(' ', '-')
                    try:
                        item_dict['CV_PRICE_1'] = item.find(class_='price').text.split('р.')[0].strip()
                    except Exception:
                        item_dict['CV_PRICE_1'] = ''
                    item_dict['IP_PROP91'] = ALL_DATA['IE_XML_ID']
                    ALL_DATA["proposal"].append(item_dict)
        else:
            item_dict = {}
            item_dict['IE_XML_ID'] = IE_XML_ID
            IE_XML_ID += 1
            item_dict['IE_NAME'] = ''.join(filter(None, map(unicode.strip, soup.find(class_='card-product__title').text.splitlines())))
            item_dict['IE_CODE'] = translit(item_dict['IE_NAME'], language_code='ru', reversed=True).replace(' ', '-')
            try:
                item_dict['CV_PRICE_1'] = ''.join(
                    filter(None, map(unicode.strip, soup.find(class_='price').text.splitlines())))[:-3]
            except Exception:
                item_dict['CV_PRICE_1'] = ''
            item_dict['IP_PROP91'] = ALL_DATA['IE_XML_ID']
            ALL_DATA["proposal"].append(item_dict)
    else:
        ALL_DATA['IE_NAME'] = ''.join(filter(None, map(unicode.strip, soup.find(class_='card-product__title').text.splitlines())))
        ALL_DATA['IE_CODE'] = translit(ALL_DATA['IE_NAME'], language_code='ru', reversed=True).replace(' ', '-')
        try:
            ALL_DATA['CV_PRICE_1'] = ''.join(filter(None, map(unicode.strip, soup.find(class_='price').text.splitlines())))[:-3]
        except Exception:
            ALL_DATA['CV_PRICE_1'] = ''
        for p in soup.find(class_='field_content').find_all('p'):
            description = p.text
            if not ':' in p.find('span').text or p.text == p.find('span').text:
                continue
            description_name, description_text = description.split(':')[0], description.split(':')[1]
            if not 'азмер' in description_name:
                if description_name in IP_PROP_ALL.keys():
                    IP_PROP_LIST[description_name] = IP_PROP_ALL[description_name]
                    ALL_DATA[IP_PROP_ALL[description_name]] = description_text
                else:
                    IP_PROP_ALL[description_name] = f"IP_PROP{IP_PROP}"
                    IP_PROP += 1
                    IP_PROP_LIST[description_name] = IP_PROP_ALL[description_name]
                    ALL_DATA[IP_PROP_ALL[description_name]] = description_text
            elif 'азмер' in description_name:
                try:
                    ALL_DATA['IP_PROP71'] = description_text.split('х')[0].split('мм')[0].strip().split(' ')[-1]
                    IP_PROP_LIST['Высота, мм'] = ALL_DATA['IP_PROP71']
                except Exception as ex:
                    print(ex)
                    ALL_DATA['IP_PROP71'] = ''
                try:
                    ALL_DATA['IP_PROP72'] = description_text.split('х')[1].split('мм')[0].strip().split(' ')[-1]
                    IP_PROP_LIST['Ширина, мм'] = ALL_DATA['IP_PROP72']
                except Exception:
                    ALL_DATA['IP_PROP72'] = ''
                try:
                    ALL_DATA['IP_PROP73'] = description_text.split('х')[2].split('мм')[0].strip().split(' ')[-1]
                    IP_PROP_LIST['Глубина, мм'] = ALL_DATA['IP_PROP73']
                except Exception:
                    ALL_DATA['IP_PROP73'] = ''

    print(ALL_DATA)
    return [ALL_DATA['IE_NAME'], ALL_DATA]


request = requests.get('https://paksmet.ru/produktsiya')
src = request.text
soup = BeautifulSoup(src, "lxml")
for name in soup.find(class_='products-list').find_all('li')[5:6]:
    print(name.find('span').text, 'https://paksmet.ru' + name.find('a')['href'] + '\n')
    proposal = True
    if name.find('span').text in ['Картотечные шкафы', 'Сейфы', 'Бухгалтерские шкафы']:
        proposal = False
    main_url = 'https://paksmet.ru' + name.find('a')['href']
    IC_GROUP_LIST = [name.find('span').text]
    all_data = {}
    IP_PROP_LIST = {}
    IP_PROP_LIST_PROPOSAL = {}
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
                    IE_NAME, IE_DATA = parser(
                        'https://paksmet.ru' + item.find(class_='product-header').find('a')['href'], PREVIEW_PICTURE,
                        proposal)
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
                                PREVIEW_PICTURE, proposal)
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
                                          PREVIEW_PICTURE, proposal)
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
                            PREVIEW_PICTURE, proposal)
                        print('https://paksmet.ru' + item.find(class_='product-header').find('a')['href'])
                IC_GROUP_LIST.pop()
        except Exception:
            pass
# with open(f"data davita/{name}.csv", "w", encoding='windows-1251', newline='') as file:
#    writer = csv.writer(file, delimiter=';')
#    header_table = tuple(
#        ['IE_XML_ID', 'IE_NAME', 'IE_PREVIEW_PICTURE', 'IE_PREVIEW_TEXT', 'IE_PREVIEW_TEXT_TYPE', 'IE_CODE',
#         'IE_DETAIL_TEXT_TYPE', 'IE_DETAIL_PICTURE', 'IE_DETAIL_TEXT'] + IP_PROP_1 + list(IP_PROP_LIST.values()) + [
#            f"IC_GROUP{u}" for u in range(IC_GROUP_COUNT)] + ['CV_PRICE_1', 'CV_CURRENCY_1'])
#    writer.writerow(header_table)
# with open(f"data davita/{name}.csv", "a", encoding='windows-1251', newline='') as file:
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
# print(IE_XML_ID - 1905)
# for key, value in IP_PROP_ALL.items():
#    print(f'"{key}": "{value}",')
# print('\n\n')
#
# for key, value in IP_PROP_ALL.items():
#    print(f'{value}    {key}')
