# -*- coding:utf-8 -*-
import warnings
warnings.filterwarnings("ignore")
# from mpl_finance import candlestick_ohlc
import matplotlib.finance as mpf
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
import pandas as pd


class HqPics(object):
    DIR = 'D:/Kmoder/images'
    H5='D:/widetable/h5data/SHSZ_1DAY_HIS.h5'
    def __init__(self, fromdt=None, todt=None, klen=7, obvlen=21):
        self.fromdt = fromdt
        self.todt = todt
        self.klen = klen
        self.obvlen = obvlen
        self.hdr = HDFsReader(fn=self.H5)
        self.codes = []
        self.datadir = None

    def set_windows_len(self, klen, obvlen):
        self.klen = klen
        self.obvlen = obvlen
        self.datadir = self.DIR+'/'+'K{}F{}'.format(self.klen, self.obvlen)
        if not os.path.exists(self.datadir) and self.klen>0:
            try:
                os.makedirs(self.datadir)
            except Exception as _:
                print(_)
            else:
                print('mkdir:', self.datadir)

    def set_dates(self, fromdt, todt):
        self.fromdt = fromdt
        self.todt = todt

    def get_codes(self):
        self.codes.clear()
        with open('ZZ800.txt','r') as f:
            src = f.readlines()
            for code in src:
                self.codes.append(code[:-1])
            
    def draw_png(self, secode, hqdata, dtlabel):
        maxlen = len(hqdata) - self.obvlen
        if maxlen < 1:
            return None
        else:
            for i in range(maxlen):
                fig = plt.figure(figsize=(1.0, 1.0))
                fig.subplots_adjust(bottom=0.0, left=0.0, right=1, top=1)
                ax = fig.add_subplot(111)
                ax.set_axis_off()
                mpf.candlestick_ohlc(ax, hqdata[i:i + self.klen], width=0.85, colorup='grey', colordown='black')
                fn = '{secode}_{st}_{et}_{maxrs}_{minrs}_{eofrs}.png'
                maxrs, minrs, eofrs = self.calc_chgpct(data=hqdata, m=i + self.klen - 1, n=i + self.klen + self.obvlen - 1)
                plt.savefig(self.datadir + '/' + fn.format(secode=secode,
                                                           st=dtlabel[i],
                                                           et=dtlabel[i + self.klen],
                                                           maxrs=maxrs,
                                                           minrs=minrs,
                                                           eofrs=eofrs))
                plt.cla()
                plt.close()
                if i % 10 == 0:
                    print('[', i, ']', end='', flush=True)
        print('\n')

    def calc_chgpct(self, data, m, n):
        print('m:n',m,n)
        cps = [line[4] for line in data[m:n]]
        print(cps)
        # maxrs = int((max(cps) / cps[0] - 1) * 100) / 5 * 5
        # minrs = int((min(cps) / cps[0] - 1) * 100) / 5 * 5
        # eofrs = int((cps[-1] / cps[0] - 1) * 100) / 5 * 5
        maxrs = round((max(cps) / cps[0] - 1) * 100, 2)
        minrs = round((min(cps) / cps[0] - 1) * 100, 2)
        eofrs = round((cps[-1] / cps[0] - 1) * 100, 2)
        return maxrs, minrs, eofrs
    
    def run(self):
        self.get_codes()
        if not self.datadir:
            print("Must set datadir by:\nself.set_windows_len(klen,obvlen)")
            return None
        i1,i2,i3,i4,i5 = self.fromdt,self.todt,self.klen,self.obvlen,self.datadir
        print('Run batch Task:\n Generate many pngs from h5 file \n From [{}] to [{}]\n KLen   :[{}]\n ObvLen :[{}]\n Datadir:[{}]'.format(i1,i2,i3,i4,i5))
        for code in self.codes:
            print("===%s===" % code)
            # if not os.path.exists(HqPics.DIR + '/' + code):
                # print('mkdir:', self.datadir + '/' + code)
                # os.mkdir(self.datadir + '/' + code)
            self.hdr.set_pars(secode=code, fromdt=self.fromdt, todt=self.todt)
            flag = self.hdr.get_ohlc()
            if flag:
                self.draw_png(secode=code, hqdata=self.hdr.hqdata, dtlabel=self.hdr.dtlist)
        
        
