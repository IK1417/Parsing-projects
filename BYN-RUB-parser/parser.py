import requests, csv
from bs4 import BeautifulSoup
cities = ['minsk', 'brest', 'vitebsk', 'gomel', 'grodno', 'mogilev']

for city in cities:
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.2.615 Yowser/2.5 Safari/537.36'
    }
    url = f"https://select.by/{city}/kurs-rublya"
    request = requests.get(url, headers=headers)
    src = request.text

    soup = BeautifulSoup(src, "lxml")
    with open(f"data/{city.title()}.csv", "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(("Банк", "Покупка(100 RUB)", "Продажа(100 RUB)", "Кол-во банков"))
    for i in soup.find_all(class_="expand"):
        bank = i.text
        buy = i.find_parent().find_next_sibling().text + " BYN"
        sell = i.find_parent().find_next_sibling().find_next_sibling().text + " BYN"
        number = i.find_parent().text.split()[-1][1:-1]
        with open(f"data/{city.title()}.csv", "a", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow((bank, buy, sell, number))
