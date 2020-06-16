#-*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2020, GHLEE.
# All rights reserved.

import re

def ref_safe(o, key, default=''):
    '''
    안전한 속성 접근 처리 함수

    Parameters
    ----------
        o : object
            속성 접근 대상 객체
        idx : int
            접근할 속성명
        default: any
            해당 객체의 속성에 접근할 수 없는 경우 반환할 기본값
    '''
    try:
        v = getattr(o, key)
        if v:
            return v
        else:
            return default
    except:
        return default

def idx_safe(o, idx, default=''):
    '''
    안전한 인덱스 접근 처리 함수

    Parameters
    ----------
        o : object
            인덱스 접근 대상 객체 (리스트)
        idx : int
            접근할 인덱스
        default: any
            해당 객체의 인덱스에 접근할 수 없는 경우 반환할 기본값
    '''
    try:
        return o[idx]
    except:
        return default

def is_iterable(o):
    '''
    대상이 이터러블 객체인지 판별

    Parameters
    ----------
        o : object
            이터러블 확인 대상 객체
    '''
    try:
        _ = (e for e in o)
        return True
    except:
        return False

def to_valid_filename(s):
    '''
    지정된 문자열을 저장 가능한 파일명으로 수정
    (일부 특이한 문자가 포함되어있는 경우 저장시 예외가 발생할 수 있음)

    Parameters
    ----------
        s : str
            변환할 파일명
    '''
    s = re.sub(r'\/', ',', s)
    return re.sub(r'[^a-zA-Z0-9가-힣.,\(\)]', '_', s)
