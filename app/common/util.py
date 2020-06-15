from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


'''
=============================================
셀레니움 관련 유틸 코드조각
'''

# 셀레니움 expected_conditions OR 조건 구현체
class EC_or:
    '''
    expected_conditions OR : Custom
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

class text_is_not_empty:
    '''
    지정된 셀렉터 요소의 텍스트가 존재하는지 확인 (EC)
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
    지정된 셀렉터에 해당하는 요소 텍스트가 text 인지 확인 (EC)
    '''
    return EC.text_to_be_present_in_element((By.ByCssSelector, selector), text)

class attr_must_fn:
    '''
    지정된 셀렉터 요소의 변경된 속성 값이 평가 (EC)
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
    지정된 셀렉터 요소가 존재하는지 확인 (EC)
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
