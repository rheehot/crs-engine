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


import app.common.userAction as userAction
from app.fsite import CrawlingModule
from app.common.util import ref_safe, idx_safe
from app.common.custom_ec import element_exist

class StoriesModule(CrawlingModule):
    def getData(self):
        self._driver.get(self._config['site_url'])
        
        # 마우스 스크롤 처리
        userAction.evtMouseDown(self._driver)
        
        elements = self._driver.find_elements_by_css_selector('#category-list > div > a > div.product-image > div')
        elements2 = self._driver.find_elements_by_css_selector('#category-list > div > a > div.description')
        
        # 상품 설명 추출
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

            self.add_meta({
                "name": product_name,
                "color": product_color,
                "price": product_price,
                "url": self._config['site_url']
            })
    
        i = 0
        # 상품 이미지 추출
        for el in elements:
            # 파일명 : 날짜_성별_브랜드_카테고리_상품명_번호
            current_meta = self._meta_list[i]
            img_file_nm = self.get_image_filename(current_meta['name'], color=current_meta['color'], num=(i + 1))
            el_product = el.find_elements_by_css_selector('img')
            el_product = idx_safe(el_product, 0)
            src = el_product.get_attribute('src')

            self.save_image(src, img_file_nm)
            i += 1

        self.save_meta()


if __name__ == "__main__":
    save_path  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/")
        
    p_args = {}
    p_args['job_id'] = '1'
    p_args['site_url'] = 'https://www.stories.com/kr_krw/whats-new/all.html'
    p_args['brand'] = 'stories'
    p_args['brand_nm'] = 'stories'
    p_args['product_sex'] = 'w'
    p_args['product_categori'] = 'new'

    StoriesModule(p_args).start()
