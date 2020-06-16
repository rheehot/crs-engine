#-*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2020, GHLEE.
# All rights reserved.

'''
크롤러 공통 모듈 클래스
 - 로그 기록 표준화
 - 에러 처리 표준화
 - 반복 기능 최소화

XXXModule extends CrawlingModule
    start(): 크롤링 시작 메소드
      - 오버라이드한 get_data 메소드 호출함
      - 데이터 수집 로직 에러 핸들링
    get_data(): 웹 페이지에 따라 직접 구현
      - [!!!필수!!!] 데이터 수집 로직 구현 (오버라이드)

    ############ 내부적으로 구현된 메소드 ############
    add_meta(): 메타 정보 리스트에 추가
    save_meta(): 메타 정보 리스트 CSV 파일로 저장
    save_image(): 이미지 다운로드
    sleep(): 스레드 대기
'''
import os
import csv
import time
import datetime
import traceback
from urllib.request import urlopen, Request
from app.common.custom_ec import get_webdriver_wait
from app.common.util import to_valid_filename
from app.common import get_logger, get_driver

class NotImplementedError(Exception):
    def __init__(self, msg):
        super(msg)

class CrawlingModule:
    '''
    크롤러 공통 모듈 클래스
    - 로그 기록 표준화
    - 에러 처리 표준화
    - 반복 기능 최소화

    Attributes
    ----------
        None(Private)


    Methods
    ----------
        start()
            오버라이드하여 구현된 get_data() 메소드 호출
        
        get_data()
            !!!중요!!! 브랜드 페이지별 데이터 수집 로직 구현 (오버라이드)
        
        add_meta(메타정보)
            상품 메타 정보 리스트에 추가
            [형식]
            - name: 상품명
            - color: 색상
            - price: 가격
            - url: 상품 정보 페이지 URL

        save_meta()
            메타 정보 리스트에 수집했던 데이터 CSV 파일로 저장
        
        save_image(이미지 소스, 파일명)
            이미지 다운로드 후 저장

        sleep(초)
            지정된 시간(초)만큼 스레드 대기
            - 타겟 서버 부하 방지
            - 데이터 로드 대기
            등..
        
        close()
            get_data() 작업 완료 후 리소스 정리
            - start() 메소드에서 자동 호출하므로 명시적으로 사용하지 않아도 됨
    '''
    def __init__(self, config):
        self._logger = get_logger(config['brand'], config['job_id'])
        self._driver = get_driver()
        self._wait = get_webdriver_wait(self._driver, timeout=10)
        self._COLLECT_DATE_ = datetime.datetime.now().strftime('%Y%m%d')
        self._meta_list = []
        self._count = 0
        self._config = config

        # CSV File
        job_id = config['job_id']
        save_path = config['save_path']
        brand = config['brand']
        product_sex = config['product_sex']
        categori = config['product_categori']
        self._csv_file = f'{self._COLLECT_DATE_}_{product_sex}_{brand}_{categori}_{job_id}.csv'
        self._info_path = f'{save_path}info/{brand}/'
        
        # Image File
        self._image_path = f'{save_path}images/{brand}/'
        self._logger.info(f'__init__ :: csv={self._csv_file}')

    def start(self):
        '''
        크롤링 작업 시작
         - get_data() 메소드 호출 및 에러 핸들링 포함
        '''
        try:
            self.get_data()
        except Exception as e:
            self._logger.error(f'CRITICAL ERROR :: {e}')
            traceback.print_stack()
        finally:
            self.close()


    def get_data(self, args, save):
        '''
        브랜트 웹 페이지별 데이터 수집 로직 구현 (오버라이드 필수)
        '''
        raise NotImplementedError('CrawlingModule :: get_data()')


    def add_meta(self, meta):
        '''
        상품 정보 리스트에 정보 추가

        Parameters
        =========
            meta : object
                상품 메타 정보
                 - name: 상품명
                 - color: 상품 색상
                 - price: 상품 가격
                 - url: 상품 페이지 URL
        '''
        name = meta['name']
        color = meta['color']
        price = meta['price']
        url = meta['url']
        self._meta_list.append(meta)
        self._logger.info(f'Metadata added :: ({name}, {color}, {price}) from {url}')


    def save_meta(self):
        '''
        상품 정보 리스트에 존재하는 데이터 CSV 파일로 저장
        '''
        self._logger.info(f'Save rows :: {len(self._meta_list)}')
        with open(os.path.join(self._info_path, self._csv_file), mode='a', encoding='utf-8') as f:
            product_writer = csv.writer(f)

            for meta in self._meta_list:
                product_writer.writerow([meta['name'], meta['color'], meta['price'], meta['url']])

        self._logger.info('Metadata :: Saved!')


    def get_image_filename(self, product_name, color='', num=0):
        '''
        저장할 이미지 파일명 생성

        Parameters
        ==========
            product_name : str
                제품명

            color : str
                제품 색상
            
            num : int
                여러 이미지가 존재하는 경우를 위한 구분 번호 (기본값: 0)
        '''
        color_str = f'({color})_' if bool(color) and color != 'unknown' else '_'
        return to_valid_filename(
            self._COLLECT_DATE_ + '_' + \
            self._config['product_sex'] + '_' + \
            self._config['brand_nm'] + '_' + \
            self._config['product_categori'] + '_' + \
            product_name + color_str + str(num) + '.jpg'
        )


    def save_image(self, src, filename):
        '''
        지정된 소스의 이미지 다운로드 후 저장

        Parameters
        =========
            src : str
                이미지 소스
            
            filename : str
                저장할 이미지 파일 명
        '''
        try:
            filename = os.path.join(self._image_path, filename)
            req = Request(src, headers={'User-Agent': 'Mozilla/5.0'})
            res = urlopen(req).read()

            with open(filename, 'wb') as f:
                f.write(res)

            self._logger.info(f'Image saved :: {filename}')
            self._count += 1
        except Exception as e:
            self._logger.error(f'Image save failed :: {e} - {src}')


    def sleep(self, second=5):
        '''
        크롤링 프로세스 일시 블로킹

        Parameters
        ========
            second : int
                블로킹할 시간 (초) - 기본값: 5

        '''
        self._logger.info(f'Sleep :: {second} sec..')
        time.sleep(second)


    def close(self):
        '''
        셀레니움 리소스 정리
        '''
        self._logger.info(f'Close :: Total image(s): {self._count} / Meta: {len(self._meta_list)}')
        try:
            self._driver.quit()
        except:
            pass
