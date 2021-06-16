import time
import os
from pathlib import Path
import traceback
import pprint

from selenium import webdriver
import selenium.common.exceptions as SeleniumExceptions
from bs4 import BeautifulSoup


BASE_URL = "https://www.wanted.co.kr/wdlist/518"
BASE_DATA_PATH = Path("crawled_data")
DRIVER_PATH = Path('./webdriver/chromedriver')
CATEGORY_BUTTON_CLASS = "_3SgvgiuDypnw8sSW2Pxngs"
PAUSE_TIME = 3


def get_driver(driver_path: Path = DRIVER_PATH):
    options = webdriver.ChromeOptions()
    return webdriver.Chrome(driver_path.absolute(), options=options)


def parse(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    positions = soup.find_all('div', {'class': 'body'})
    yield from (
        {
            "location": position.find('div', {'class': 'job-card-company-location'}).text,
            "company": position.find('div', {'class': 'job-card-company-name'}).text,
            "title": position.find('div', {'class': 'job-card-position'}).text
        } for position in positions
    )


def subcrawl(driver: webdriver.Chrome) -> str:
    page_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(PAUSE_TIME)
        page_height_scrolled = driver.execute_script(
            "return document.body.scrollHeight")
        if page_height == page_height_scrolled:
            break
        page_height = page_height_scrolled
    return driver.page_source


def click_category_button(driver: webdriver.Chrome, button_index: int) -> str:
    while True:
        try:
            buttons = driver.find_elements_by_class_name(CATEGORY_BUTTON_CLASS)
            category = buttons[button_index].text
            buttons[button_index].click()
        except (SeleniumExceptions.ElementClickInterceptedException, SeleniumExceptions.ElementNotInteractableException):
            right_button = driver.find_element_by_xpath(
                '//*[@id="__next"]/div/div[3]/div[1]/div/div/button[2]/i')
            right_button.click()
            time.sleep(PAUSE_TIME)
        else:
            return category


def crawl_and_save(do_all: bool = True):
    driver = get_driver()
    button_index = 0
    information = {}

    try:
        # Whole positions
        if do_all:
            driver.get(BASE_URL)
            time.sleep(PAUSE_TIME)
            information["All"] = parse(subcrawl(driver))

        # Sub categories
        while True:
            driver.get(BASE_URL)
            time.sleep(PAUSE_TIME)
            buttons = driver.find_elements_by_class_name(CATEGORY_BUTTON_CLASS)
            if button_index >= len(buttons):
                break

            category = click_category_button(driver, button_index)
            time.sleep(PAUSE_TIME)
            print("Crawling category [%s]..." % (category,))
            information[category] = parse(subcrawl(driver))
            button_index += 1

    except BaseException as e:
        traceback.print_exception(type(e), e, e.__traceback__)

    finally:
        # Write CSV
        with open(BASE_DATA_PATH / "company_list.csv", "w") as file:
            file.write("category,company,position,location\n")
            for category in information:
                file.writelines("%s,%s,%s,%s\n" % (
                    category, info["company"], info["title"], info["location"]
                ) for info in information[category])


if __name__ == "__main__":
    crawl_and_save(True)
