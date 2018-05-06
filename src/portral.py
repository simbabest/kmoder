# -*- coding:utf-8 -*-

import pymysql
from datetime import date
import urllib.request as urllib2

rsUrl ='http://s.cf8.com.cn/statics/js/codes_utf8.js?ver={tdate}'


class PORTRAL(object):

    def __init__(self):
        self.code = None
        self.k = 0
        self.f = 0
        self.con = None
        self.cur = None
        self.dbFlag = False
        self.db = 'jswk'
        self.host = 'localhost'
        self.user = 'root'
        self.pswd = '10111011'
        self.fn = 'D:/Mysql_data/raw/t_stock_hq.csv'
        # self.fn = 'D:/Mysql_data/raw/test.csv'

    def get_k(self):
        pass

    def set_secode(self, code):
        self.code = code

    def set_k_f(self, k, f):
        self.k = k
        self.f = f

    def _db_con_(self):
        if not self.dbFlag:
            try:
                self.con = pymysql.connect(database=self.db,
                                           user=self.user,
                                           password=self.pswd,
                                           host=self.host,
                                           charset="utf8")
            except Exception as _:
                print('Connecting to MySql [', self.host, '] failed! ')
                print('ErrorCode: ', _)
            else:
                print('Connected')
                self.dbFlag = True

    def _import_csv(self):
        print(self.con)
        self.cur = self.con.cursor()
        with open(self.fn, 'r') as f:
            cnt = 0
            rtn = []
            while True:
                line = f.readline()
                if line:
                    cnt += 1
                    zz = line[:-1].split(',')
                    rtn.append(zz)
                    if cnt % 1000 == 0:
                        self._insert_lines(rtn,cnt)
                        rtn = []

                else:
                    self._insert_lines(rtn,cnt)
                    print('Eof')
                    break

    def _insert_lines(self, rtn,cnt):
        print(cnt)
        insql = 'insert into t_stock_hq values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self.cur.executemany(insql, rtn)
        except Exception as e:
            print(e)
            self.con.rollback()
        else:
            print('.')
            self.con.commit()

    def get_raw_by_web(self):
        self.cur = self.con.cursor()
        self.data = []
        todt = date.today().strftime('%Y%m%d')
        req = urllib2.Request(url = rsUrl.format(tdate=todt))
        try:
            fp = urllib2.urlopen(req).read()
        except Exception as e:
            print('get codes Failed:\n',e)
        else:
            print('get codes Success!')
            try:
                rs = eval(fp[12:-1].decode('utf8'))
                for row in rs:
                    row[0]='SH'+row[0] if row[0][0]=='6' else 'SZ'+row[0]
                    self.data.append(row)
                self.cur.executemany('insert into t_stock_pinyin values(%s,%s,%s)', self.data)
                self.con.commit()
            except Exception as e:
                print('cov Raw into list Failed \n',e)
def main():
    x = PORTRAL()
    x._db_con_()
    #x._import_csv()
    x.get_raw_by_web()

if __name__ == '__main__':
    main()
