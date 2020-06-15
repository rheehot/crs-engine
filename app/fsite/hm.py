#-*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2020, GHLEE.
# All rights reserved.

__author__ = 'SEOK'

import os
import time
import csv
import datetime
import logging
import logging.handlers
import traceback
from selenium import webdriver
from urllib.request import urlopen, Request

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

if __name__ == '__main__' and __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.common.util import ref_safe, idx_safe, get_webdriver_wait, element_exist
from app.common.userAction import evtMouseDown
from app.common import chromeSet


# 파일명 : 날짜_성별_브랜드_카테고리_상품명_번호
_COLLECT_DATE_ = datetime.datetime.now().strftime('%Y%m%d')
logger = logging.getLogger(__name__)

def getData(p_args, p_savepath):
    try:
        p_job_id = p_args['job_id']
        p_url = p_args['site_url']
        p_brand = p_args['brand']
        p_brand_nm = p_args['brand_nm']
        p_product_sex = p_args['product_sex']
        p_product_categori = p_args['product_categori']

        link_list = []
        def product_parser(driver):
            '''
            H&M 모든 상품 목록 추출 (더 보기 버튼 처리)
            '''
            more_btn = driver.find_elements_by_css_selector('button.js-load-more')
            if len(more_btn) >= 1:
                more_btn = idx_safe(more_btn, 0)

            while True:
                # 더 보기 버튼이 보이는 경우 (상품이 더 있음)
                if not (more_btn.is_displayed()):
                    break

                more_btn.click()
                time.sleep(3)

            # 상품 링크 태그 추출
            product_anchors = driver.find_elements_by_css_selector('ul.products-listing li div.image-container > a')

            # 상품 페이지 정보 추출
            product_list = []
            for el in product_anchors:
                url = el.get_attribute('href')
                product_list.append(url)

            # 상품별 색상 정보 추출 (색상별 상품 페이지 URL)
            for product_url in product_list:
                logger.info(product_url)
                driver.get(product_url)

                # 색상 정보 로드 대기
                try:
                    wait.until(
                        element_exist('div.product-colors.loaded')
                    )
                except:
                    continue
                
                product_colors = driver.find_elements_by_css_selector('li.mini-slider-group > ul > li > a')

                for product_color in product_colors:
                    href = product_color.get_attribute('href')
                    link_list.append(href)
                    logger.info('Find: ' + href)

        driver = webdriver.Chrome(executable_path=chromeSet.DRIVER_PATH, options=chromeSet.options)
        # 웹 페이지 로딩 시 3초간 대기함 (셀레니움 암묵적 대기)
        driver.implicitly_wait(3)
        driver.get(p_url)
        wait = get_webdriver_wait(driver, timeout=10)

        # 상품 모두 추출
        product_parser(driver)

        # link 중복값 제거 
        link_list = list(set(link_list))
        logger.info('Targets: {}'.format(len(link_list)))

        # 상품 설명 추출
        total_cnt = 0
        product_list = []
        info_file_nm = _COLLECT_DATE_ + '_' + p_product_sex + '_' + p_brand + '_' + p_product_categori + '_' + p_job_id + '.csv'

        for slink in link_list:
            driver.get(slink)

            # 상품 정보 추출
            name = driver.find_elements_by_css_selector('section.name-price h1.primary')
            color = driver.find_elements_by_css_selector('div.product-colors h3.product-input-label')
            price = driver.find_elements_by_css_selector('section.name-price span.price-value')

            if isinstance(name, list):
                name = idx_safe(name, 0)
            
            if isinstance(color, list):
                color = idx_safe(color, 0)

            if isinstance(price, list):
                price = idx_safe(price, 0)
 
            name = ref_safe(name, 'text')
            color = ref_safe(color, 'text', default='unknown')
            price = ref_safe(price, 'text')

            product_data = {
                "name": name,
                "color": color,
                "price": price,
                "url": slink
            }
            product_list.append(product_data)

            logger.info('({}, {}, {}):{}'.format(name, color, price, slink))

            # 이미지 영역 추출
            # 메인
            sub_elements = driver.find_elements_by_css_selector('figure.product-detail-images img')
            # 서브
            sub_elements += driver.find_elements_by_css_selector('figure.pdp-secondary-image > img')

            # 이미지 다운로드
            i = 0
            for sub_el in sub_elements:
                img_src = sub_el.get_attribute('src')
                logger.info(img_src)
                req = Request(img_src, headers={'User-Agent': 'Mozilla/5.0'})
                res = urlopen(req).read()

                img_file_nm = _COLLECT_DATE_ + '_' + p_product_sex + '_' + p_brand + '_' + p_product_categori + '_' + product_data['name'] + '_' + str(i+1) + '.jpg'
                filename = p_savepath + '/images/' + p_brand + '/' + img_file_nm

                with open(filename.encode('utf-8'), "wb") as f:
                    f.write(res)

                i += 1

            # 크롤링한 이미지 수 추가
            total_cnt += 1
        
        # Save data as csv
        with open(p_savepath + '/info/' + p_brand + '/' + info_file_nm, mode='a', encoding="utf-8") as product_infos:
            product_writer = csv.writer(product_infos)
            for prod in product_list:
                product_writer.writerow([prod['name'], prod['color'], prod['price'], prod['url']])

        logger.info('END, ' + str(total_cnt))
    except Exception as ex:
        logger.error('ERROR [hm - getData]')
        traceback.print_exc()
    finally:
        driver.quit()


if __name__ == "__main__":
    try:
        driver = webdriver.Chrome(executable_path=chromeSet.DRIVER_PATH, options=chromeSet.options)
        save_path  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/")
        
        p_args = {}
        p_args['job_id'] = '1'
        p_args['site_url'] = 'https://www2.hm.com/ko_kr/ladies/new-arrivals/clothes.html'
        p_args['brand'] = 'hm'
        p_args['brand_nm'] = 'hm'
        p_args['product_sex'] = 'w'
        p_args['product_categori'] = 'test'
        logger.info(save_path)
        
        getData(p_args, save_path)

    except Exception as ex:
        logger.error('ERROR [hm - main]')
        logger.error(ex)
    finally:
        driver.quit()
