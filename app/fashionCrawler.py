#-*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2020, SEOK.
# All rights reserved.

__author__ = 'SEOK'

import os
import logging
import logging.handlers
import time
import csv
import datetime

from urllib.request import urlopen
import urllib.request

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing import Process, Queue, cpu_count, Pool

if __name__ == '__main__' and __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
from app.common.comConfig import conf_info
from app.fsite import stories, zara, hm


# _PROCESS_COUNT_ = cpu_count()
_PROCESS_COUNT_ = 2

_TEST_MODE_ = True

_SAVE_PATH_ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/")

class ImgCrawler():
    """
    이미지 크롤러

    Attributes
    ----------
    logger : Logger
        로거
    brand_list : list
        크롤링 대상 브랜드 목록

    brand_list_nm : object
        크롤링 대상 브랜드 목록

    brand_site_list : object

    brand_site_sex_list : object

    brand_site_categori_list : object

    site_total_count : int

    Methods
    -------
    init()
        크롤링 설정 기준으로 초기 세팅 (데이터 저장 폴더 생성 등)

    crawler_task()
        브랜드별 크롤링 설정 매핑, 멀티프로세싱 풀 생성 및 작업 수행
    """
    
    
    def __init__(self):
        
        _log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs/", conf_info.get('init').get('log_file'))
        logging.basicConfig(
            format=conf_info.get('init').get('log_format'),
            level=logging.INFO,
            # level=logging.DEBUG,
            stream=sys.stderr)
            
        self.logger = logging.getLogger(__name__)
        
        fileMaxByte = 1024 * 1024 * 5 #5MB
        self.logger.addHandler(logging.handlers.RotatingFileHandler(filename=_log_file,maxBytes=fileMaxByte, backupCount=10))
        
        
        self.brand_list = conf_info.get('site').keys()
        self.brand_list_nm = {}
        self.brand_site_list = {}
        self.brand_site_sex_list = {}
        self.brand_site_categori_list = {}
        
        self.site_total_count = 0
        for brand in self.brand_list:
            self.brand_list_nm[brand] = conf_info.get('site').get(brand).get('site_nm')
            self.brand_site_list[brand] = conf_info.get('site').get(brand).get('site').split(',')
            self.brand_site_sex_list[brand] = conf_info.get('site').get(brand).get('site_sex').split(',')
            self.brand_site_categori_list[brand] = conf_info.get('site').get(brand).get('site_categori').split(',')
            self.site_total_count += len(self.brand_site_list[brand])

    
    def init(self):
        
        try:
            s1 = datetime.datetime.now()
    
            self.logger.info('[ImgCrawler - init] START : ] ------------------------------------------')
    
            
            # 저장폴더 생성 (이미지, 태그정보)
            for brand in self.brand_list:
                
                images_path = _SAVE_PATH_ + 'images/' + brand
                info_path = _SAVE_PATH_ + 'info/' + brand
                
                # 브랜드별 상품 이미지 저장 폴더 생성
                if not os.path.exists(images_path):
                    os.makedirs(images_path)
                    
                # 브랜드별 상품 정보 저장 폴더 생성
                if not os.path.exists(info_path):
                    os.makedirs(info_path)
            
            
            # 크롤러 태스크 실행
            self.crawler_task()
                    
        except Exception as e:
            print('ERROR [ImgCrawler - init] !!!')
        finally:
    
            s2 = datetime.datetime.now()
    
            self.logger.info("\nStart Time : {}".format(s1))
            self.logger.info("End Time : {}".format(s2))
            self.logger.info("Time : {}".format(s2 - s1))
            self.logger.info('[ImgCrawler - init] END : ] ------------------------------------------')



    def crawler_task(self):
        
        s1 = datetime.datetime.now()
        self.logger.info("Start Time : %s" % s1)
        self.logger.info('\n\nJOB START ---------------------------------------------------------\n\n')
        
        work_result = Queue()
        process_obj = {}
        pool_args = []
        
        self.logger.info('\nTOTAL SITE URL COUNT ----------------------------------------------------[ %d ] \n' % (self.site_total_count))
        
        job_cnt = 0
        for brand in self.brand_list:
            
            # 테스트용 (특정 브랜드만 수행)
            if _TEST_MODE_ and brand not in ['hm']: # 'stories'
                continue
            
            scnt = 0
            for site_url in self.brand_site_list[brand]:
                tmp_data = {}
                tmp_data['site_url'] = site_url                                     # 크롤링 사이트
                tmp_data['job_id'] = 'WORK_JOB_' + str(job_cnt+1)                   # Job ID
                tmp_data['brand'] = brand                                           # Job Site(브랜드)
                tmp_data['brand_nm'] = self.brand_list_nm[brand]                    # Job Site(브랜드명)
                tmp_data['product_sex'] = self.brand_site_sex_list[brand][scnt]     # 상품 성별
                tmp_data['product_categori'] = self.brand_site_categori_list[brand][scnt]   # 상품 카테고리
                pool_args.append(tmp_data)
                scnt += 1
                job_cnt += 1
        
        self.logger.info('\nTOTAL JOB COUNT ---------------------------------------------------------[ %d ] \n' % (job_cnt))
        
        pool = Pool(_PROCESS_COUNT_)
        pool.map(do_work, pool_args)
        pool.close()
        pool.join()
        

        s2 = datetime.datetime.now()
        self.logger.info('\n\nJOB END -----------------------------------------------------------\n\n')
        self.logger.info("Start Time : %s" % s1)
        self.logger.info("End Time : %s" % s2)
        self.logger.info("Time : %s" % (s2 - s1))
    

