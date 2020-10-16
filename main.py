import requests
from bs4 import BeautifulSoup

class VehiclesData:
    brand = None
    brand_url = None
    vehicles = []

    def __init__(self, brand, brand_url):
        self.brand = brand
        self.brand_url = brand_url

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

base_url = "https://en.wikipedia.org"
arr = []

def find_car(target_div, car_arr):
    car_group = target_div.find_all("div", class_="mw-category-group")
    if len(car_group) == 0:
        car_group.append(target_div.find("div", class_="mw-content-ltr"))
    for group in car_group:
        a_tags = group.find_all("a")
        for a_tag in a_tags:
            if "Template:" not in a_tag.text:
                car_arr.append(a_tag.text)
            #  data.add_vehicle(a_tag.text)

def find_brand_car(url, car_arr):
    soup = get_page_soup(url)
    target_div = soup.find("div", id="mw-pages")
    if target_div is None:
        return
    next_url = find_next_page(target_div)
    find_car(target_div, car_arr)
    if next_url:
        print(next_url)
        find_brand_car(next_url, car_arr)


def update_car_data():
    for data in arr:
        car_arr = []
        find_brand_car(data.brand_url, car_arr)
        data.vehicles = car_arr
        car_arr = []
        car_count = len(data.vehicles)

        print(f"{data.brand} car crawl done ({car_count})")

def wikipedia_crawl(url):
    soup = get_page_soup(url)
    main_div = soup.find("div", id="mw-subcategories")
    next_url = find_next_page(main_div)
    find_data_div(soup)
    if next_url:
        wikipedia_crawl(next_url)
    else:
        update_car_data()

def find_next_page(div):
    for child in div.children:
        if child.name == "a" and child.text == "next page":
            return child.attrs.get("href")

def get_page_soup(url):
    req = requests.get(base_url + url)
    html = req.text
    return BeautifulSoup(html, 'html.parser')

def find_data_div(soup):
    category_divs = soup.find_all("div", class_="mw-category-group")
    for div in category_divs:
        title = div.find("h3").text
        if title != "*":
            find_brand(div)

def find_brand(div):
    a_tag_arr = div.find_all("a")
    for a in a_tag_arr:
        brand_name = a.text.replace(" vehicles", "")
        href = a.attrs.get("href")
        data = VehiclesData(brand_name, href)
        arr.append(data)
        print(brand_name, href)

if __name__ == "__main__":
    init_url = "/wiki/Category:Vehicles_by_brand"
    wikipedia_crawl(init_url)
