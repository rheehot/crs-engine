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


from app.common.userAction import evtMouseDown
from app.common import chromeSet
    

# 파일명 : 날짜_성별_브랜드_카테고리_상품명_번호
_COLLECT_DATE_ = datetime.datetime.now().strftime('%Y%m%d')

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
        
        
        

        # elements = driver.find_elements_by_css_selector('#products > div > ul > li > a')
        elements = driver.find_elements_by_css_selector('#products > div > ul > li > a')
        # elements2 = driver.find_elements_by_css_selector('#products > div._groups-wrap > ul > li > div')

        # print(driver.page_source)
        # print(elements)

        print('상품 개수: {}'.format(len(elements)))
        # print('상품 설명 개수: {}'.format(len(elements2)))

        # link_str = elements[0].get_attribute('href')
        link_list = []
        for el in elements:
            link_list.append(el.get_attribute('href'))
            # print(el.get_attribute('href'))

        print(len(link_list))
        
        # link 중복값 제거 
        link_list = list(set(link_list))
        print(len(link_list))
        
        
        
        
        
        # 상품 설명 추출
        product_list = []
        # TODO: 상품 정보 추출 로직 작성 필요
        for slink in link_list:
            print(slink)
            product_list.append({
                "name": '',
                "color": '',
                "price": ''
            })
        '''
        
        
        product_list.append({
            "name": '',
            "color": '',
            "price": ''
        })
        
        info_file_nm = _COLLECT_DATE_ + '_' + p_product_sex + '_' + p_brand + '_' + p_product_categori + '_' + p_job_id + '.csv'
        
        with open(p_savepath + '/info/' + p_brand + '/' + info_file_nm, mode='w', encoding="utf-8") as product_infos:
            product_writer = csv.writer(product_infos)
    
            for list in product_list:
                product_writer.writerow([list["name"], list["color"], list["price"]])
        
        
        '''
        
        
        

        total_cnt=0
        for slink in link_list:
            # print(slink)
            
            driver.get(slink)

            driver.implicitly_wait(5)
            
            #main-images > div:nth-child(2) > a > img.image-big._img-zoom._main-image
            sub_elements = driver.find_elements_by_css_selector('#main-images > div > a > img.image-big._img-zoom._main-image')

            i=0
            for sub_el in sub_elements:

                img_src = sub_el.get_attribute('src')
                print(img_src)

                req = urllib.request.Request(img_src, headers={'User-Agent': 'Mozilla/5.0'})

                t = urlopen(req).read()
                
                img_file_nm = _COLLECT_DATE_ + '_' + p_product_sex + '_' + p_brand + '_' + p_product_categori + '_' + product_list[i].get('name') + '_' + str(i+1) + '.jpg'
                filename = p_savepath + '/images/' + p_brand + '/' + img_file_nm

                with open(filename.encode('utf-8'), "wb") as f:
                    f.write(t)
                i=i+1

            total_cnt = total_cnt + 1
        
        
        
        
    except Exception as ex:
        print('ERROR [zara - getData]')
        print(ex)
    finally:
        driver.quit()
    

if __name__ == "__main__":
    
    try:
        
        driver = webdriver.Chrome(executable_path=chromeSet.DRIVER_PATH, options=chromeSet.options)
        save_path  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/")
        
        p_args = {}
        p_args['job_id'] = '1'
        p_args['site_url'] = 'https://www.zara.com/kr/ko/woman-event-l1053.html?v1=1478211'
        p_args['brand'] = 'zara'
        p_args['brand_nm'] = 'zara'
        p_args['product_sex'] = 'w'
        p_args['product_categori'] = 'event'
        
        getData(p_args, save_path)
    
    except Exception as ex:
        print('ERROR [zara - main]')
        print(ex)
    finally:
        driver.quit()
