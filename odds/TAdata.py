# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
Header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
czceUrl = 'http://www.czce.com.cn'
session = requests.Session()
contractUrl='http://www.czce.com.cn/portal/DFSStaticFiles/Future/2018/{tdate}/FutureDataTrdhedge.txt'
# import urllib2
# fp = urllib2.urlopen(url=url)
# print fp.read()
try:
    session.get(czceUrl)
except Exception as _:
    print 'Connect to Czce Failed @ on __init__'
else:
    print 'Connect to Czce Success @ on __init__'

fw=open('FutureDataTrdhedge.csv','a')

for tdate in ['20180416','20180417','20180418','20180419','20180420','20180423','20180424']:
    r=session.get(url=contractUrl.format(tdate=tdate))
    src = r.text.encode('latin1').decode('gbk')
    lines = src.split('\n')
    for line in lines[2:]:
        nline = line[:-1].replace(' ','').replace(',','')
        nlist = nline.split('|')
        if len(nlist)>1:
            nlist.insert(0,tdate)
            fw.write(','.join(nlist)+'\n')
fw.close()
        