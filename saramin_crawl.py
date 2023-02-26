import csv
import math
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}
request_url = "https://www.saramin.co.kr/zf_user/jobs/list/job-category?page={}&cat_kewd=92%2C87%2C86%2C84%2C91&search_optional_item=n&search_done=y&panel_count=y&preview=y&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1#searchTitle"

# csv 헤더 작성
filename = "사람인공고추출.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)
title = "기업명	직무	지원자격	학력자격	근무타입	근무지역".split("\t")
writer.writerow(title)

# 전체 페이지수 계산
base_url = "https://www.saramin.co.kr/zf_user/jobs/list/job-category?page=1&cat_kewd=92%2C87%2C86%2C84%2C91&search_optional_item=n&search_done=y&panel_count=y&preview=y&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1#searchTitle"
response = requests.get(base_url, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, "lxml")
total_count = (
    soup.find("div", attrs={"class": "common_recruilt_list"})
    .find("span", attrs={"class": "total_count"})
    .get_text()
    .replace("건", "")
    .replace(",", "")
)
total_page = math.ceil(int(total_count) / 50)
current_page = 1

# 페이지별로 데이터 추출
while True:
    response = requests.get(request_url.format(current_page), headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    rows = soup.find("div", attrs={"class": "common_recruilt_list"}).find_all(
        "div", attrs={"class": "list_item"}
    )
    for row in rows:
        company_name = (
            row.find("div", attrs={"class": "company_nm"}).find("a").get_text()
        )
        job_title = row.find("div", attrs={"class": "job_tit"}).find("a").get_text()

        requirements = row.find("p", attrs={"class": "career"})
        if requirements:
            requirements = requirements.get_text()
        else:
            requirements = "<없음>"

        education = row.find("p", attrs={"class": "education"})
        if education:
            education = education.get_text()
        else:
            education = "<없음>"

        career_type = row.find("p", attrs={"class": "employment_type"})
        if career_type:
            career_type = career_type.get_text()
        else:
            career_type = "<없음>"

        work_location = row.find("p", attrs={"class": "work_place"})
        if work_location:
            work_location = work_location.get_text()
        else:
            work_location = "<없음>"

        data = [
            company_name,
            job_title,
            requirements,
            education,
            career_type,
            work_location,
        ]
        writer.writerow(data)
    current_page += 1
    if current_page > total_page:
        break
