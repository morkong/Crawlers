#！/user/bin/env python
#- *- coding:utf-8 -*-
import random
import time
import mysql.connector
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#基金代码
Code =[]
#基金名称
Name =[]
#估算值
Estimated_value =[]
#估算增长率
Estimated_growth_rate =[]
#今日单位净值
Today_net_unit_value =[]
#今日日增长率
Today_daily_growth_rate=[]
#估算偏差
Estimation_bias = []
#昨日单位净值
Yesterday_net_unit_value =[]
#是否可购
Is_buy =[]

#chrome浏览器无头模式
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
#driver = webdriver.Chrome()


url = 'http://fund.eastmoney.com/fundguzhi.html'
#打开网页
driver.get(url)
#通过requests打开网页获取状态码，判断网页是否成功打开
r = requests.get(url)
if r.status_code != 200:
    print('连接错误')
    #退出程序
    exit()
#延时5秒，等待浏览器加载页面
time.sleep(5)
for i in range(2):
    print('已到达第%s页'%str(i+1))
    #xpath 定位标签，获取数据
    try:
        code = driver.find_elements_by_xpath('//tbody[@id="tableContent"]/tr/td[3]')
        name = driver.find_elements_by_xpath('//tbody[@id="tableContent"]/tr/td[4]/a[1]')
        estimated_value = driver.find_elements_by_xpath('//tbody[@id="tableContent"]/tr/td[5]')
        estimated_growth_rate =driver.find_elements_by_xpath('//tbody[@id="tableContent"]/tr/td[6]')
        today_net_unit_value= driver.find_elements_by_xpath('//tbody[@id="tableContent"]/tr/td[7]')
        today_daily_growth_rate= driver.find_elements_by_xpath('//tbody[@id="tableContent"]/tr/td[8]')
        estimation_bias= driver.find_elements_by_xpath('//tbody[@id="tableContent"]/tr/td[9]')
        yesterday_net_unit_value= driver.find_elements_by_xpath('//tbody[@id="tableContent"]/tr/td[10]')
        is_buy = driver.find_elements_by_xpath('//tbody[@id="tableContent"]/tr/td[11]/a')
        print('已获取%s页数据,等待中'% str(i + 1))

        for j in range(len(code)):
            # 判断购买按钮是否是灰色，灰色表示不可购买

            # isbuy = '.'.join(is_buy[j].get_attribute('class'))
            # if isbuy.find('gray'):
            #     isbuy = '0'
            # else:
            #     isbuy = '1'
            #
            # print(code[j].text, name[j].text, estimated_value[j].text, estimated_growth_rate[j].text,
            #           today_net_unit_value[j].text,
            #           today_daily_growth_rate[j].text, estimation_bias[j].text, yesterday_net_unit_value[j].text, isbuy)

            # 基金代码
            Code.append(code[j].text)
            # 基金名称
            Name.append(name[j].text)
            # 估算值
            Estimated_value.append(estimated_value[j].text)
            # 估算增长率
            Estimated_growth_rate.append(estimated_growth_rate[j].text)
            # 今日单位净值
            Today_net_unit_value.append(today_net_unit_value[j].text)
            # 今日日增长率
            Today_daily_growth_rate.append(today_daily_growth_rate[j].text)
            # 估算偏差
            Estimation_bias.append(estimation_bias[j].text)
            # 昨日单位净值
            Yesterday_net_unit_value.append(yesterday_net_unit_value[j].text)

            #判断是否可购买
            isbuy = ''.join(is_buy[j].get_attribute('class'))
            #没有找到则返回-1
            if isbuy.find('gray') == -1:
                isbuy = '1'
            else:
                isbuy = '0'

            # 是否可购
            Is_buy.append(isbuy)
        time.sleep(random.choice(range(1, 5)))  # 随机延时一段时间，以免反爬虫
        # 点击翻页
        driver.find_element_by_xpath('//a[@class="next ttjj-iconfont"]').click()
    except Exception as  e:
        print(e)
#关闭浏览器
driver.quit()
print('数据采集完成，关闭浏览器')
print('开启数据库，正在保存数据')
try:
    conn = mysql.connector.connect(
                host='localhost', user='root', database='stocks', port='3306', password='123456',
                use_unicode=True)
    # 获取游标
    cur = conn.cursor()
    for j in range(len(Code)):
        values = [Code[j],Name[j],Estimated_value[j],Estimated_growth_rate[j],Today_net_unit_value[j],
                  Today_daily_growth_rate[j],Estimation_bias[j],Yesterday_net_unit_value[j],Is_buy[j]]

        # values = [code[j].text, name[j].text, estimated_value[j].text, estimated_growth_rate[j].text,
        #           today_net_unit_value[j].text,
        #           today_daily_growth_rate[j].text, estimation_bias[j].text, yesterday_net_unit_value[j].text, isbuy]
        cur.execute("insert into estimation_of_net_worth_table values (%s,%s,%s,%s,%s,%s,%s,%s,%s)", values)
        conn.commit()
        if (j+1)%100 == 0:
            print('正在保存第%s条数据'% str(j+1))
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()
    print('数据保存完成，关闭数据库')
except Exception as  e:
    print(e)