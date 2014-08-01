from abc import ABCMeta
import sys
import time

from maioget.parse_args import parse_args
from maioget.threads import GetProfiles
from maioget.threads import ProfileThread

class MaioGetBase:
    __metaclass__ = ABCMeta
    
    def __init__(self, *args, **kwargs):
        self.args = list(args)
        self.kwargs = dict(kwargs)
    
    def main(self):
        print "Hi, welcome to MaioGet!"
        print "args:", self.args
        print "kwargs:", self.kwargs
        profiles = ['profile_'+str(num) for num in range(5)]
        print profiles
        #getprofiles = GetProfiles(profiles, int(self.kwargs.get('threads', 5)))
        try:
            getprofiles = ProfileThread(profiles, int(self.kwargs.get('threads', 5)))
            getprofiles.start()
        except KeyboardInterrupt, e:
            print "Got interrupt!"
            print "Killing threads..."
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
            print "Got second interrupt!"
            print "Killing all threads..."
            getprofiles.kill_all_threads = True
        print 'Exiting main thread!'
    
    def command_line(self):
        return self.main()