def do_work(args):
    """
    이미지 크롤링 작업 수행

    Parameters
    ----------
    args : object
        크롤링 설정 객체
    """
    
    try:
        print('START_JOB ID: %s, %s' % (args['job_id'], args['brand_nm']))
        p_job_id = args['job_id']
        p_site_url = args['site_url']
        p_brand = args['brand']
        
        
        # 앤아더스토리즈 크롤링 모듈 호출
        if p_brand == 'stories':
            # stories.getData(p_site_url, _SAVE_PATH_, p_job_id)
            stories.getData(args, _SAVE_PATH_)

        # 자라 크롤링 모듈 호출            
        elif p_brand == 'zara':
            # zara.getData(p_site_url, _SAVE_PATH_, p_job_id)
            zara.getData(args, _SAVE_PATH_)
        
        # H&M 크롤링 모듈 호출            
        elif p_brand == 'hm':
            hm.getData(args, _SAVE_PATH_)
        
        # COS 크롤링 모듈 호출            
        elif p_brand == 'cos':
            pass
        
        # Net-A-Porter 크롤링 모듈 호출            
        elif p_brand == 'netaporter':
            pass
        
        # mathesfasion 크롤링 모듈 호출            
        elif p_brand == 'mathesfasion':
            pass
        
        # ASOS 크롤링 모듈 호출            
        elif p_brand == 'asos':
            pass
        
        # farfetch 크롤링 모듈 호출            
        elif p_brand == 'farfetch':
            pass
        
        # wconcept 크롤링 모듈 호출            
        elif p_brand == 'wconcept':
            pass
        
        # 무신사 크롤링 모듈 호출            
        elif p_brand == 'musinsa':
            pass
        
        # 우신사 크롤링 모듈 호출            
        elif p_brand == 'wusinsa':
            pass
        
        # LF몰 크롤링 모듈 호출            
        elif p_brand == 'lfmall':
            pass
        
        # ssfshop 크롤링 모듈 호출            
        elif p_brand == 'ssfshop':
            pass
        
        # 29cm 크롤링 모듈 호출            
        elif p_brand == '29cm':
            pass
        
        # 더한섬닷컴 크롤링 모듈 호출            
        elif p_brand == 'thehandsome':
            pass
        
    except Exception as ex:
            print('ERRPR [do_work] ID: %s, %s' % (args['job_id'], args['brand_nm']))
            print(ex)
    finally:
        print('END_JOB ID: %s, %s' % (args['job_id'], args['brand_nm']))
        
    
    
if __name__ == "__main__":

    crawler = ImgCrawler()
    crawler.init()