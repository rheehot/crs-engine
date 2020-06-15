#-*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2020, GHLEE.
# All rights reserved.

'''
커스텀 EC(expected_conditions) 모듈
'''
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_webdriver_wait(driver, timeout=5):
    '''
    명시적 대기를 위한 인스턴스 생성 및 반환

    Parameters
    ----------
    driver : selenium.webdriver
        셀레니움 드라이버
    timeout : int
        대기시간 (기본값: 5초)
    '''
    return WebDriverWait(driver, timeout)

class EC_or:
    '''
    다중 EC 조건 처리 (OR)
    '''
    def __init__(self, *args):
        self.ecs = args
    
    def __call__(self, driver):
        for ec in self.ecs:
            try:
                if ec(driver):
                    return True
            except:
                pass

class EC_and:
    '''
    다중 EC 조건 처리 (AND)
    '''
    def __init__(self, *args):
        self.ecs = args
    
    def __call__(self, driver):
        for ec in self.ecs:
            try:
                if not ec(driver):
                    return False
            except:
                pass
        else:
            return True

class text_is_not_empty:
    '''
    지정된 셀렉터 요소의 텍스트가 존재하는지 확인
    '''
    def __init__(self, selector):
        self.selector = selector

    def __call__(self, driver):
        try:
            element_text = EC._find_element(driver, (By.CSS_SELECTOR, self.selector)).text.strip()
            return element_text != ''
        except:
            return False

def text_is (selector, text):
    '''
    지정된 셀렉터에 해당하는 요소 텍스트가 text 인지 확인
    '''
    return EC.text_to_be_present_in_element((By.ByCssSelector, selector), text)

class attr_must_fn:
    '''
    지정된 셀렉터 요소의 변경된 속성 값 평가
    '''
    def __init__(self, attr, eval_fn, selector=None, el=None):
        self.selector = selector
        self.el = el
        self.attr = attr
        self.eval_fn = eval_fn

    def __call__(self, driver):
        try:
            if self.el:
                el_attr = self.el.get_attribute(self.attr)
            elif self.selector:
                el_attr = EC._find_element(driver, (By.CSS_SELECTOR, self.selector)) \
                    .get_attribute(self.attr)
            else:
                return False

            return self.eval_fn(el_attr)
        except Exception as e:
            return False

class element_exist:
    '''
    지정된 셀렉터 요소가 존재하는지 확인
    '''
    def __init__(self, selector):
        self.selector = selector
    
    def __call__(self, driver):
        try:
            el = EC._find_element(driver, (By.CSS_SELECTOR, self.selector))

            if isinstance(el, list):
                return len(el)
            else:
                return not not el
        except Exception as e:
            return False
