# coding: UTF-8

import threading
import time

threadlock = threading.Lock()
def runme(txt):
    threadlock.acquire()
    print 'In thread safe function:', txt
    threadlock.release()

def partition(lst, n):
    """
    Given lst, n, partition lst into n nearly equal partitions
    """
    return [lst[i::n] for i in xrange(n)]

class GetProfiles:
    class GetProfile(threading.Thread):
        def __init__(self, profile_list):
            threading.Thread.__init__(self)
            self.profile_list = profile_list
            self.threadlock = threading.Lock()
        def run(self):
            print "Starting " + str(self.profile_list)
            for profile in self.profile_list:
                counter = 0
                while counter < 10:
                    from random import randint
                    time.sleep(randint(1,3))
                    counter += 1
                    runme('Thread %s %s' % (profile, counter))
        
    def __init__(self, profiles, threads):
        self.profiles = profiles
        self.threads = threads
        self.thread_list = []
    def start(self):
        print self.profiles, self.threads
        for profile_list in partition(self.profiles, self.threads):
            self.getProfileList(profile_list)
    def getProfileList(self, profiles):
        t = self.GetProfile(profiles)
        t.start()
        self.thread_list.append(t)