class SqlDictReader(object):
    isql = "select {flds} from {tb} where Fcp!=0.00 and Fsecode='{secode}' and Ftdate>='{fromdt}' and Ftdate<='{todt}' order by Ftdate"

    def __init__(self, tb='t_his_hq', fieldnames=['Ftdate', 'Fop', 'Fhp', 'Flp', 'Fcp', 'Fpcp', 'Fvol', 'Fchgpct']):
        self.__tb = tb
        self.__fieldNames = fieldnames
        self.hqdata = []
        self.dtlist = []

    def set_pars(self, secode, cur, fromdt, todt):
        self.secode = secode
        self.reader = cur
        self.fromdt = fromdt
        self.todt = todt

    def get_data(self):
        self.hqdata = []
        self.dtlist = []
        self.isql = SqlDictReader.isql.format(flds=','.join(self.__fieldNames),
                                             tb=self.__tb,
                                             fromdt=self.fromdt,
                                             todt=self.todt,
                                             secode=self.secode)
        self.reader.execute(self.isql)
        _ = self.reader.fetchone()
        rs = self.reader.fetchall()
        if len(rs) == 0:
            raise Exception("No data! Check the sql:%s" % self.isql)
        print('Inner SqlDictReader len(rs): ', len(rs))
        cumfactor = 1.00
        for idx, row in enumerate(rs):
            if idx == 0:
                zrjs = row[4]
                cumfactor = 1.00
            else:
                jrzs = row[5]
                if jrzs != zrjs:
                    cumfactor *= float(zrjs / jrzs)
                zrjs = row[4]
            adjcp = round(float(row[4]) * cumfactor, 5)
            adjlp = round(float(row[3]) * cumfactor, 5)
            adjhp = round(float(row[2]) * cumfactor, 5)
            adjop = round(float(row[1]) * cumfactor, 5)
            tdate = row[0].strftime('%Y%m%d')
            self.hqdata.append((idx, adjop, adjhp, adjlp, adjcp))
            self.dtlist.append(tdate)
        return (self.hqdata, self.dtlist)


class HDFsReader(object):

    def __init__(self, fn='.', fieldnames=['open','high','low','close']):
        self.__fn = fn
        self.__fieldNames = fieldnames
        self.hqdata = []
        self.dtlist = []

    def set_pars(self, secode, fromdt, todt):
        self.secode = secode
        self.fromdt = fromdt
        self.todt = todt

    def get_ohlc(self):
        self.hqdata.clear()
        self.dtlist.clear()
        df = pd.read_hdf(path_or_buf=self.__fn,
                         key=self.secode,
                         columns=self.__fieldNames,
                         where=['index>=Timestamp("%s")'%self.fromdt,'index<=Timestamp("%s")'%self.todt])
        if df.empty:
            return False
        else:
            df = df.reset_index()
            for idx,row in df.iterrows():
                line = (idx,row['open'],row['high'],row['low'],row['close'])
                self.hqdata.append(line)
                dtlabel = row['index'].to_pydatetime().strftime('%Y%m%d')
                self.dtlist.append(dtlabel)
        print(self.dtlist)
        print(self.hqdata)
        return True



def all_run():
    hpcs = HqPics()
    hpcs.set_dates(fromdt='2018-01-01', todt='2018-04-10')
    for klen in [5,6,7,8,9,10]:
        for obvlen in [klen,2*klen,3*klen]:
            hpcs.set_windows_len(klen, obvlen)
            hpcs.run()

def main():
    hpcs = HqPics()
    hpcs.set_windows_len(klen=7, obvlen=21)
    hpcs.set_dates(fromdt='2018-01-01', todt='2018-04-10')
    hpcs.run()


if __name__ == '__main__':
    all_run()
