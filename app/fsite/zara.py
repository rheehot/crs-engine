#-*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2020, SEOK.
# All rights reserved.

__author__ = 'SEOK'

import os
import time
import csv
import datetime
import logging
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

from app.common.util import ref_safe, idx_safe, get_webdriver_wait, text_is_not_empty, attr_must_fn
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
        
        driver = webdriver.Chrome(executable_path=chromeSet.DRIVER_PATH, options=chromeSet.options)
        # 웹 페이지 로딩 시 3초간 대기함 (셀레니움 암묵적 대기)
        driver.implicitly_wait(3)
        driver.get(p_url)

        # 상품 목록 수집
        # document.querySelectorAll('#products > div > ul > li a').length : 279
        elements = driver.find_elements_by_css_selector('#products > div > ul > li > a')
        logger.info('상품 개수: {}'.format(len(elements)))

        wait = get_webdriver_wait(driver, timeout=15)

        link_list = []
        for el in elements:
            url = el.get_attribute('href')
            qs = el.get_attribute('data-extraquery')
            full_url = url + '?' + qs
            link_list.append(url)

        # link 중복값 제거 
        link_list = list(set(link_list))
        logger.info('Targets: {}'.format(len(link_list)))

        # 상품 설명 추출
        total_cnt = 0
        product_list = []
        for slink in link_list:
            driver.get(slink)

            try:
                # 상품 가격의 텍스트가 표시될 때까지 명시적으로 최대 timeout초 대기
                # https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions
                wait.until(
                    text_is_not_empty('div.price > span')
                )
            except:
                # timeout초 이후에도 상품 정보를 로드할 수 없는 경우
                logger.warning('Data not found')
                continue

            # 상품 정보 추출
            name = driver.find_elements_by_css_selector('h1.product-name')
            color = driver.find_elements_by_css_selector('p.product-color > span._colorName')
            price = driver.find_elements_by_css_selector('div.price > span')
            
            if isinstance(name, list):
                name = idx_safe(name, 0)
            
            if isinstance(color, list):
                color = idx_safe(color, 0)

            if isinstance(price, list):
                price = idx_safe(price, 0)
 
            name = ref_safe(name, 'text')
            color = ref_safe(color, 'text')
            price = ref_safe(price, 'text')

            # 상품 이름이 없는 경우 문제가 발생한 것으로 판단하고 다음 상품 진행
            if not price:
                logger.warning('No product name: {}'.format(slink))
                continue

            product_data = {
                "name": name,
                "color": color,
                "price": price,
                "url": slink,
                "saved": False
            }
            product_list.append(product_data)

            logger.info('({}, {}, {}):{}'.format(name, color, price, slink))
            info_file_nm = _COLLECT_DATE_ + '_' + p_product_sex + '_' + p_brand + '_' + p_product_categori + '_' + p_job_id + '.csv'

            time.sleep(3)

            # 이미지 영역 추출
            sub_elements = driver.find_elements_by_css_selector('#main-images > div > a > img.image-big._img-zoom._main-image')

            # 이미지 다운로드
            i = 0
            for sub_el in sub_elements:
                try:
                    # 자라의 경우 base64 로딩 이미지를 보여주다가,
                    # 이미지가 로드되면 기존 src 대체함.
                    # => src 속성에 base64 값이 사라딜
                    wait.until(
                        attr_must_fn('src', lambda a: not a.find('base64') != -1, el=sub_el)
                    )
                except Exception as e:
                    traceback.print_exc()
                    logger.error('EEE!!')
                    logger.error(e)
                    pass

                try:
                    img_src = sub_el.get_attribute('src')
                    logger.info(img_src)
                    req = Request(img_src, headers={'User-Agent': 'Mozilla/5.0'})
                    res = urlopen(req).read()

                    img_file_nm = _COLLECT_DATE_ + '_' + p_product_sex + '_' + p_brand + '_' + p_product_categori + '_' + product_data['name'] + '_' + str(i+1) + '.jpg'
                    filename = p_savepath + '/images/' + p_brand + '/' + img_file_nm

                    with open(filename.encode('utf-8'), "wb") as f:
                        f.write(res)

                    product_data['saved'] = True
                    i += 1
                except Exception as e:
                    logger.error('Image download failed')
                    logger.error(e)

            # 크롤링한 이미지 수 추가
            total_cnt += 1

        # Save data as csv
        with open(p_savepath + '/info/' + p_brand + '/' + info_file_nm, mode='a', encoding="utf-8") as product_infos:
            product_writer = csv.writer(product_infos)
            for prod in product_list:
                if not prod['saved']:
                    continue
                product_writer.writerow([prod['name'], prod['color'], prod['price'], prod['url']])

        logger.info('END, ' + str(total_cnt))
    except Exception as ex:
        logger.error('ERROR [zara - getData]')
        traceback.print_exc()
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
        p_args['product_categori'] = 'test'
        logger.info(save_path)
        
        getData(p_args, save_path)

    except Exception as ex:
        logger.error('ERROR [zara - main]')
        logger.error(ex)
    finally:
        driver.quit()
