# -*- coding: utf-8 -*-
import requests, csv
from bs4 import BeautifulSoup
from lxml.builder import unicode
from transliterate import translit
import time
from requests.exceptions import ConnectionError

#IP_PROP_IMG = 59
#IP_PROP_1 = [f'IP_PROP{IP_PROP_IMG}']
#IP_PROP_DOC = 64
#IP_PROP_1 += [f'IP_PROP{IP_PROP_DOC}']
IP_PROP = 330
IE_XML_ID = 3374
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
    "Комплектация": "IP_PROP324",
    "Cрок службы": "IP_PROP325",
    "Толщина полки-фанеры": "IP_PROP326",
    "Ребро жесткости позволяет увеличить максимальную нагрузку на полку МС": "IP_PROP327",
    "В инструментальный шкаф можно установить": "IP_PROP328",
    "Навеcные элементы": "IP_PROP329",
}
ALL_PRODUCTS = set()


request = requests.get('https://assum.ru/nejtralnoe-oborudovanie/')
src = request.text
soup = BeautifulSoup(src, "lxml")

for url in soup.find(class_='content').find_all(class_='ult-content-box-anchor'):
    if 'https://assum.ru' in url['href']:
        fullurl = url['href']
    else:
        fullurl = 'https://assum.ru' + url['href']
    name = fullurl.split('/')[-2]
    request = requests.get(fullurl)
    src = request.text
    soup = BeautifulSoup(src, "lxml")
    all_data = []
    IC_GROUP_COUNT = 0
    IP_PROP_LIST = {}
    IP_PROP_LIST_PROPOSAL = {}
    for line in soup.find_all(class_='vc_row'):
        for product in line.find_all(class_='wpb_column'):
            try:
                if 'https://assum.ru' in product.find(class_='ult-content-box-anchor')['href']:
                    url_product = product.find(class_='ult-content-box-anchor')['href']
                else:
                    url_product = 'https://assum.ru' + product.find(class_='ult-content-box-anchor')['href']
            except Exception:
                continue
            product_request = requests.get(url_product)
            product_src = product_request.text
            product_soup = BeautifulSoup(product_src, "lxml")
            if not product_soup.find_all(class_='assum_modification__product_block'):
                continue
            item_data = {}
            item_data['IE_XML_ID'] = IE_XML_ID
            IE_XML_ID += 1
            item_data['IE_NAME'] = ''
            try:
                item_data['IE_PREVIEW_PICTURE'] = product.find('img')['src']
            except Exception:
                item_data['IE_PREVIEW_PICTURE'] = ''
            item_data['IE_PREVIEW_TEXT'] = ''
            item_data['IE_PREVIEW_TEXT_TYPE'] = 'html'
            item_data['IE_CODE'] = ''
            #item_data['IE_CODE'] = url_product.split('/')[-2]
            item_data['IE_DETAIL_TEXT_TYPE'] = 'html'
            try:
                item_data['IE_DETAIL_TEXT'] = product_soup.find_all(class_='wpb_wrapper')[2].find('p').text
            except Exception:
                item_data['IE_DETAIL_TEXT']= ''
            item_data['CV_PRICE_1'] = ''
            item_data['CV_CURRENCY_1'] = 'RUB'
            try:
                item_data['IE_DETAIL_PICTURE'] = item_data['IE_PREVIEW_PICTURE']
            except Exception:
                item_data['IE_DETAIL_PICTURE'] = ''
            item_ipr = set()
            try:
                for ipr in product_soup.find('table').find_all('tr'):
                    description_name = ipr.find('th').text.strip()
                    description_text = ipr.find('td').text.strip()
                    if 'Вес' in description_name:
                        continue
                    if description_name in IP_PROP_ALL.keys():
                        IP_PROP_LIST[description_name] = IP_PROP_ALL[description_name]
                        item_data[IP_PROP_LIST[description_name]] = description_text
                        item_ipr.add(description_name)
                    else:
                        IP_PROP_ALL[description_name] = f'IP_PROP{IP_PROP}'
                        IP_PROP += 1
                        IP_PROP_LIST[description_name] = IP_PROP_ALL[description_name]
                        item_data[IP_PROP_LIST[description_name]] = description_text
                        item_ipr.add(description_name)
            except Exception:
                pass
            try:
                item_data['IC_GROUP_LIST'] = [i.text for i in product_soup.find(class_='breadcrumbs text-small').find_all('li')[1:-1]] + [product_soup.find(class_='page-title-head').text]
                IC_GROUP_COUNT = max(len(item_data['IC_GROUP_LIST']), IC_GROUP_COUNT)
            except Exception as ex:
                item_data['IC_GROUP_LIST'] = []
            item_data['proposals'] = []
            for proposal in product_soup.find_all(class_='assum_modification__product_block'):
                proposal_data = {}
                proposal_info = proposal.find(class_='assum_modification__info_block')
                proposal_url = proposal_info.find('a')['href']
                proposal_data['IE_XML_ID'] = IE_XML_ID
                IE_XML_ID += 1
                sizes = proposal_info.find_all('div')[1].text.split(')')[-1].split('×')
                IP_PROP_LIST_PROPOSAL['IE_XML_ID товара'] = 'IP_PROP91'
                IP_PROP_LIST_PROPOSAL['Товарное предложение'] = 'IP_PROP90'
                proposal_data['IP_PROP91'] = item_data['IE_XML_ID']
                proposal_data['IP_PROP90'] = ''
                try:
                    proposal_data['IP_PROP71'] = sizes[2].strip()
                    IP_PROP_LIST_PROPOSAL['Высота, мм'] = IP_PROP_ALL['Высота, мм']
                    proposal_data['IP_PROP90'] += 'heigh'+ proposal_data['IP_PROP71']
                except IndexError:
                    proposal_data['IP_PROP71'] = ''
                    IP_PROP_LIST_PROPOSAL['Высота, мм'] = IP_PROP_ALL['Высота, мм']
                try:
                    proposal_data['IP_PROP72'] = sizes[1].strip()
                    IP_PROP_LIST_PROPOSAL['Ширина, мм'] = IP_PROP_ALL['Ширина, мм']
                    proposal_data['IP_PROP90'] += 'width' + proposal_data['IP_PROP72']
                except IndexError:
                    proposal_data['IP_PROP72'] = ''
                    IP_PROP_LIST_PROPOSAL['Ширина, мм'] = IP_PROP_ALL['Ширина, мм']
                try:
                    proposal_data['IP_PROP73'] = sizes[0].strip()
                    IP_PROP_LIST_PROPOSAL['Глубина, мм'] = IP_PROP_ALL['Глубина, мм']
                    proposal_data['IP_PROP90'] += 'depth' + proposal_data['IP_PROP73']
                except IndexError:
                    proposal_data['IP_PROP73'] = ''
                    IP_PROP_LIST_PROPOSAL['Глубина, мм'] = IP_PROP_ALL['Глубина, мм']
                try:
                    proposal_data['CV_PRICE_1'] = proposal_info.find_all('div')[2].text.split('ь')[-1].replace('₽', '').strip()
                except Exception:
                    proposal_data['CV_PRICE_1'] = ''
                proposal_request = requests.get(proposal_url)
                proposal_src = proposal_request.text
                proposal_soup = BeautifulSoup(proposal_src, 'lxml')
                proposal_data['IE_NAME'] = proposal_soup.find(class_='page-title-head').text
                proposal_data['IE_CODE'] = proposal_url.split('/')[-2]
                try:
                    for ipr in proposal_soup.find('table').find_all('tr'):
                        description_name = ipr.find('th').text.strip()
                        description_text = ipr.find('td').text.strip()
                        if 'Размер конструкции' in description_name or description_name in item_ipr:
                            continue
                        if description_name in IP_PROP_ALL.keys():
                            IP_PROP_LIST_PROPOSAL[description_name] = IP_PROP_ALL[description_name]
                            proposal_data[IP_PROP_LIST_PROPOSAL[description_name]] = description_text
                        else:
                            IP_PROP_ALL[description_name] = f'IP_PROP{IP_PROP}'
                            IP_PROP += 1
                            IP_PROP_LIST_PROPOSAL[description_name] = IP_PROP_ALL[description_name]
                            proposal_data[IP_PROP_LIST_PROPOSAL[description_name]] = description_text
                except Exception:
                    pass
                item_data['proposals'].append(proposal_data)
            all_data.append(item_data)
            print(product_soup.find(class_='page-title-head').text)
            print(url_product)
            print('\n')

    with open(f"data assum/products/{name}.csv", "w", encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        header_table = tuple(
            ['IE_XML_ID', 'IE_NAME', 'IE_PREVIEW_PICTURE', 'IE_PREVIEW_TEXT', 'IE_PREVIEW_TEXT_TYPE', 'IE_CODE',
             'IE_DETAIL_TEXT_TYPE', 'IE_DETAIL_PICTURE', 'IE_DETAIL_TEXT'] + list(IP_PROP_LIST.values()) + [
                f"IC_GROUP{u}" for u in range(IC_GROUP_COUNT)] + ['CV_PRICE_1', 'CV_CURRENCY_1'])
        writer.writerow(header_table)
    with open(f"data assum/products/{name}.csv", "a", encoding='utf-8', newline='') as file:
        for item in all_data:
            try:
                table_list = [item['IE_XML_ID'], item['IE_NAME'], item['IE_PREVIEW_PICTURE'],
                              item['IE_PREVIEW_TEXT'],
                              item['IE_PREVIEW_TEXT_TYPE'], item['IE_CODE'], item['IE_DETAIL_TEXT_TYPE'],
                              item['IE_DETAIL_PICTURE'], item['IE_DETAIL_TEXT']]
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
            except UnicodeEncodeError as ex:
                print(ex)
    with open(f"data assum/proposals/{name}_proposal.csv", "w", encoding='utf-8',
              newline='') as file:
        writer = csv.writer(file, delimiter=';')
        header_table = tuple(
            ['IE_XML_ID', 'IE_NAME', 'IE_CODE'] + list(IP_PROP_LIST_PROPOSAL.values()) + ['CV_PRICE_1'])
        writer.writerow(header_table)
    with open(f"data assum/proposals/{name}_proposal.csv", "a", encoding='utf-8',
              newline='') as file:
        for product in all_data:
            for item in product['proposals']:
                try:
                    table_list = [item['IE_XML_ID'], item['IE_NAME'], item['IE_CODE']]
                    for ip in IP_PROP_LIST_PROPOSAL.values():
                        if ip in item.keys():
                            table_list.append(item[ip])
                        else:
                            table_list.append('')
                    table_list.append(item['CV_PRICE_1'])
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(tuple(table_list))
                except UnicodeEncodeError:
                    print('UNICO')

for key, value in IP_PROP_ALL.items():
    print(f'"{key}": "{value}",')
print('\n\n')

for key, value in IP_PROP_ALL.items():
   print(f'{value}    {key}')
