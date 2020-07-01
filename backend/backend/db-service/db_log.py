import time
import datetime
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import sys

def log_app(self, message, *args, **kws):
    """Log Handler for custom level (21), for Module Update Messages. Use instead of logger.info, since the info level is used heavily by included packages.

    :param message: The message to Log
    :type message: String

    """
    if self.isEnabledFor(logging.INFO+1):
        # Yes, logger takes its '*args' as 'args'.
        self._log(logging.INFO+1, message, args, **kws) 

def main_app_logs():
    #STD File Handler (hourly):
    logging.addLevelName(logging.INFO+1, "app_lvl")

    logger = logging.getLogger('app')
    logging.Logger.log_app = log_app
    logging.basicConfig(level=logging.INFO+1, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', filemode='a')
    log_file = "logs/app/app.log".format()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.handlers.TimedRotatingFileHandler(log_file,when="h",backupCount=24)    
    file_handler.setFormatter(formatter)                       
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)


def db_logs():
    #STD File Handler (hourly):
    logging.addLevelName(logging.INFO+1, "app_lvl")

    logger = logging.getLogger('db')
    logging.Logger.log_app = log_app
    logging.basicConfig(level=logging.INFO+1, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', filemode='a')
    log_file = "logs/db/db.log".format()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.handlers.TimedRotatingFileHandler(log_file,when="h",backupCount=24)    
    file_handler.setFormatter(formatter)                       
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
