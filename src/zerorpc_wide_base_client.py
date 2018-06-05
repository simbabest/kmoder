# -*- coding:utf-8 -*-
import cStringIO
#import cx_Oracle
import datetime
import pandas as pd
import pymysql
import zerorpc
usecols = ['tdate', 'index', 'open', 'high', 'low', 'current',
           'last_close', 'tr', 'volume', 'amount']
insql = {'ORACLE': "insert into T_STOCK_HQ(ftdate,fsecode,fop,fhp,flp,fcp,fpcp,ftr,fvol,famt) values(to_date(:1,'yyyy-mm-dd'),:2,:3,:4,:5,:6,:7,:8,:9,:10)",
         'MYSQL': "insert into t_stock_hq(ftdate,fsecode,fop,fhp,flp,fcp,fpcp,ftr,fvol,famt) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"}

isql = {'ORACLE': """select max(Ftdate) as mxdt
                      from (select Ftdate, count(*) as nums
                          from T_STOCK_HQ t
                             where Ftdate > to_Date('{tdate}', 'yyyy-MM-dd')
                             group by Ftdate) z""",
        "MYSQL": """SELECT    max(Ftdate) AS mxdt
                    FROM (SELECT Ftdate, count(*) AS nums
                        FROM T_STOCK_HQ t
                        WHERE Ftdate > '{tdate}'
                        GROUP BY Ftdate
                    ) z"""}


class DB(object):
    def __init__(self):
        self.conn = None
        self.cur = None

    def _connect_(self, dbtype):
        print(dbtype == 'ORACLE')
        if dbtype.upper() == 'MYSQL':
            self._con_to_mysql()
        elif dbtype.upper() == 'ORACLE':
            self._con_to_oracle()
        else:
            print('unsupported dbtype!')

    def _con_to_mysql(self):
        self.conn = pymysql.connect(database='jswk',
                                    user='root',
                                    password='10111011',
                                    host='127.0.0.1',
                                    port=3306,
                                    charset="utf8")
        self.cur = self.conn.cursor()

    def _con_to_oracle(self):
        self.conn = cx_Oracle.connect('simba/10111011@localhost:1521/Orcl')
        self.cur = self.conn.cursor()


class RPC2DB(DB):
    def __init__(self, dbtype=''):
        self.dbtype = dbtype
        self.c = zerorpc.Client()
        self.c.connect("tcp://120.24.75.77:3636")
        self.c.hello()
        self.dtlist = []

    def find_miss_date(self):
        ndts = datetime.datetime.now() - datetime.timedelta(days=60)
        ndtsfmt = ndts.strftime('%Y-%m-%d')
        self.cur.execute(isql.get(self.dbtype.upper()).format(tdate=ndtsfmt))
        mxdt = self.cur.fetchone()[0].strftime('%Y-%m-%d')
        mxdts = datetime.datetime.strptime(mxdt, '%Y-%m-%d')
        dttos = datetime.datetime.strptime(datetime.date.today().strftime('%Y-%m-%d'), '%Y-%m-%d')
        itv = dttos - mxdts
        self.dtlist = []
        if itv.days > 0:
            for i in range(itv.days):
                dt = mxdts + datetime.timedelta(days=i + 1)
                print(dt.strftime('%w'))
                if int(dt.strftime('%w')) > 0 and int(dt.strftime('%w')) < 6:
                    self.dtlist.append(dt.strftime('_%Y%m%d'))
        print(self.dtlist)

    def run(self):
        self._connect_(self.dbtype)
        self.find_miss_date()
        for tdate in self.dtlist:
            print(tdate)
            output = cStringIO.StringIO()
            try:
                data = self.c.get_hq_by_dt(tdate)
            except Exception as _:
                print('error')
            else:
                df = pd.read_json(data)
                df.reset_index(inplace=True)
                df = df[usecols]
                df = df.round(2)
                df.to_csv(output, sep='\t', index=False, header=False)
                output.getvalue()
                output.seek(0)
                lines = output.read().split('\n')
                zdata = []
                for line in lines:
                    nli = line.split('\t')
                    if len(nli) == 10:
                        zdata.append(nli)
                print(len(zdata))
                try:
                    self.cur.executemany(insql.get(self.dbtype), zdata)
                except Exception as e:
                    print('Error', e)
                    self.conn.rollback()
                else:
                    print(tdate, 'hq inserted!')
                    self.conn.commit()


def main():
    dbtype = 'MYSQL'
    r2d = RPC2DB(dbtype=dbtype)
    r2d.run()


if __name__ == '__main__':
    main()
