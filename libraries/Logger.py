import logging
from globals import *

class FII_Logger:
    @staticmethod
    def LogDEBUG(message):
        logging.basicConfig(filename=FIIConstants.LOG_FILE_PATH,level=logging.DEBUG,format='%(asctime)s %(message)s ',datefmt='%m/%d/%Y %I:%M:%S%p')
        logging.debug(message)
    @staticmethod
    def LogINFO(message):
        logging.basicConfig(filename=FIIConstants.LOG_FILE_PATH,level=logging.INFO,format='%(asctime)s %(message)s ',datefmt='%m/%d/%Y %I:%M:%S%p')
        logging.info(message)
    @staticmethod
    def LogWARNING(message):
        logging.basicConfig(filename=FIIConstants.LOG_FILE_PATH,level=logging.WARNING,format='%(asctime)s %(message)s ',datefmt='%m/%d/%Y %I:%M:%S%p')
        logging.warning(message)
#FII_Logger().LogDEBUG("Hello")
        