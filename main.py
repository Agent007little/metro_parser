import json

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from selenium_pars import get_data_with_selenium

URL = "https://online.metro-cc.ru/category/chaj-kofe-kakao/kofe?from=under_search&page="
domain = "https://online.metro-cc.ru"
ua = UserAgent()
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": ua.random
}

cookies = {
    'pickupStore': '15'  # 15 Питер, 10 москва
}

result_dict = dict()
all_links = []
page = 1


# достаём ссылки на каждый товар и записываем их в список
def create_products_links():
    global all_links, page
    while len(all_links) < 100:
        req = requests.get(URL + str(page), headers=headers, cookies=cookies)
        src = req.text
        soup = BeautifulSoup(src, "lxml")

        all_products_on_page = soup.find_all(class_="product-card-photo__link reset-link")
        for el in all_products_on_page:
            link = el.get("href")
            all_links.append(domain + link)
        page += 1
    else:
        page = 1

    for link in all_links[:100]:
        create_result_dict(link)


# Собираем все данные со страницы товара
def create_result_dict(link) -> dict[str:str]:
    global result_dict
    get_data_with_selenium(link)
    with open('index_selenium.html', "r", encoding="utf-8") as f:
        src = f.read()
    soup = BeautifulSoup(src, "lxml")
    # Вытаскиваем ID товара
    result_dict["id товара"] = soup.find(class_="product-page-content__article").text.split()[1]
    # Наименование товара
    result_dict["Наименование"] = soup.find("h1").text.strip()
    # Ссылка на товар
    result_dict["Ссылка на товар"] = link
    prices = soup.find_all("span", class_="product-price__sum-rubles")
    # цены
    if prices[1]:
        result_dict["Промо цена"] = prices[0].text.replace(u"\xa0", u"")
        result_dict["Регулярная цена"] = prices[1].text.replace(u"\xa0", u"")
    else:
        result_dict["Регулярная цена"] = prices[0].text.replace(u"\xa0", u"")
    # бренд
    list_items = soup.find_all("li", class_="product-attributes__list-item")
    result_dict["Бренд"] = list_items[5].find("a").text.strip()
    in_json()


# Сохраняем данные в json
def in_json():
    with open("products.json", "a", encoding="utf-8") as f:
        json.dump(result_dict, f)
        f.write("\n")


def main():
    create_products_links()


if __name__ == "__main__":
    main()
