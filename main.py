from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import time
import collections
import csv

chrome_driver = '/Users/joseong-eun/crawl_starbucks/chromedriver_mac64/chromedriver'
driver = webdriver.Chrome(chrome_driver)
driver.implicitly_wait(5) 


# 스타벅스 위치 정보 페이지
url = 'https://www.starbucks.co.kr/store/store_map.do'

# 페이지가 물리적으로 open
driver.get(url)

# 값을 담을 리스트
starbucks = []

# 열린 페이지에서 '지역 검색' 탭 클릭
search = driver.find_element(By.LINK_TEXT, '지역 검색')
time.sleep(1)
search.click()

time.sleep(1)
# 개발자도구로 class : set_sido_cd_btn의 데이터 긁어옴
search = driver.find_elements(By.CLASS_NAME, 'set_sido_cd_btn')

for item in search:
    item.click()
    time.sleep(1)

    # data-sidocd='01~17' 서울~세종
    if '17' == item.get_attribute('data-sidocd'):
        print('in')
        # 소스 가져오기
        src = driver.page_source

        # BeautifulSoup 객체로 변환
        soup = BeautifulSoup(src)
        name = soup.select('li[data-name]')
        for name_one in name:
            print(name_one)
            x = name_one['data-lat'] # 위도 저장
            y = name_one['data-long'] # 경도 저장
            z = name_one['data-name'] # 지점명 저장
            p = name_one.select_one('p').text.split('1522-3232')[0] 
            starbucks.append({'name': z, 'address': p, 'lat': x, 'long':y}) # dict 형태로 리스트에 저장
        time.sleep(1)

        # 열린 페이지 닫기
        driver.close()
    else:
        print('out')

        search2 = driver.find_element(By.LINK_TEXT, '전체')
        search2.click()
        driver.implicitly_wait(5)
        time.sleep(1)

        src = driver.page_source

        soup = BeautifulSoup(src)
        name = soup.select('li[data-name]')
        for name_one in name:
            print(name_one)
            x = name_one['data-lat']
            y = name_one['data-long']
            z = name_one['data-name']
            p = name_one.select_one('p').text.split('1522-3232')[0]
            starbucks.append({'name': z, 'address': p, 'lat': x, 'long':y})
        time.sleep(1)

        # 다시 지역 검색 탭으로 돌아가기위한 소스
        search3 = driver.find_element(By.LINK_TEXT,'지역 검색')
        search3.click()
        time.sleep(1)

        # 리스트 중복값 제거
        starbucks = list(map(dict, collections.OrderedDict.fromkeys(tuple(sorted(d.items())) for d in starbucks)))



# newline=''을 넣으면 공백라인 제거
with open('starbucks.csv', 'w', newline='') as f:
    fieldnames =['지점명', '주소', '위도', '경도']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for i in starbucks:
        writer.writerow({'지점명': i['name'], '주소': i['address'], '위도': i['lat'], '경도': i['long']})