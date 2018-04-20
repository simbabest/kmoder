# -*- coding:utf-8 -*-
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from datetime import date, timedelta
import matplotlib.finance as mpf
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from xsalg import dHash, tHash, cmpHash, cmpHashNew
import glob
import cv2

PNGBASE = 'D:/Kmoder/images'
DAYH5 = 'D:/widetable/h5data/SHSZ_1DAY_HIS.h5'
TEMPDIR ='./temppic'

class KPNG(object):
    def __init__(self,secode='', dtlist=[], hqdata=[]):
        self.secode = secode
        self.dtlist = dtlist
        self.hqdata = hqdata
        self.fn = ''
        self.drawFlag = False
    def set_data(self,secode='',dtlist='',hqdata=''):
        self.secode = secode
        self.dtlist = dtlist
        self.hqdata = hqdata
    def get_fn(self):
        return self.fn
    def draw_png(self):
        fig = plt.figure(figsize=(1.0, 1.0))
        fig.subplots_adjust(bottom=0.0, left=0.0, right=1, top=1)
        ax = fig.add_subplot(111)
        ax.set_axis_off()
        mpf.candlestick_ohlc(ax, self.hqdata, width=0.85, colorup='grey', colordown='black')
        fntemplate = '{secode}_{st}_{et}.png'
        self.fn = TEMPDIR + '/' + fntemplate.format(secode=self.secode,
                                                    st=self.dtlist[0],
                                                    et=self.dtlist[-1])
        try:
            plt.savefig(self.fn)
        except Exception as _:
            self.drawFlag = False
        else:
            self.drawFlag = True


class KMODER(object):
    '''Kmoder :ts data,attr etc'''
    def __init__(self,secode='', klen=7):
        self.secode = secode
        self.klen = klen
        self.hqdata = []
        self.dtlist = []
        self.kpng=KPNG()

    def __str__(self):
        i1,i2,i3,i4 = self.secode,self.klen,self.kpng.fn,self.kpng.drawFlag
        return 'Class  : KMODER\nSecode : {}\nKlen   : {}\nPngFile:{}\nDrawFlag:{}'.format(i1,i2,i3,i4)
    def __del__(self):
        pass
    def get_moder(self):
        fieldNames = ['open','high','low','close']
        startdate = (date.today() - timedelta(days=50)).strftime('%Y-%m-%d')
        self.hqdata.clear()
        self.dtlist.clear()
        df = pd.read_hdf(path_or_buf=DAYH5,
                         key=self.secode,
                         columns=fieldNames,
                         where=['index>=Timestamp("%s")'%startdate])
        if df.empty:
            return False
        else:
            df = df.reset_index()
            df = df.tail(n=self.klen)
            for idx,row in df.iterrows():
                line = (idx,row['open'],row['high'],row['low'],row['close'])
                self.hqdata.append(line)
                dtlabel = row['index'].to_pydatetime().strftime('%Y%m%d')
                self.dtlist.append(dtlabel)
        self.kpng.set_data(secode=self.secode, dtlist=self.dtlist, hqdata=self.hqdata)
        self.kpng.draw_png()
        # print('Saved  :', self.kpng.fn)


class KMATHCHER(KMODER):
    '''--'''
    def __init__(self, secode='', klen=7, obvlen=21, thres=0.9):
        super(KMATHCHER, self).__init__(secode, klen)
        self.obvlen = obvlen
        self.thres = thres
        self.matchList = []
        self.dbLoc = PNGBASE + '/' + 'K{}F{}'.format(self.klen, self.obvlen)
    def __str__(self):
        fa_str_ = super(KMATHCHER, self).__str__().replace('KMODER', 'KMATHCHER')
        fa_str_ += '\nobvLen  :{}\ndbLoc   :{}\nThres   :{}'.format(self.obvlen,self.dbLoc,self.thres)
        return fa_str_

    def set_pars(self,secode, klen, obvlen, thres):
        self.secode = secode
        self.klen = klen
        self.obvlen = obvlen
        self.thres = thres
        self.dbLoc = PNGBASE + '/' + 'K{}F{}'.format(self.klen, self.obvlen)

    def run(self):
        self.get_moder()
        print(self)
        pngfn = glob.glob(self.dbLoc + '/*.png')
        pngfn.sort()
        data = []
        fn1 = self.kpng.fn
        d = []
        for fn2 in pngfn[:100]:
            img1=cv2.imread(fn1)
            img2=cv2.imread(fn2)
            hash1,hash2 = tHash(img=img1,m=32), dHash(img=img2,m=32)
            # print(hash1)
            # print(hash2)
            n = cmpHashNew(hash1,hash2)
            # print('均值哈希算法相似度：',n)
            v = round(1-n / (32*32*1.0), 4)
            code,st,et,mxrf,mnrf,edrf = fn2.replace('.png','').split('_')
            _,_,_,kf,secode = code.replace('\\','/').split('/')
            d.append((kf,secode,st,et,float(mxrf),float(mnrf),float(edrf),v))
        df = pd.DataFrame(data=d,columns=['KF', 'secode', 'st', 'et', 'mx','mn','ed','xsd'])
        print(df.loc[df['xsd']>self.thres,:])

def main():
#     kmd = KMODER(secode='SH600519', klen=7)
#     print(kmd)
#     kmd.get_moder()
    kmt = KMATHCHER(secode='SH600115', klen=5,obvlen=5,thres=0.4)
    kmt.run()


if __name__ == '__main__':
    main()