#-*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2020, SEOK.
# All rights reserved.

__author__ = 'SEOK'

import os
import time
import csv
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
import urllib.request

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

if __name__ == '__main__' and __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.common import chromeSet
    

# 파일명 : 날짜_성별_브랜드_카테고리_상품명_번호
_COLLECT_DATE_ = datetime.datetime.now().strftime('%Y%m%d')

def evtMouseDown(p_driver):
    
    # 무한 스크롤 적용 
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = p_driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        p_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        p_driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = p_driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height       
        

def getData(p_args, p_savepath):

    try:
        
        # print(p_args)
        
        p_job_id = p_args['job_id']
        p_url = p_args['site_url']
        p_brand = p_args['brand']
        p_brand_nm = p_args['brand_nm']
        p_product_sex = p_args['product_sex']
        p_product_categori = p_args['product_categori']
        
        driver = webdriver.Chrome(executable_path=chromeSet.DRIVER_PATH, options=chromeSet.options)
        
        driver.get(p_url)
    
        # 3초 웹페이지 로딩
        driver.implicitly_wait(3)
        
        # 마우스 스크롤 처리
        evtMouseDown(driver)
        
        elements = driver.find_elements_by_css_selector('#category-list > div > a > div.product-image > div')
        elements2 = driver.find_elements_by_css_selector('#category-list > div > a > div.description')
    
        print('상품 설명 개수: {}'.format(len(elements2)))
        print('상품 개수: {}'.format(len(elements)))
        
        # 상품 설명 추출
        product_list = []
        for el2 in elements2:
            
            el_title = el2.find_elements_by_css_selector('div.product-title > label')
            el_colr = el2.find_elements_by_css_selector('div.product-colours')
            el_price = el2.find_elements_by_css_selector('div.m-product-price > label')
            
            product_name = el_title[0].get_attribute('innerHTML')
            product_color = el_colr[0].get_attribute('innerHTML')
            product_price = el_price[0].get_attribute('innerHTML')
    
            # print('product name: {}'.format(product_name))
            # print('product color: {}'.format(product_color))
            # print('product price: {}'.format(product_price))
    
            product_list.append({
                "name": product_name,
                "color": product_color,
                "price": product_price
            })
            
        info_file_nm = _COLLECT_DATE_ + '_' + p_product_sex + '_' + p_brand + '_' + p_product_categori + '_' + p_job_id + '.csv'
        
        with open(p_savepath + '/info/' + p_brand + '/' + info_file_nm, mode='w', encoding="utf-8") as product_infos:
            product_writer = csv.writer(product_infos)
    
            for list in product_list:
                product_writer.writerow([list["name"], list["color"], list["price"]])
    
    
        i=0
        # 상품 이미지 추출
        for el in elements:
            
            # 파일명 : 날짜_성별_브랜드_카테고리_상품명_번호
            img_file_nm = _COLLECT_DATE_ + '_' + p_product_sex + '_' + p_brand + '_' + p_product_categori + '_' + product_list[i].get('name') + '_' + str(i+1) + '.jpg'
            
            el_product = el.find_elements_by_css_selector('img')
    
            # print('file name: {}'.format(el_product[0].get_attribute('src')))
    
            t = urlopen(el_product[0].get_attribute('src')).read()
            filename = p_savepath + '/images/' + p_brand + '/' + img_file_nm
    
            with open(filename.encode('utf-8'), "wb") as f:
                f.write(t)
            i=i+1

            
    except Exception as ex:
        print('ERROR [stories - getData]')
        print(ex)
    finally:
        driver.quit()
    

if __name__ == "__main__":
    
    try:
        
        driver = webdriver.Chrome(executable_path=chromeSet.DRIVER_PATH, options=chromeSet.options)
        save_path  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/")
        
        p_args = {}
        p_args['job_id'] = '1'
        p_args['site_url'] = 'https://www.stories.com/kr_krw/whats-new/all.html'
        p_args['brand'] = 'stories'
        p_args['brand_nm'] = 'stories'
        p_args['product_sex'] = 'w'
        p_args['product_categori'] = 'new'
        
        getData(p_args, save_path)
    
    except Exception as ex:
        print('ERROR [stories - main]')
        print(ex)
    finally:
        driver.quit()