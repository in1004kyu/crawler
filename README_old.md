## 디렉토리 구조

```
root
ㄴ webdriver
    ㄴ chromedriver
ㄴ crawled_data
    ㄴ wanted.html
    ㄴ company_list.csv
ㄴwanted_crawl.py
```

## 실행 방법

1. 터미널 열기
2. `cd {path}`
3. `python3 /wanted_crawl.py`

## 에러 해결 방법

#### 에러 1

**상황**: 실행 중 다음과 같은 에러 메시지가 나는 경우: 

`selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome version must be between ...` 

**해결 방법**: 컴퓨터에 설치된 크롬 버전과 webdriver 디렉토리의 chromedriver가 맞지 않을 때 위와 같은 에러가 발생하므로, chromedriver를 교체하면 됨.

1. [chromedriver 다운로드 링크](https://chromedriver.chromium.org/downloads)에서 컴퓨터에 설치된 크롬 버전에 맞는 chromedriver를 다운로드
2. webdriver 디렉토리의 chromedriver를 1에서 다운로드한 걸로 교체
3. chromedriver 마우스 우클릭 - 실행 버튼 클릭하기
    * 주의: 꼭 우클릭해 실행할 것. 더블 클릭으로 파일을 실행하면 mac이 이 파일은 신뢰할 수 없다며 막아버린다.
4. 스크립트 재실행

#### 에러 2

**상황**: 실행 중 다음과 같은 에러 메시지가 나는 경우:

`selenium.common.exceptions.WebDriverException: Message: Service ./webdriver/chromedriver unexpectedly exited. Status code was: -9`

**해결 방법**: 스크립트가 webdriver를 실행하지 못했다는 뜻이므로 직접 webdriver를 실행해주면 됨.

1. chromedriver 우클릭 - 실행 버튼 클릭하기
    * 주의: 꼭 우클릭해 실행할 것. 더블 클릭으로 파일을 실행하면 mac이 이 파일은 신뢰할 수 없다며 막아버린다.
2. 스크립트 재실행
