# -*- coding:utf-8 -*-
import os 
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
os.environ['ORACLE_HOME'] = 'D:/instantclient_11_2_my'
os.environ['PATH'] = 'D:\\instantclient_11_2_my;'+os.environ['PATH']
print(os.environ['PATH'])
import cx_Oracle
import pandas as pd
 #IFMSREOPR/QalY2hua
LCtest = 'pub_query/pub_query@10.14.215.92:1555/s2ifmsdb'
LCnew = 'IFMSREOPR/QalY2hua@10.0.76.95:1521/wbifmsdb'
LCold = 'ORAXPAB/IfmsReLc12@10.0.79.30:1521/adgncpxrac'
fund = ' *****/*****@10.0.79.25:1521/adgifm30'
test='paorg/Paorg123@10.14.200.70:1555/logcng'
conn = cx_Oracle.connect(LCnew)
print(conn)
curs=conn.cursor()
sql='select t.table_name from user_tables t order by t.table_name' # FROM 1'
rr=curs.execute(sql)
rs=curs.fetchall()
for row in rs:
    print(row)

tbs = ['ifms_re_cfg_prod_info']#,'ifms_re_cfg_prod_info','lc12_product']
for tb in tbs:
    # curs.execute('select * from %s'%tb)
    # rs = curs.fetchall()
    # for row in rs:
        # print(row)
    df = pd.read_sql(sql='select * from %s'%tb,con=conn)
    df.to_csv(path_or_buf='%s.csv'%tb,sep='\t',encoding = "gbk")
    # names = [x for x in df['PRODUCTNAME'].get_values()]
    # print(names[:20])
    #print(df.tail())
curs.close()
conn.close()