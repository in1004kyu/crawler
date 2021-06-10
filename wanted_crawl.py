from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

BASE_URL = "https://www.wanted.co.kr/wdlist/518"
DUMP_FILE_PATH = "crawled_data/wanted.html"
CSV_FILE_PATH = "crawled_data/company_list.csv"

SCROLL_PAUSE_TIME = 3


def web_driver_options():
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')
    return options

def scroll_and_dump_html():
    driver = webdriver.Chrome('./webdriver/chromedriver', options=web_driver_options())
    driver.get(BASE_URL)

    # Get scroll height
    page_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        page_height_scrolled = driver.execute_script("return document.body.scrollHeight")
        if page_height == page_height_scrolled:
            break
        page_height = page_height_scrolled

    html = driver.page_source
    driver.quit()
    with open(DUMP_FILE_PATH, 'w+') as dumpfile:
        dumpfile.write(html)


def parse():
    html = open(DUMP_FILE_PATH, 'r').read()
    soup = BeautifulSoup(html, 'html.parser')

    positions = soup.find_all('div', {'class': 'body'})
    position_titles = [row.find('div', {'class': 'job-card-position'}).text for row in positions]
    company_names = [row.find('div', {'class': 'job-card-company-name'}).text for row in positions]
    locations = [row.find('div', {'class': 'job-card-company-location'}).text for row in positions]
    
    positions_with_good_response_rate = list(filter(lambda position: '응답률' in str(position), positions))
    company_names_with_good_response_rate = set([row.find('div', {'class': 'job-card-company-name'}).text for row in positions_with_good_response_rate])

    df = pd.DataFrame({
        'position_title': position_titles,
        'company_name': company_names,
        'location': locations,
    })
    df['good_response_rate'] = df['company_name'].isin(company_names_with_good_response_rate)
    df.to_csv(CSV_FILE_PATH, index=False)

    print('찾은 포지션 수:', len(position_titles))
    print('찾은 회사 수:', len(set(company_names)))

if __name__ == '__main__':
    scroll_and_dump_html()
    parse()