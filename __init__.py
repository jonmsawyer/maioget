from abc import ABCMeta
import sys
import time

from maioget.parse_args import parse_args
from maioget.threads import ProfileThread
import logger #exposes maioget.logger

def _t(*args):
    txt = ''
    for arg in args:
        txt += str(arg)+" "
    return txt

_log = None

class MaioGetBase:
    __metaclass__ = ABCMeta
    
    def __init__(self, *args, **kwargs):
        self.args = list(args)
        self.kwargs = dict(kwargs)

    def set_logger(self, logger):
        """
        Call this in derived class' Constructor to have logging set up properly
        """
        global _log
        self.logger = logger
        _log = self.logger
    
    def main(self):
        _log = self.logger
        _log.info("Hi, welcome to MaioGet!")
        _log.debug(_t("args:", self.args))
        _log.debug(_t("kwargs:", self.kwargs))
        profiles = ['profile_'+str(num) for num in range(5)]
        _log.info(_t("Profiles:", profiles))
        try:
            getprofiles = ProfileThread(profiles, int(self.kwargs.get('threads', 5)), self.logger)
            getprofiles.start()
        except KeyboardInterrupt, e:
            _log.debug("Got interrupt!")
            _log.debug("Killing threads...")
            getprofiles.kill_all_threads = True
        try:
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
        except KeyboardInterrupt:
            _log.debug("Got second interrupt!")
            _log.debug("Killing all threads...")
            getprofiles.kill_all_threads = True
        _log.debug('Exiting main thread!')
    
    def command_line(self):
        return self.main()

