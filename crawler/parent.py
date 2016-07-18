import time
import subprocess
import sys


while 1:
    time.sleep(10)
    etcd = subprocess.check_call('scrapy crawl linkedincrawl', close_fds = True)
    print etcd
