import time
import subprocess
import sys

i = 1
while i > 0:
    time.sleep(10)
    etcd = subprocess.Popen('scrapy crawl linkedincrawl', close_fds = True)
    i -= 1
    time.sleep(1800)
    if etcd.poll() is None:
        etcd.kill()
        print 'timed out'
