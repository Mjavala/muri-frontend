import time
import datetime
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import sys

def device_logger(device_list, id, message):
    #if the device is streaming and there is no logger created
    for i in device_list:
        if id in device_list and id not in logging.root.manager.loggerDict:
            #create a logger
            logger = device_log_setup(id)
            logger.info(message)
        elif id in device_list and id in logging.root.manager.loggerDict:
            #logger exists
            logger = logging.getLogger(id)
            logger.info(message)
        elif id not in device_list:
            raise

def device_log_setup(id):
    daily_path,  hourly_path = build_dir(id)


    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

    handler_daily = TimedRotatingFileHandler( daily_path + 'log', 
                                    when= 'D',
                                    backupCount = 7 )
    handler_hourly = TimedRotatingFileHandler( hourly_path + 'log', 
                                    when= 'H',
                                    backupCount = 24 )    

    handler_hourly.setFormatter(formatter)
    handler_daily.setFormatter(formatter)

    logger = logging.getLogger(id)
    logger.addHandler(handler_hourly)
    logger.addHandler(handler_daily)
    logger.setLevel(logging.INFO)

    return logger

def build_dir(id):
    
    # config to your directory structure
    path_hourly = './logs/{0}/hourly/'.format(id)
    path_daily = './logs/{0}/daily/'.format(id)

    try:
        os.makedirs(path_hourly, mode=0o777, exist_ok=True)
        os.makedirs(path_daily, mode=0o777, exist_ok=True)

    except OSError as e:
        sys.exit("Can't create dir: {err}".format(err=e))
  

    return path_daily, path_hourly