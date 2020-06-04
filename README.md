### 소스 형상관리 ###
* git init
* git remote add origin https://gitlab.com/big.imcloud/fashion-crawler.git
* git remote -v
* git config --global user.email "본인@imcloud.co.kr"
* git config --global user.name "본인"
* git config --global --list



# Selenium WebDrivers 다운로드 경로
https://sites.google.com/a/chromium.org/chromedriver/downloads


# 가상화 환경 생성
python3 -m venv env
source /Volumes/DevOps/devs/py_works/fashionCrawler/env/bin/activate

# 라이브러리 목록 생성
pip freeze > requirements.txt

# 라이브러리 일괄 설치
pip install -r requirements.txt


# xvfb, jdk 등 설치 
sudo apt-get update 
sudo apt-get install -y unzip xvfb libxi6 libgconf-2-4 
sudo apt-get install default-jdk 

# 구글 크롬설치 #아래는 루트 권한으로 실행해야 합니다. 
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add 
sudo echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list 
sudo apt-get -y update 
sudo apt-get -y install google-chrome-stable 

# 자신의 크롬 버젼에 맞는 최신 크롬드라이버 주소를 찾아 다운로드 받습니다. 
# google-chrome --version # https://sites.google.com/a/chromium.org/chromedriver/downloads 
# wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip 
wget https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip unzip chromedriver_linux64.zip 

# 다운로드 받은 크롬드라이버를 이동하고 실행 권한 주기 
sudo mv chromedriver /usr/bin/chromedriver 
sudo chown root:root /usr/bin/chromedriver 
chmod +x /usr/bin/chromedriver 

# Remote Selenium WebDrivers 를 실행하기위한 jar 파일 다운로드 
wget https://selenium-release.storage.googleapis.com/3.13/selenium-server-standalone-3.13.0.jar 

# 셀레니움 스탠드얼론 서버 시작 
# selenium-server-standalone-3.13.0.jar 파일을 selenium-server-standalone.jar로 이름 변경 후 
mv selenium-server-standalone-3.13.0.jar selenium-server-standalone.jar 
-run java -Dwebdriver.chrome.driver=/usr/bin/chromedriver -jar selenium-server-standalone.jar 

# Headless ChromeDriver 시작 
chromedriver --url-base=/wd/hub 

# 파이썬에서 셀레니움 실행 테스트 
selenium import webdriver 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 

driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', DesiredCapabilities.CHROME) 
driver.get("https://www.naver.com") 
print(driver.page_source)



# Headless Chrome 인스턴스 검색 및 삭제
ps -ef | grep chrome
kill [인스턴스 번호]


PYTHONIOENCODING=UTF-8



# Docker 기반 멀티 셀레니움 실행
에러: unknown error: session deleted because of page crash
원인: 공유 메모리(/dev/shm) 부족으로 실행 에러 (용량 확인: df -h)
해결: 도커 컨테이너 실행시 해당 메모리 할당 (--shm-size)
 - nvidia-docker run -d --shm-size 2G -it
 - 주의사항: 물리메모리보다 크게 할당하지 않도록