#-*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2020, SEOK.
# All rights reserved.


__author__ = 'SEOK'

from app.common.comConfig import conf_info
from selenium.webdriver.chrome.options import Options


DRIVER_PATH = conf_info.get('init').get('chromedriver_path')

options = Options()
options.add_argument('--headless')
# 크롬브라우저 로그 레벨 낮춤
options.add_argument('--log-level=3')
# 로그를 남기지 않는 옵션
options.add_argument('--disable-logging')

# GUI 미제공 환경시 사용
options.add_argument('--no-sandbox')
options.add_argument('--disable_gpu')
options.add_argument('window-size=1240x820')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')
