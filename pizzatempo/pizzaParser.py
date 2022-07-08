import requests, csv, json
import pandas as pd
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.2.615 Yowser/2.5 Safari/537.36',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           }
url = 'https://www.pizzatempo.by/menu/pizza.html?action=search&price_from=6.6&price_to=53.7&price_start=6.6&price_end=53.7'

request = requests.get(url, headers=headers)
src = request.text
soup = BeautifulSoup(src, 'lxml')


pizzaDough = ['На тонком тесте', 'С пышным краем']
writer = pd.ExcelWriter('data/all_pizza.xlsx', engine='xlsxwriter')

for group in soup.find_all(class_='previews'):
    for pizza in group.find_all(class_='item'):
        all_pizza_data = {'Фото': [],
                          'Cостав': [],
                          'Диаметр': [],
                          'Вес': [],
                          'Тип пиццы': [],
                          'Цена с доставкой': [],
                          'Цена навынос': [],}
        sheet_name = pizza.find("h3").text[:31]
        pizza_data = json.loads(pizza.find(class_="pizza-selector")['data-initprops'])
        for i in pizza_data['pizzaList']:
            all_pizza_data['Фото'].append(pizza.find("img")['src'])
            all_pizza_data['Cостав'].append(pizza.find(class_="composition").string.strip().capitalize())
            all_pizza_data['Диаметр'].append(i['size'] + 'см')
            all_pizza_data['Вес'].append(i['weight'] + "г")
            all_pizza_data['Тип пиццы'].append(pizzaDough[i["type"] - 1])
            all_pizza_data['Цена с доставкой'].append(BeautifulSoup(i['price'], "lxml").find(class_='price_byn')['data-price'] + "BYN")
            all_pizza_data['Цена навынос'].append(BeautifulSoup(i['priceTakeAway'], "lxml").find(class_='price_byn')['data-price'] + "BYN")
            #print(size, weight, pizzaType, price_deliver, priceTakeAway)
        #print("\n\n")
        df = pd.DataFrame(all_pizza_data)
        df.to_excel(writer, sheet_name=sheet_name, index=False)
writer.save()




#salaries1 = pd.DataFrame({'Name': ['L. Messi', 'Cristiano Ronaldo', 'J. Oblak'],
#                                        'Salary': [560000, 220000, 125000]})
#
#salaries2 = pd.DataFrame({'Name': ['K. De Bruyne', 'Neymar Jr', 'R. Lewandowski'],
#                                        'Salary': [370000, 270000, 240000]})
#
#salaries3 = pd.DataFrame({'Name': ['Alisson', 'M. ter Stegen', 'M. Salah'],
#                                        'Salary': [160000, 260000, 250000]})
#
#salary_sheets = {'Group1': salaries1, 'Group2': salaries2, 'Group3': salaries3}
#writer = pd.ExcelWriter('./salaries.xlsx', engine='xlsxwriter')
#
#for sheet_name in salary_sheets.keys():
#    salary_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
#
#writer.save()

