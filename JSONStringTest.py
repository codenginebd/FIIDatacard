import threading
import time

downloadComplete = threading.Condition()
dataAvailable = threading.Condition()

def DownloadData():
    downloadComplete.acquire()
    print "Downloading Started."
    time.sleep(5)
    print "Downloading completed half."
    downloadComplete.notify()
    downloadComplete.release()
    time.sleep(10)
    print "Download Complete Total"
    
def Crawl():
    downloadComplete.acquire()
    downloadComplete.wait()
    print "Crawling Started."
    time.sleep(4)
    dataAvailable.acquire()
    dataAvailable.notify()
    time.sleep(3)
    print "Crawling Ended."
    dataAvailable.release()
    downloadComplete.release()
    
def Upload():
    dataAvailable.acquire()
    dataAvailable.wait()
    print "Upload Started."
    time.sleep(4)
    print "Upload Ended."
    dataAvailable.release()
    
threads = []

t3 = threading.Thread(target=Upload)
t3.start()
t2 = threading.Thread(target=Crawl)
t2.start()
t1 = threading.Thread(target=DownloadData)
t1.start()