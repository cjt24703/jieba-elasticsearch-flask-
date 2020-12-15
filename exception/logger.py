import sys,os
import logging
import datetime
import time

def build_logger(log_file):
    log_name = time.strftime("%Y%m%d", time.localtime())+'.txt'
    log_path = os.path.join(log_file,log_name)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.FileHandler(log_path))
    return logger