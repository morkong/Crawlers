#！/user/bin/env python
#- *- coding:utf-8 -*-
import random
import time

import mysql.connector
import urllib.request
#########start根据url地址下载小文件############
def download_little_file(from_url,to_path):
    # 该请求对象的User-Agent进行了成功的伪装
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1;Win64;x64;rv:61.0) Gecko/20102001 Firefox/61.0",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

    request = urllib.request.Request(url=from_url, headers=headers)
    # 针对自定义请求对象发起请求
    response = urllib.request.urlopen(request)
    #conn = urllib.request.urlopen(from_url)
    #写入文件
    f = open(to_path,'wb')
    f.write(response.read())
    f.close()
#########end根据url地址下载小文件############
def getfile() :
    try:
        #连接数据库
        conn = mysql.connector.connect(
            host='localhost', user='root', database='stocks', port='3306', password='123456',
            use_unicode=True)
        # 获取游标
        cur = conn.cursor()
        #查询
        cur.execute("SELECT code from stock_code")
        #conn.commit()
        #将查询的code 结果遍历
        for row in cur:
            #拼装下载链接
            file_urls = "http://quotes.money.163.com/service/chddata.html?code=0" + row[
                0] + "&start=19900101&end=20191210&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
            print(file_urls)
            #调用，下载文件
            download_little_file(file_urls, r'D:\360Downloads\data2\ '+row[0]+".csv")
            print(row[0]+'.csv','下载完成！')
            time.sleep(random.choice(range(1, 5))) #随机延时一段时间，以免反爬虫

        print('--------关闭数据库资源----------')
        # 关闭游标
        cur.close()
        # 关闭连接
        conn.close()
    except Exception as  e:
        print(e)


if __name__ == '__main__':
    getfile()
