# coding: UTF-8

import threading
import time
import Queue
from random import randint
import sys

#########################################################################

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

class GetProfile(threading.Thread):
    def __init__(self, profile_list):
        threading.Thread.__init__(self)
        self.profile_list = profile_list
        self.threadlock = threading.Lock()
    def run(self):
        print "Starting " + str(self.profile_list)
        for profile in self.profile_list:
            counter = 0
            while counter < 5:
                time.sleep(randint(1,3))
                counter += 1
                runme('Thread %s %s' % (profile, counter))

class GetProfiles():
    def __init__(self, profiles, threads):
        self.profiles = profiles
        self.threads = threads
        self.thread_list = []
    def start(self):
        print self.profiles, self.threads
        for profile_list in partition(self.profiles, self.threads):
            self.getProfileList(profile_list)
    def getProfileList(self, profiles):
        t = GetProfile(profiles)
        t.start()
        self.thread_list.append(t)

#########################################################################

_print_lock = threading.Lock()
def _print(*args):
    with _print_lock:
        for arg in args:
            print str(arg)+" ",
        print ""

class ProfileThread():
    def __init__(self, profiles, threads):
        self.profiles = profiles
        self.threads = threads
        self.thread_list = []
        self.thread = None
        self.queue = Queue.Queue()
        self.kill_all_threads = False
    #def do_work(self, profile):
    #    _print("In ProfileThread.do_work => Profile", profile)
    #    pages = ['page_'+str(num) for num in range(4)]
    #    _print(pages)
    #    getpages = PagesThread(profile, pages, self.threads)
    #    etpages.start()
    def test_work(self, *args, **kwargs):
        id = args[0]
        profile = args[1]
        for i in xrange(0, 2):
            if self.kill_all_threads:
                break
            num = randint(1,1)
            _print("Thread ID:", id, "Profile:",profile,">> Doing work for", num, "seconds")
            time.sleep(num)
    def worker(self, id):
        while not self.kill_all_threads:
            try:
                profile = self.queue.get(True, 1)
                _print("Profile:", profile)
                self.test_work(id, profile)
                self.queue.task_done()
            except Queue.Empty, e:
                return
    def start(self):
        for num in range(self.threads):
            t = threading.Thread(target=self.worker, args=(num,))
            t.start()
            self.thread_list.append(t)
        for profile in self.profiles:
            self.queue.put(profile)
        for thread in self.thread_list:
            _print("Hi!")
            thread.join(0.001)

#class PagesThread():
#    def __init__(self, profile, pages, threads):
#        self.profile = profile
#        self.pages = pages
#        self.threads = threads
#        self.thread_list = []
#        self.queue = Queue.Queue()
#    def do_work(self, page):
#        printthread("Profile "+self.profile)
#        printthread("In PagesThread.do_work => Page "+page)
#        images = ['image_'+str(num) for num in range(3)]
#        printthread(images)
#        #getimages = ImagesThread(self.profile, page, images, self.threads)
#        #getimages.start()
#        time.sleep(1)
#    def worker(self):
#        while True:
#            if not self.queue.empty():
#                page  = self.queue.get(True, 1)
#                self.do_work(page)
#                self.queue.task_done()
#            else:
#                time.sleep(0.2)
#    def start(self):
#        for i in range(self.threads):
#            thread = threading.Thread(target=self.worker)
#            thread.start()
#            self.thread_list.append(thread)
#        for page in self.pages:
#            self.queue.put(page)
#        try:
#            for t in self.thread_list:
#                t.join(1)
#        except KeyboardInterrupt, e:
#            print "KBI in PagesThread, killing"
#            raise

#class ImagesThread():
#    def __init__(self, profile, page, images, threads):
#        self.profile = profile
#        self.page = page
#        self.images = images
#        self.threads = threads
#        self.queue = Queue.Queue()
#    def do_work(self, image):
#        printthread("Profile "+self.profile+", Page "+self.page)
#        printthread("In ImagesThread.do_work => Image "+image)
#        time.sleep(randint(1,2))
#    def worker(self):
#        while True:
#            if not self.queue.empty():
#                image  = self.queue.get(True, 1)
#                self.do_work(image)
#                self.queue.task_done()
#            else:
#                time.sleep(0.2)
#    def start(self):
#        self.thread = threading.Thread(target=self.worker)
#        self.thread.daemon = False
#        self.thread.start()
#        for image in self.images:
#            self.queue.put(image)
#        self.queue.join()

