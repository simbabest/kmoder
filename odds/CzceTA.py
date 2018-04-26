# -*- coding:utf-8 -*-
import requests
from requests.exceptions import ConnectTimeout, ReadTimeout
from datetime import datetime, date, timedelta
from cmd import Cmd
Header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
czceUrl = 'http://www.czce.com.cn'
contractUrl = 'http://www.czce.com.cn/portal/DFSStaticFiles/Future/{yyyy}/{tdate}/FutureDataTrdhedge.txt'
csvfile = 'FutureTrdhedge.csv'

class CZCETA(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = ">"
        self.session = requests.Session()
        self.dlist = []

    def do_t(self, argv):
        '''测试网络连接情况:\n NetWork to http://www.czce.com.cn'''
        self.make_net_work()

    def make_net_work(self):
        try:
            self.session.get(url=czceUrl)
        except Exception as _:
            print('Failed Connect to Czce\nError:', _)
        else:
            print('Success Connect to Czce')

    def set_date(self, st, et):
        self.dlist = []
        st = st.replace('/', '').replace('-', '')
        et = et.replace('/', '').replace('-', '')
        dt1 = datetime.strptime(st, '%Y%m%d')
        dt2 = datetime.strptime(et, '%Y%m%d')
        tdays = (dt2 - dt1).days if dt2 > dt1 else (dt1 - dt2).days
        if tdays == 0:
            self.dlist = [st]
        else:
            for i in range(tdays):
                start = min([dt1, dt2])
                dt = start + timedelta(days=i)
                if dt.strftime('%w') in list('12345'):
                    self.dlist.append(dt.strftime('%Y%m%d'))

    def do_run(self, argv):
        '''支持三种运行方式:
1.不设定日期参数: 获取最近一个交易日数据|未收盘,上个交易日数据;收盘,当日数据
2.设定一个日期参数: 获取指定日期的数据
3.设定两个日期参数 :  获取两个日期之间的多个交易日的数据
-----------------------------------------
\trun
\trun yyyymmdd
\trun yyyymmdd yyyymmdd
-----------------------------------------'''
        print('Argv', argv)
        argvlist = argv.split(' ')
        if argv == '':
            tmp = []
            for i in range(7):
                dt = date.today() - timedelta(days=i)
                if dt.strftime('%w') in list('12345'):
                    tmp.append(dt.strftime('%Y%m%d'))
            print("Lastest Trading day is:", max(tmp))
            self.dlist = [max(tmp)]
        elif len(argvlist) == 1 and argv:
            print("You set the single day is:", argvlist[0].replace('/', '').replace('-', ''))
            self.set_date(argvlist[0], argvlist[0])
        else:
            print("You set the date range:\n",
                  "From", argvlist[0].replace('/', '').replace('-', ''),
                  'To', argvlist[1].replace('/', '').replace('-', ''))
            self.set_date(argvlist[0], argvlist[1])
        self.make_net_work()
        print('Datelist=[', ','.join(self.dlist), ']')
        fw = open(csvfile, 'a')
        for tdate in self.dlist:
            print(tdate)
            r = self.session.get(url=contractUrl.format(yyyy=tdate[:4], tdate=tdate))
            src = r.text.encode('latin1').decode('gbk')
            if src[:6] != '<html>':
                print(src)
                lines = src.split('\n')
                for line in lines[2:]:
                    nline = line[:-1].replace(' ', '').replace(',', '')
                    nlist = nline.split('|')
                    if len(nlist) > 1:
                        nlist.insert(0,tdate)
                        fw.write(','.join(nlist)+'\n')
            else:
                print('Error Page')
        fw.close()
        print("已完成, 数据存放于{csvfile} \n输入q/Q/exit/EXIT/quit/QUIT 可退出".format(csvfile=csvfile))

    def do_quit(self, argv):
        """EXIT ways:\n q Q exit EXIT quit QUIT"""
        return True

    do_q = do_exit = do_EXIT = do_Q = do_QUIT = do_quit
    do_T = do_test = do_TEST = do_t
    do_RUN = do_run


def main():
    cct = CZCETA()
    # cct.set_date(st='20180419', et='20180429')
    # print(cct.dlist)
    # cct.run()
    # cct.make_net_work()
    cct.cmdloop()


if __name__ == '__main__':
    main()
