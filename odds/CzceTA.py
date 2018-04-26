# -*- coding:utf-8 -*-
import requests
from requests.exceptions import ConnectTimeout
from datetime import datetime, date, timedelta
from cmd import Cmd
Header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
czceUrl = 'http://www.czce.com.cn'
contractUrl = 'http://www.czce.com.cn/portal/DFSStaticFiles/Future/{yyyy}/{tdate}/FutureDataTrdhedge.txt'


class CZCETA(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = ">"
        self.session = requests.Session()
        self.dlist = []

    def make_net_work(self):
        try:
            self.session.get(url=czceUrl, timeout=3)
        except ConnectTimeout as _:
            print('Connect to Czce Failed @ on __init__\n', _)
        else:
            print('Connect to Czce Success @ on __init__')

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
        # self.make_net_work()
        if not self.dlist:
            print('Must set date range')
            return
        else:
            print('Datelist=[', ','.join(self.dlist), ']')
        fw = open('FutureTrdhedge.csv', 'a')
        for tdate in self.dlist:
            print(tdate)
#             r = self.session.get(url=contractUrl.format(yyyy=tdate[:4], tdate=tdate))
#             src = r.text.encode('latin1').decode('gbk')
#             if src[:6] != '<html>':
#                 print(src)
#                 lines = src.split('\n')
#                 for line in lines[2:]:
#                     nline = line[:-1].replace(' ', '').replace(',', '')
#                     nlist = nline.split('|')
#                     if len(nlist) > 1:
#                         nlist.insert(0,tdate)
#                         fw.write(','.join(nlist)+'\n')
#             else:
#                 print('Error Page')
        fw.close()

    def do_quit(self, argv):
        return True

    do_q = do_quit


def main():
    cct = CZCETA()
    # cct.set_date(st='20180419', et='20180429')
    # print(cct.dlist)
    # cct.run()
    # cct.make_net_work()
    cct.cmdloop()


if __name__ == '__main__':
    main()
