import time
import pandas as pd
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

warnings.filterwarnings('ignore')

	
def rank(data):
    out = []
    options = webdriver.ChromeOptions()  # 옵션 객체 생성
    options.add_argument("--headless")  # 헤드리스 모드로 설정 (필요한 경우)
    
    driver = webdriver.Chrome()
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://map.naver.com/v5/search/"+data) # 검색창에 가게이름 입력
    time.sleep(3)
    driver.implicitly_wait(3)
    driver.switch_to.frame('searchIframe') #  검색하고나서 가게정보창이 바로 안뜨는 경우 고려해서 무조건 맨위에 가게 링크 클릭하게 설정
    driver.implicitly_wait(3)
    temp = driver.find_element_by_xpath('//*[@id="_pcmap_list_scroll_container"]/ul') # 메뉴표에 있는 텍스트 모두 들고옴(개발자 도구에서 그때그때 xpath 복사해서 들고오는게 좋다)
    driver.implicitly_wait(20)
    button = temp.find_elements_by_tag_name('a')
    driver.implicitly_wait(20)
    if '이미지수' in button[0].text or button[0].text == '': # 가게 정보에 사진이 있는 경우
        button[1].send_keys(Keys.ENTER) 
    else: # 사진이 없는 경우
        button[0].send_keys(Keys.ENTER)
    driver.implicitly_wait(3)
    time.sleep(3)
    driver.switch_to.default_content()
    driver.switch_to.frame('entryIframe')
    driver.implicitly_wait(2)
    review = driver.find_element_by_css_selector('#app-root > div > div > div > div.place_section.GCwOh > div._3uUKd._2z4r0 > div._20Ivz') 
    # xpath는 가게마다 다르게 설정되어 있었기 때문에 css selector를 이용해서 review text가 있는 tag에 접근
    review_text = review.find_elements_by_tag_name('span') #span태그 안에서 별 규칙성을 찾지 못해서 span태그안에 별점, 리뷰 텍스트 정보가 들어가 있기 때문에 span에 있는거 모두 들고오기로 했음.
    for i in review_text:
        out.append(i.text) # parsing하기 쉽게 배열에 넣어놓음
    rank_report = 0.0
    review_report = 0
    if len(out) == 0:
        pass
    else:
        if '별점' in out[0]: # 별점이 존재하는 경우
            rank_report = float(out[0].split('\n')[1].split('/')[0]) # 별점을 실수형으로 바꿔서 담아둔다
            if len(out) >3 and '리뷰' in out[3]: # 리뷰가 방문자리뷰, 사용자리뷰 2개가 있는데 방문자, 블로그리뷰가 둘다 있는 경우
                out[2] = out[2].split(' ')[1].replace(',','') # [방문자리뷰,200] 이런 형태로 있는 데이터를 200만 가져오도록 parsing
                out[3] = out[3].split(' ')[1].replace(',','') # [블로그리뷰,50] 형태의 데이터를 50만 가져오도록 parsing
                review_report = int(out[2]) + int(out[3]) # 두 리뷰를 더해준다.
            else:
                out[2] = out[2].split(' ')[1].replace(',','') # 방문자리뷰만 있는 경우
                review_report = int(out[2])
        else: # 별점이 존재하지 않는 경우
            if len(out) < 2: # 방문자리뷰만 있는 경우 또는 블로그리뷰만 있는 경우
                out[0] = out[0].split(' ')[1].replace(',','')
                review_report = int(out[0])
            else: # 방문자리뷰, 블로그리뷰 둘다 있는 경우
                out[0] = out[0].split(' ')[1].replace(',','')
                out[1] = out[1].split(' ')[1].replace(',','')
                review_report = int(out[0]) + int(out[1]) # 리뷰 더해준다
                
    out = (rank_report,review_report) # 별점이랑 리뷰개수 담아서 return 해준다
    return out

rank("베스킨라빈스 경북대")