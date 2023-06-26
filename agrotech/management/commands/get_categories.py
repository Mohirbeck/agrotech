from django.core.management.base import BaseCommand
from selenium import webdriver
import geckodriver_autoinstaller
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
from requests.auth import HTTPBasicAuth
import json
from agrotech.models import Category, Product, ProductImage, UnitOfMeasure, ProductPrice
from django.core.files.base import ContentFile
import re
import time


def scroll_to_bottom(driver):
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        if last_height == driver.execute_script("return document.body.scrollHeight"):
            break
        last_height = driver.execute_script("return document.body.scrollHeight")


def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.

    Chrome options for headless browser is enabled.

    """

    chrome_options = Options()

    chrome_options.add_argument("--headless")

    chrome_options.add_argument("--no-sandbox")

    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_prefs = {}

    chrome_options.experimental_options["prefs"] = chrome_prefs

    chrome_prefs["profile.default_content_settings"] = {"images": 2}

    return chrome_options


class Command(BaseCommand):
    help = "Get categories"

    def handle(self, *args, **options):
        categories = []
        url = "https://lebazar.uz/store/korzinka-uz-7/beruniy-115/categories"
        driver = webdriver.Chrome(options=set_chrome_options())
        driver.get(url)
        print(url)
        driver.add_cookie({"name": "lang", "value": "ru"})
        time.sleep(2)
        driver.get(url)
        time.sleep(5)
        see_more_buttons = driver.find_elements(By.CLASS_NAME, "toggle-link")
        for button in see_more_buttons:
            driver.execute_script("arguments[0].click();", button)
            time.sleep(5)
        cats = driver.find_elements(By.CLASS_NAME, "category-list-box")
        for cat in cats:
            subcats = []
            sub_cats = cat.find_elements(By.TAG_NAME, "li")
            categ, created = Category.objects.get_or_create(
                name=cat.find_element(By.CLASS_NAME, 'category-name').text,
                slug=cat.find_element(By.TAG_NAME, "a")
                .get_attribute("href")
                .split("/")[-1],
                layer=1,
            )
            for sub_cat in sub_cats:
                sub_categ = Category.objects.get_or_create(
                    name=sub_cat.text,
                    slug=sub_cat.find_element(By.TAG_NAME, "a")
                    .get_attribute("href")
                    .split("/")[-1],
                    parent=categ,
                    layer=2
                )
                subcats.append(
                    {
                        "name": sub_cat.text,
                        "url": sub_cat.find_element(By.TAG_NAME, "a").get_attribute(
                            "href"
                        ),
                    }
                )
            categories.append(
                {
                    "name": cat.find_element(By.CLASS_NAME, 'category-name').text,
                    "url": cat.find_element(By.TAG_NAME, "a").get_attribute("href"),
                    "subcats": subcats,
                }
            )

        for cat in categories:
            for subcat in cat["subcats"]:
                products = []
                sub_cat = Category.objects.get(slug=subcat['url'].split("/")[-1])
                driver.get(subcat["url"])
                print(subcat["url"])
                time.sleep(3)
                scroll_to_bottom(driver)
                time.sleep(3)
                ps = driver.find_elements(By.CLASS_NAME, "product-item")
                for p in ps:
                    name = p.find_element(By.CLASS_NAME, "product-title").text
                    price = "0"
                    unit = ""
                    try:
                        sale_unit_price = p.find_element(
                            By.CLASS_NAME, "sale-unit-price"
                        ).text.split("/")
                        price = sale_unit_price[0].split("сум")[0].replace(" ", "")
                        unit = sale_unit_price[1].replace(" ", "").replace("1", "")
                    except:
                        pass
                    try:
                        sale_unit_price = p.find_element(
                            By.CLASS_NAME, "sale-price"
                        ).text.split("/")
                        price = sale_unit_price[0].split("сум")[0].replace(" ", "")
                        unit = sale_unit_price[1].replace(" ", "").replace("1", "")
                    except:
                        pass
                    url = p.find_element(By.CLASS_NAME, "clickable").get_attribute(
                        "href"
                    )
                    image = (
                        p.find_element(By.CLASS_NAME, "product-image")
                        .find_element(By.TAG_NAME, "img")
                        .get_attribute("src")
                    )

                    u, c = UnitOfMeasure.objects.get_or_create(name=unit, short_name=unit)

                    prod, created = Product.objects.get_or_create(
                        name=name,
                        unit_of_measure=u,
                        article_id=1,
                        stock=999,
                        company_id=1,
                        category=sub_cat
                    )
                    ProductPrice.objects.create(product=prod, price=int(price), min_quantity=1, max_quantity=999)
                    img = ProductImage.objects.create(product=prod)
                    img.image.save(image.split('/')[-1], ContentFile(requests.get(image).content))
                    img.save()

                    products.append(
                        {
                            "name": name,
                            "price": price,
                            "unit": unit,
                            "url": url,
                            "image": image,
                        }
                    )

                subcat["products"] = products
        # save to json
        with open("categories.json", "w") as f:
            json.dump(categories, f)
        driver.quit()
