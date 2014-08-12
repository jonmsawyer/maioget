import os
import sys
import logging
from logging import handlers

class LogDirectoryException(Exception):
    pass

def setup(directory=None,
          name=None,
          formatter=None,
          loglevel=None,
          rotatinglogsize=None,
          daemon=False,
          nofile=False
          ):
    # init config
    if not directory:
        directory = 'logs'
    if not os.path.isdir(directory):
        _msg = "Directory %s not found. Please create this directory" + \
               " or pass in the --logs-dir=LOGS_DIR flag into %s."
        _dir = os.path.realpath(os.path.join(os.getcwd(), directory))
        raise LogDirectoryException(_msg % (_dir, sys.argv[0]))
    
    if not name:
        name = __name__
    
    if not formatter:
        formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    if not loglevel:
        loglevel = logging.DEBUG
    else:
        loglevel = getattr(logging, loglevel.upper())
    
    if not rotatinglogsize:
        rotatinglogsize = 1024*1024*5
    # /end init config
    
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    
    # create formatter
    formatter = logging.Formatter(formatter)
    
    # create console handler
    if not daemon:
        ch = logging.StreamHandler()
        ch.setLevel(loglevel)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    
    # create a file handler
    if not nofile:
        fh = handlers.RotatingFileHandler("%s.log" % (os.path.join(directory, name),), 'a', rotatinglogsize)
        fh.setLevel(loglevel)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    return logger

