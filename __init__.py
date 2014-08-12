from abc import ABCMeta
import sys
import os
import time
import signal

from maioget.parse_args import parse_args
from maioget.threads import ProfileThread
from logger import LogDirectoryException
import logger #exposes maioget.logger

def _t(*args):
    txt = ''
    for arg in args:
        txt += str(arg)+" "
    return txt

_log = None
_main_thread = None

class MaioGetBase:
    __metaclass__ = ABCMeta
    
    def __init__(self, *args, **kwargs):
        self.args = list(args)
        self.kwargs = dict(kwargs)
        self.logger_kwargs = {
            'directory': kwargs.get('logsdir', os.path.join('..', 'logs')),
            'name': 'maioget.%s' % (kwargs.get('name', 'UNNAMED'),),
            'daemon': kwargs.get('daemon', False),
            'loglevel': kwargs.get('loglevel', 'INFO'),
        }
        try:
            self.set_logger(logger.setup(**self.logger_kwargs))
        except LogDirectoryException:
            raise

    def set_logger(self, logger):
        global _log
        self.logger = logger
        _log = self.logger
    
    def main(self):
        global _log, _main_thread
        _log = self.logger
        _log.info("Hi, welcome to MaioGet!")
        _log.debug(_t("args:", self.args))
        _log.debug(_t("kwargs:", self.kwargs))
        profiles = ['profile_'+str(num) for num in range(5)]
        _log.info(_t("Profiles:", profiles))
        that = self
        getprofiles = ProfileThread(that, profiles)
        getprofiles.start()
        _main_thread = getprofiles
        empty = False
        while not empty:
            empty = getprofiles.queue.empty()
            time.sleep(0.2)
        threads_over = False
        while not threads_over:
            threads_over = True
            for t in getprofiles.thread_list:
                if t.is_alive():
                    threads_over = False
            time.sleep(0.2)
        _log.debug('Exiting main thread!')
    def command_line(self):
        return self.main()

def signal_handler(signum, frame):
    global _log, _main_thread
    if signum == 2:
        _log.error("Signal SIGINT Received!")
    elif signum == 1:
        _log.error("Signal SIGHUP Received!")
    elif signum == 15:
        _log.error("Signal SIGTERM Received!")
    _log.error("Killing all threads...")
    _main_thread.kill_all_threads = True

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)
