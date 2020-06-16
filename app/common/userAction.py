#-*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2020, GHLEE.
# All rights reserved.


"""
사용자 액션 관련 모듈
 - 스크롤
 - 
"""

import time


def evtMouseDown(driver):
    """
    인피니티 스크롤 이벤트 처리

    Parameters
    ----------
    driver : 
        셀레니움 드라이버
    """

    # 무한 스크롤 적용 
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

def evtScrollDown(driver):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
