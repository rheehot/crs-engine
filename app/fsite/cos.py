#-*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2020, GHLEE.
# All rights reserved.

__author__ = 'GHLEE'

import os
import io
import sys
import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

if __name__ == '__main__' and __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import app.common.userAction as userAction
from app.fsite import CrawlingModule
from app.common.util import ref_safe, idx_safe
from app.common.custom_ec import element_exist

class COSModule(CrawlingModule):
    def get_data(self):
        # 상품 페이지 URL 리스트
        link_list = []

        self._driver.get(self._config['site_url'])

        def parser():
            els = []
            prev_count = -1
            prev_time = datetime.datetime.now()
            waiting = 15

            # 무한 스크롤 대기
            while True:
                userAction.evtScrollDown(self._driver)
                els = self._driver.find_elements_by_css_selector('#category-list > div.column > a')
                no_more = True if prev_count == len(els) else False
                prev_count = len(els)

                if not no_more:
                    prev_time = datetime.datetime.now()

                # 30초동안 새로운 상품이 추출되지 않는 경우 마지막 페이지로 간주함
                delta = (datetime.datetime.now() - prev_time).seconds
                if no_more and delta >= 15:
                    self._logger.info('No more products.')
                    break
                elif not no_more:
                    prev_time = datetime.datetime.now()

                self._logger.info(f'Products found: {prev_count}, [Waiting... {delta}/{waiting}s]')
                self.sleep(2)

            hrefs = []
            for el in els:
                hrefs.append(el.get_attribute('href'))

            for href in hrefs:
                self._driver.get(href)
                href = href.split('?')[0]

                lis = self._driver.find_elements_by_css_selector('ul.options > li')
                for li in lis:
                    color_code = li.get_attribute('data-value')
                    prod_url = href + '?slitmCd=' + color_code
                    link_list.append(prod_url)
                    self._logger.info(f'Parsed product URL :: {prod_url}')

        parser()

        # link 중복값 제거
        link_list = list(set(link_list))
        self._logger.info('Products: {}'.format(len(link_list)))

        # 상품 상세정보 추출/이미지 다운로드
        product_list = []
        for slink in link_list:
            self._driver.get(slink)

            # 상품 정보 추출
            name = self._driver.find_element_by_id('product-detail-name')
            color = self._driver.find_elements_by_css_selector('div.color-section label > span')
            price = self._driver.find_element_by_id('prdDetailPrice')

            if isinstance(name, list):
                name = idx_safe(name, 0)
            
            if isinstance(color, list):
                color = idx_safe(color, 0)

            if isinstance(price, list):
                price = idx_safe(price, 0)
 
            name = ref_safe(name, 'text')
            color = ref_safe(color, 'text', default='unknown')
            price = ref_safe(price, 'text')

            # 제품을 찾을 수 없는 경우 건너뛰기
            if not name:
                self._logger.warning('Product not found: {}'.format(slink))
                continue

            product_data = {
                "name": name,
                "color": color,
                "price": price,
                "url": slink
            }
            self.add_meta(product_data)

            # 이미지 영역 추출
            img_elements = self._driver.find_elements_by_css_selector('div.main-image-wrapper > ul > li img')

            # 이미지 다운로드 (동일 상품에 여러 이미지가 있는 경우, 파일명 뒤 숫자로 구분)
            i = 0
            for img_el in img_elements:
                img_src = img_el.get_attribute('src')
                img_file_name = self.get_image_filename(product_data['name'], color=product_data['color'], num=(i + 1))
                self.save_image(img_src, img_file_name)
                i += 1

        # Save data as csv
        self.save_meta()


if __name__ == "__main__":
    save_path  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/")
    
    p_args = {}
    p_args['job_id'] = '1'
    p_args['site_url'] = 'https://www.cosstores.com/kr_krw/women/new-arrivals.html'
    p_args['brand'] = 'cos'
    p_args['brand_nm'] = 'cos'
    p_args['product_sex'] = 'w'
    p_args['product_categori'] = 'test'
    p_args['save_path'] = save_path

    COSModule(p_args).start()
