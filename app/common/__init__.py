import os
import sys
import logging
import logging.handlers
from selenium import webdriver
from app.common.comConfig import conf_info
from app.common import chromeSet

def get_logger(name, filename=None):
    if not filename:
        filename = conf_info.get('init').get('log_file')
    else:
        filename = name + '-' + filename + '.log'

    _format = conf_info.get('init').get('log_format')
    _log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../logs/', filename)
    logging.basicConfig(
        format=_format,
        level=logging.INFO,
        # level=logging.DEBUG
    )

    fileMaxByte = 1024 * 1024 * 5 #5MB
    streamHandler = logging.StreamHandler()
    logger = logging.getLogger(name)

    formatter = logging.Formatter(_format)
    file_handler = logging.handlers.RotatingFileHandler(filename=_log_file,maxBytes=fileMaxByte, backupCount=10)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def get_driver():
    driver = webdriver.Chrome(executable_path=chromeSet.DRIVER_PATH, options=chromeSet.options)
    # 웹 페이지 로딩 시 3초간 대기함 (셀레니움 암묵적 대기)
    driver.implicitly_wait(3)
    return driver
