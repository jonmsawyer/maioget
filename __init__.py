from abc import ABCMeta

from maioget.parse_args import parse_args
from maioget.threads import GetProfiles

class MaioGetBase:
    __metaclass__ = ABCMeta
    
    def __init__(self, *args, **kwargs):
        self.args = list(args)
        self.kwargs = dict(kwargs)
    
    def main(self):
        print "Hi, welcome to MaioGet!"
        print "args:", self.args
        print "kwargs:", self.kwargs
        profiles = ['profile_'+str(num) for num in range(0, 10)]
        print profiles
        getprofiles = GetProfiles(profiles, int(self.kwargs.get('threads', 5)))
        getprofiles.start()
        for t in getprofiles.thread_list:
            t.join()
        print 'Exiting main thread!'
    
    def command_line(self):
        return self.main()

