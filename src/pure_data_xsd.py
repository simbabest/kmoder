# -*- coding:utf-8 -*-

import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine

# conn = create_engine('mysql+mysqldb://root:password@localhost:3306/databasename?charset=utf8')  

RAWTS = 'D:/widetable/h5data/SHSZ_RAWTS_HIS.h5'


def df_col_max(c1, c2):
    if c1 > c2:
        return c1
    else:
        return c2


def df_col_min(c1, c2):
    if c1 < c2:
        return c1
    else:
        return c2

class DB():
    def __init__(self,user="root",pswd="111111",host="10.6.10.184",db="fight"):
        self.user = user
        self.pswd = pswd
        self.host = host
        self.db = db
        self.con=None
        self.cur=None
        self.Flag = False
    def __del__(self):
        if self.con:
            self.con = None

    def set_pars(self,user="root",pswd="111111",host="10.6.10.184",db="fight"):
        self.user = user
        self.pswd = pswd
        self.host = host
        self.db = db

    def _create_engine_(self):
        cnnstr = 'mysql+mysqldb://{u}:{p}@{h}:3306/{db}?charset=utf8'.format(u=self.user,p=self.pswd,h=self.host,db=self.db)
        try:
            self.con = create_engine(cnnstr)
        except Exception as _:
            print('Create engine to [', self.host, '] failed! ')
            print('ErrorCode: ',_)
        else:
            print('Created!')
            self.Flag = True

    def _db_con_(self):
        if not self.Flag:
            try:
                self.con = pymysql.connect(database=self.db,
                                           user=self.user,
                                           password=self.pswd,
                                           host=self.host,
                                           charset="utf8")
            except Exception as _:
                print('Connecting to MySql [', self.host, '] failed! ')
                print('ErrorCode: ',_)
            else:
                print('Connected')
                self.Flag = True
        

class HDFsReader(DB):

    def __init__(self, fn='.', fieldnames=['open', 'high', 'low', 'close']):
        super(HDFsReader, self).__init__()
        self.__fn = fn
        self.__fieldNames = fieldnames
        self.hqdata = []
        self.dtlist = []
        self.tb = 'shape_mode_k7f3'
        self._create_engine_()
        print(self.con)
        self.droplist=['_r_cpf'+str(x)+'_'+str(y) for x in [1,2,3] for y in [1,2,3,4,5,6]]

    def set_pars(self, secode, fromdt, todt):
        self.secode = secode
        self.fromdt = fromdt
        self.todt = todt

    def get_k_mode(self):
        self.hqdata.clear()
        self.dtlist.clear()
        df = pd.read_hdf(path_or_buf=self.__fn,
                         key=self.secode,
                         # columns=self.__fieldNames,
                         where=['index>=Timestamp("%s")' % self.fromdt, 'index<=Timestamp("%s")' % self.todt])
        if df.empty:
            return False
        else:
            df = df.reset_index()
            df.sort_values(by='tdate', ascending=False, inplace=True)
            df['Fchg'] = df['Fcp'].shift(-1)
            df['Fchgpct'] = df['Fpcp'] / df['Fchg']
            df['Fchgpct'] = df['Fchgpct'].shift(1)
            df['Fchgpct'] = df['Fchgpct'].fillna(1.00)
            df['Fq'] = df['Fchgpct'].cumprod()
            for c in ['Fop', 'Fhp', 'Flp', 'Fcp']:
                df[c] = df[c] * df['Fq']
            df['Fvol'] = df['Fvol'] / df['Fq']
            df['Fvols'] = df['Fvol'].shift(-1)
            df['_r_cpf1'] = df['Fcp'] / df['Fcp'].shift(1) - 1.0
            df['_r_cpf2'] = df['Fcp'] / df['Fcp'].shift(2) - 1.0
            df['_r_cpf3'] = df['Fcp'] / df['Fcp'].shift(3) - 1.0
            for c in ['Fop', 'Fhp', 'Flp', 'Fcp']:
                df['_r_' + c] = df[c] / df['Fpcp'] - 1.0
            df['_r_'+'Fvol']= df['Fvol'] / df['Fvols'] -1.0
            df['_r_maxco'] = df[['_r_Fcp', '_r_Fop']].apply(lambda row:df_col_max(row['_r_Fcp'], row['_r_Fop']), axis=1)
            df['_r_minco'] = df[['_r_Fcp', '_r_Fop']].apply(lambda row:df_col_min(row['_r_Fcp'], row['_r_Fop']), axis=1)
            usecol = ['_r_' + c for c in ['Fop', 'Fhp', 'Flp', 'Fcp', 'Fvol', 'maxco', 'minco','cpf1','cpf2','cpf3']]
            usecol.insert(0, 'tdate')
            df = df.loc[:, usecol].dropna()
            #print(df)
            nrow, _ = df.shape
            print(nrow)
            dfs = pd.DataFrame()
            for nr in range(1, nrow - 6):
                dfm = df.loc[range(nr, nr + 7), :].copy()
                dfm['mkdate'] = max(dfm['tdate'].values)
                #print(dfm)
                dfm['tdate'] = [str(i) for i in range(1, 8)]
                dfm.set_index(keys=['mkdate', 'tdate'], inplace=True)
                dfm = dfm.unstack()
                dfm.columns = ['_'.join(col) for col in dfm.columns]
                dfm.drop(labels=self.droplist,axis=1,inplace=True)
                dfs = pd.concat(objs=[dfs, dfm], axis=0)
                dfs = dfs.round(4)
            #print(dfs)
            dfs['secode'] = self.secode
            se = dfs['secode']
            dfs.drop(labels=['secode'], axis=1,inplace = True)
            dfs.insert(0, 'secode', se)
            try:
                dfs.to_sql(name=self.tb, con=self.con,if_exists='append')
            except Exception as _:
                print('Error',_)
            else:
                print('Inserted to db',self.secode)

        return True


def main():
    hdr = HDFsReader(fn=RAWTS)
    for code in ['SZ002434','SZ300113','SZ000970','SZ000975']:
        hdr.set_pars(secode=code, fromdt='2018-01-01', todt='2018-04-10')
        hdr.get_k_mode()


if __name__ == '__main__':
    main()
