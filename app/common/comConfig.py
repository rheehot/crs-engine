#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Copyright 2020, IMCLOUD Inc.
# All rights reserved.


import os
import json

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

import six
if six.PY2:
    import ConfigParser as configparser
else:
    import configparser

# 인스턴스 생성
config = configparser.RawConfigParser()


# 설정파일 읽기
if six.PY2:
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/config.cfg'))
else:
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../conf/config.cfg'), 'utf-8')


# 설정 정보 변수(JSON)
conf_info = {}
init_conf = {}
site_conf = {}
site_list_conf = {}

# 기본 설정 정보 읽기
if config.has_section('init') == True :
    init_conf['process'] = config.get('init', 'process')
    init_conf['interval_time'] = config.getint('init', 'interval_time')
    init_conf['log_file'] = config.get('init', 'log_file')
    init_conf['log_format'] = config.get('init', 'log_format')
    init_conf['chromedriver_path'] = config.get('init', 'chromedriver_path')
    

if config.has_section('stories') == True :
    site_conf['site'] = config.get('stories', 'site')
    site_conf['site_nm'] = config.get('stories', 'site_nm')
    site_conf['site_sex'] = config.get('stories', 'site_sex')
    site_conf['site_categori'] = config.get('stories', 'site_categori')
    site_list_conf['stories'] = site_conf
    site_conf = {}


if config.has_section('zara') == True :
    site_conf['site'] = config.get('zara', 'site')
    site_conf['site_nm'] = config.get('zara', 'site_nm')
    site_conf['site_sex'] = config.get('zara', 'site_sex')
    site_conf['site_categori'] = config.get('zara', 'site_categori')
    site_list_conf['zara'] = site_conf
    site_conf = {}


if config.has_section('hm') == True :
    site_conf['site'] = config.get('hm', 'site')
    site_conf['site_nm'] = config.get('hm', 'site_nm')
    site_conf['site_sex'] = config.get('hm', 'site_sex')
    site_conf['site_categori'] = config.get('hm', 'site_categori')
    site_list_conf['hm'] = site_conf
    site_conf = {}


if config.has_section('cos') == True :
    site_conf['site'] = config.get('cos', 'site')
    site_conf['site_nm'] = config.get('cos', 'site_nm')
    site_conf['site_sex'] = config.get('cos', 'site_sex')
    site_conf['site_categori'] = config.get('cos', 'site_categori')
    site_list_conf['cos'] = site_conf
    site_conf = {}
    
if config.has_section('netaporter') == True :
    site_conf['site'] = config.get('netaporter', 'site')
    site_conf['site_nm'] = config.get('netaporter', 'site_nm')
    site_conf['site_sex'] = config.get('netaporter', 'site_sex')
    site_conf['site_categori'] = config.get('netaporter', 'site_categori')
    site_list_conf['netaporter'] = site_conf
    site_conf = {}
    
    
if config.has_section('mathesfasion') == True :
    site_conf['site'] = config.get('mathesfasion', 'site')
    site_conf['site_nm'] = config.get('mathesfasion', 'site_nm')
    site_conf['site_sex'] = config.get('mathesfasion', 'site_sex')
    site_conf['site_categori'] = config.get('mathesfasion', 'site_categori')
    site_list_conf['mathesfasion'] = site_conf
    site_conf = {}
    
    
if config.has_section('asos') == True :
    site_conf['site'] = config.get('asos', 'site')
    site_conf['site_nm'] = config.get('asos', 'site_nm')
    site_conf['site_sex'] = config.get('asos', 'site_sex')
    site_conf['site_categori'] = config.get('asos', 'site_categori')
    site_list_conf['asos'] = site_conf
    site_conf = {}
    
    
if config.has_section('farfetch') == True :
    site_conf['site'] = config.get('farfetch', 'site')
    site_conf['site_nm'] = config.get('farfetch', 'site_nm')
    site_conf['site_sex'] = config.get('farfetch', 'site_sex')
    site_conf['site_categori'] = config.get('farfetch', 'site_categori')
    site_list_conf['farfetch'] = site_conf
    site_conf = {}
    
    
if config.has_section('wconcept') == True :
    site_conf['site'] = config.get('wconcept', 'site')
    site_conf['site_nm'] = config.get('wconcept', 'site_nm')
    site_conf['site_sex'] = config.get('wconcept', 'site_sex')
    site_conf['site_categori'] = config.get('wconcept', 'site_categori')
    site_list_conf['wconcept'] = site_conf
    site_conf = {}
    
    
if config.has_section('musinsa') == True :
    site_conf['site'] = config.get('musinsa', 'site')
    site_conf['site_nm'] = config.get('musinsa', 'site_nm')
    site_conf['site_sex'] = config.get('musinsa', 'site_sex')
    site_conf['site_categori'] = config.get('musinsa', 'site_categori')
    site_list_conf['musinsa'] = site_conf
    site_conf = {}
    
    
if config.has_section('wusinsa') == True :
    site_conf['site'] = config.get('wusinsa', 'site')
    site_conf['site_nm'] = config.get('wusinsa', 'site_nm')
    site_conf['site_sex'] = config.get('wusinsa', 'site_sex')
    site_conf['site_categori'] = config.get('wusinsa', 'site_categori')
    site_list_conf['wusinsa'] = site_conf
    site_conf = {}
    
    
if config.has_section('lfmall') == True :
    site_conf['site'] = config.get('lfmall', 'site')
    site_conf['site_nm'] = config.get('lfmall', 'site_nm')
    site_conf['site_sex'] = config.get('lfmall', 'site_sex')
    site_conf['site_categori'] = config.get('lfmall', 'site_categori')
    site_list_conf['lfmall'] = site_conf
    site_conf = {}
    
    
if config.has_section('ssfshop') == True :
    site_conf['site'] = config.get('ssfshop', 'site')
    site_conf['site_nm'] = config.get('ssfshop', 'site_nm')
    site_conf['site_sex'] = config.get('ssfshop', 'site_sex')
    site_conf['site_categori'] = config.get('ssfshop', 'site_categori')
    site_list_conf['ssfshop'] = site_conf
    site_conf = {}
    
    
if config.has_section('29cm') == True :
    site_conf['site'] = config.get('29cm', 'site')
    site_conf['site_nm'] = config.get('29cm', 'site_nm')
    site_conf['site_sex'] = config.get('29cm', 'site_sex')
    site_conf['site_categori'] = config.get('29cm', 'site_categori')
    site_list_conf['29cm'] = site_conf
    site_conf = {}
    
    
if config.has_section('thehandsome') == True :
    site_conf['site'] = config.get('thehandsome', 'site')
    site_conf['site_nm'] = config.get('thehandsome', 'site_nm')
    site_conf['site_sex'] = config.get('thehandsome', 'site_sex')
    site_conf['site_categori'] = config.get('thehandsome', 'site_categori')
    site_list_conf['thehandsome'] = site_conf
    site_conf = {}
    
conf_info['init'] = init_conf
conf_info['site'] = site_list_conf


# 설정 정보 출력(테스트)
def fn_conf_print():
    
    print(config.sections())
    print(init_conf)
    
    print(conf_info)
    print(conf_info.keys())
    print(conf_info.get('init'))
    
    print(site_list_conf)
    print(site_list_conf.keys())
    print(site_list_conf.get('stories'))
    print(site_list_conf.get('stories').get('site_nm'))
    print(site_list_conf.get('29cm').get('site_nm'))
    
    print(conf_info.get('site').keys())
    
# 테스트
if __name__ == '__main__':
    fn_conf_print()
