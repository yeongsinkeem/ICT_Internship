import time
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException

warnings.filterwarnings('ignore')

# 두 문자열 사이의 레벤슈타인 거리 계산하는 함수 
def levenshtein_distance(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)
    
    # 초기 행렬 생성
    dp = [[0] * (len_str2 + 1) for _ in range(len_str1 + 1)]
    
    # 초기 값 설정
    for i in range(len_str1 + 1):
        dp[i][0] = i
    for j in range(len_str2 + 1):
        dp[0][j] = j
    
    # 레벤슈타인 거리 계산
    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)
    
    return dp[len_str1][len_str2]

# 두 문자열의 유사성 점수 계산하는 함수, 유사성 점수는 0 ~ 1
def similarity_score(str1, str2):
    max_len = max(len(str1), len(str2))
    distance = levenshtein_distance(str1, str2)
    similarity = 1 - (distance / max_len)
    return similarity


def check_network(media):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    
    url = f"https://map.naver.com/p/search/{media}" 
    try:
        driver.get(url)
        time.sleep(2)
    except (WebDriverException, TimeoutException) as e:
        print("네트워크 연결이 끊겼습니다.")
        print(e)
        return None

    return driver

def extract_media_info(driver, media):
    try:
        # 검색 결과가 한 곳인지 여러 곳인지에 따라 웹페이지 구조가 달라짐
        # 검색결과 장소가 한 군데라면 entryIframe 존재
        if 'entryIframe' in driver.page_source:      
            driver.switch_to.frame('entryIframe')
            try:
                # time_inf는 진료 여부, time_inf2는 진료 종료 시간 및 휴게 시간을 알려주는 변수
                time_inf = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[5]/div/div[1]/div[1]/div/div[3]/div/a/div/div/div/em').text
                time_inf2 = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[5]/div/div[1]/div[1]/div/div[3]/div/a/div/div/div/span/time').text
            # 예외처리
            except NoSuchElementException:
                time_inf = None
                time_inf2 = None
            
            # time_inf와 time_inf2 값이 None 일 때에 따른 경우 예외처리
            if time_inf == None and time_inf2 == None:
                try:
                    time_inf = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[5]/div/div[1]/div[1]/div/div[2]/div/a/div[1]/div/div/em').text
                    time_inf2 = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[5]/div/div[1]/div[1]/div/div[2]/div/a/div[1]/div/div/span/time').text
                except NoSuchElementException:
                    time_inf = None
            print(time_inf, time_inf2)
            return True
        
        # 검색 결과가 여러개인 경우 searchIframe으로 이동
        else: 
            driver.switch_to.frame('searchIframe')

            # 간혹 검색하였을 때 media 이름과 동일하지 않은데 검색결과가 나오는 오류 처리  
            name = driver.find_element(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul/li[1]/div[1]/div[2]/a[1]/div/div/span[1]').text
            name = ''.join(name.split())
            media = ''.join(media.split())
            similarity = similarity_score(name, media)
            
            if similarity < 0.3:    # 유사도가 0.3 미만이라면
                print("media값과 검색결과값이 다릅니다.")
                return None
            
            # time_inf는 진료 여부, time_inf2는 진료 종료 시간 및 휴게 시간을 알려주는 변수
            time_inf = driver.find_element(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul/li[1]/div[1]/div[2]/a[2]/div/div/span[1]').text
            time_inf2 = driver.find_element(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul/li[1]/div[1]/div[2]/a[2]/div/div/span[2]').text
            print(time_inf, time_inf2)
            return True
            
    # 검색결과가 한 군데도 나오지 않는 경우
    except NoSuchElementException:
        print("조건에 맞는 업체가 존재하지 않습니다.")
        return None

if __name__ == "__main__":
    start_time = time.time()
    count = 0
    driver = None  # 드라이버 변수를 미리 정의
    
    try:
        while True:
            media = input("검색할 업체명을 입력하세요: ")
            
            for char in media:
                if char.isdigit():
                    count += 1
                    
            if len(media) == count or len(media) <= 0:     # 만약 매체가 숫자로만 이루어져 있거나 공백이라면 올바르지 않은 입력이라 판단
                print("올바른 형식의 입력이 아닙니다. 문자열을 입력하세요.")
            else:
                start_time = time.time()
                driver = check_network(media)
                if driver:
                    extract_media_info(driver, media)
                    break
                else:
                    print("네트워크 연결에 문제가 있습니다.")
    finally:
        if driver:
            driver.quit()
        end_time = time.time()
        print("실행 시간:", end_time - start_time)


