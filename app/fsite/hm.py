#-*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2020, GHLEE.
# All rights reserved.

__author__ = 'SEOK'

import os
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

if __name__ == '__main__' and __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.fsite import CrawlingModule
from app.common.util import ref_safe, idx_safe
from app.common.custom_ec import element_exist

class HMModule(CrawlingModule):
    def get_data(self):
        # 상품 페이지 URL 리스트
        link_list = []
        def parse_products():
            '''
            H&M 모든 상품 목록 추출 (더 보기 버튼 처리)
            '''
            self._driver.get(self._config['site_url'])

            # 더 보기 버튼
            more_btn = self._driver.find_elements_by_css_selector('button.js-load-more')
            
            if len(more_btn) >= 1:
                more_btn = idx_safe(more_btn, 0)

            while True:
                # 더 보기 버튼이 보이는 경우 (상품이 더 있음)
                if not (more_btn.is_displayed()):
                    break

                more_btn.click()
                self.sleep(3)

            # 상품 링크 태그 추출
            product_anchors = self._driver.find_elements_by_css_selector('ul.products-listing li div.image-container > a')

            # 상품 페이지 정보 추출
            product_list = []
            for el in product_anchors:
                url = el.get_attribute('href')
                product_list.append(url)

            # 상품별 색상 정보 추출 (색상별 상품 페이지 URL)
            for product_url in product_list:
                self._driver.get(product_url)

                # 색상 정보 로드 대기
                try:
                    self._wait.until(
                        element_exist('div.product-colors.loaded')
                    )
                except:
                    continue
                
                product_colors = self._driver.find_elements_by_css_selector('li.mini-slider-group > ul > li > a')

                for product_color in product_colors:
                    href = product_color.get_attribute('href')
                    link_list.append(href)
                    self._logger.info(f'Parsed product URL :: {href}')


        # 상품 모두 추출
        parse_products()

        # link 중복값 제거 
        link_list = list(set(link_list))
        self._logger.info('Products: {}'.format(len(link_list)))

        # 상품 상세정보 추출/이미지 다운로드
        total_cnt = 0
        product_list = []
        for slink in link_list:
            self._driver.get(slink)

            # 상품 정보 추출
            name = self._driver.find_elements_by_css_selector('section.name-price h1.primary')
            color = self._driver.find_elements_by_css_selector('div.product-colors h3.product-input-label')
            price = self._driver.find_elements_by_css_selector('section.name-price span.price-value')

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
            self.add_meta(product_data)

            # 이미지 영역 추출
            # 메인
            img_elements = self._driver.find_elements_by_css_selector('figure.product-detail-images img')
            # 서브
            img_elements += self._driver.find_elements_by_css_selector('figure.pdp-secondary-image > img')

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
    p_args['site_url'] = 'https://www2.hm.com/ko_kr/ladies/new-arrivals/clothes.html'
    p_args['brand'] = 'hm'
    p_args['brand_nm'] = 'hm'
    p_args['product_sex'] = 'w'
    p_args['product_categori'] = 'test'
    p_args['save_path'] = save_path

    HMModule(p_args).start()
