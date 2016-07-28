import urllib
from pymongo import MongoClient
import datetime
import os
client = MongoClient('localhost', 27017)
db = client['linkedin']
today = str(datetime.date.today())

def downjpg(filepath, hash_url):

    FileName = '/%s.jpg' % (hash_url)
    web = urllib.urlopen(filepath)
    jpg = web.read()
    DstDir = "D:/Test/src/demo/static/pic/company/"+today
    if not os.path.exists(DstDir):
        os.makedirs(DstDir)
    File = open(DstDir + FileName, "wb")
    File.write(jpg)
    File.close()
    image_paths = {"image_paths": 'company/'+ today + FileName}
    db.company.update({'idcompanyitem': hash_url}, {"$set": {"image_paths": image_paths}})



def main():
    #globals flist
    i = 0
    for c in db.company.find({'image_paths' : []}):
        print c
        if c['company_logo']:
            downjpg(c['company_logo'], c['idcompanyitem'])
        else:
            c.update({}, {"$set": {"image_paths": ['company/2016-07-26/cd7026ef971162c323611ddf604ac21d.jpg']}})
        i += 1
        print i

main()
#4690