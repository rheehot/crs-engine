#-*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2020, SEOK.
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
from app.common.custom_ec import text_is_not_empty, attr_must_fn

class ZARAModule(CrawlingModule):
    def getData(self):
        self._driver.get(self._config['site_url'])

        # 상품 목록 수집
        # document.querySelectorAll('#products > div > ul > li a').length : 279
        elements = self._driver.find_elements_by_css_selector('#products > div > ul > li > a')

        link_list = []
        for el in elements:
            url = el.get_attribute('href')
            qs = el.get_attribute('data-extraquery')
            full_url = url + '?' + qs
            link_list.append(url)
            self._logger.info(f'Parsed product URL :: {url}')

        # link 중복값 제거 
        link_list = list(set(link_list))
        self._logger.info('Products: {}'.format(len(link_list)))

        # 상품 설명 추출
        for slink in link_list:
            self._driver.get(slink)
            try:
                # 상품 가격의 텍스트가 표시될 때까지 명시적으로 최대 timeout초 대기
                # https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions
                self._wait.until(
                    text_is_not_empty('div.price > span')
                )
            except:
                # timeout초 이후에도 상품 정보를 로드할 수 없는 경우
                self._logger.warning('Can\'t load product information')
                continue

            # 상품 정보 추출
            name = self._driver.find_elements_by_css_selector('h1.product-name')
            color = self._driver.find_elements_by_css_selector('p.product-color > span._colorName')
            price = self._driver.find_elements_by_css_selector('div.price > span')
            
            if isinstance(name, list):
                name = idx_safe(name, 0)
            
            if isinstance(color, list):
                color = idx_safe(color, 0)

            if isinstance(price, list):
                price = idx_safe(price, 0)

            name = ref_safe(name, 'text')
            color = ref_safe(color, 'text', default='unknown')
            price = ref_safe(price, 'text')

            # 상품 이름이 없는 경우 문제가 발생한 것으로 판단하고 다음 상품 진행
            if not price:
                self._logger.warning('No product name: {}'.format(slink))
                continue

            product_data = {
                "name": name,
                "color": color,
                "price": price,
                "url": slink
            }
            self.add_meta(product_data)

            # 이미지 영역 추출
            img_elements = self._driver.find_elements_by_css_selector('#main-images > div > a > img.image-big._img-zoom._main-image')

            # 이미지 다운로드
            i = 0
            for img_el in img_elements:
                try:
                    # 자라의 경우 base64 로딩 이미지를 보여주다가,
                    # 이미지가 로드되면 기존 src 대체함.
                    # => src 속성에 있던 base64 값이 사라짐
                    self._wait.until(
                        attr_must_fn('src', lambda a: not a.find('base64') != -1, el=img_el)
                    )
                except Exception as e:
                    self._logger.error(f'Image load failed: {e}')
                    continue

                img_src = img_el.get_attribute('src')
                img_file_name = self.get_image_filename(product_data['name'], color=product_data['name'], num=(i + 1))
                self.save_image(img_src, img_file_name)

        self.save_meta()


if __name__ == "__main__":
    save_path  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/")

    p_args = {}
    p_args['job_id'] = '1'
    p_args['site_url'] = 'https://www.zara.com/kr/ko/woman-event-l1053.html?v1=1478211'
    p_args['brand'] = 'zara'
    p_args['brand_nm'] = 'zara'
    p_args['product_sex'] = 'w'
    p_args['product_categori'] = 'test'
    
    ZARAModule(p_args).start()
