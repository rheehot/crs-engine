#-*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2020, GHLEE.
# All rights reserved.

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
        return getattr(o, key)
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
