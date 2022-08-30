#!/home/flask/bin/python3.8
# -*- coding: utf-8 -*-
from pandas import DataFrame
from selenium import webdriver
from selenium.common.exceptions import *
from pathlib import Path
import time,pyodbc
from datetime import datetime
from random import randint
import myloggerclass
import os,pydoc
logger = myloggerclass.MyLoggerClass('stock_data', 'logdata{}.log'.format(datetime.now().strftime('%Y%m%d')),'info')

def getNextPage(webdriver):
    next = None
    try:
        next = webdriver.find_element_by_link_text('下一页')
    except NoSuchElementException:
        logger.writeWarnLog('no more page')
    return next

def getWebPageData(html):
    from requests_html import HTML
    today = datetime.now().strftime('%Y-%m-%d')
    resp = HTML(html=html)
    tr = resp.find("tr")
    ret = []
    for _ in tr:
        if _.attrs:
            temp = []
            for td in _.find("td"):
                temp.append(td.text)
            for i in range(3,16):
                if temp[i].find('亿') > 0:
                    temp[i] = temp[i].replace('亿','')
                    temp[i] = round(float(temp[i]) * 100000000, 0)
                elif temp[i].find('万') > 0:
                    temp[i] = temp[i].replace('万','')
                    temp[i] = round(float(temp[i]) * 10000, 0)
                elif temp[i].find('%') > 0:
                    temp[i] = temp[i].replace('%','')
            if temp[4] == '-':
                continue
            temp[3]=today
            ret.append(temp)
    return ret

def main():
    alldata = []
    conn = None
    conn = connectDB()
    if not conn:
        print('no db conn')
        os.sys.exit() 
    trunTable(conn)
    col = ['rank'
          ,'code'
          ,'name'
          ,'other'
          ,'zuixinjia'
          ,'zhangdiefu'
          ,'zhuli_jinge'
          ,'zhuli_zhanbi'
          ,'chaodadan_jinge'
          ,'chaodadan_zhanbi'
          ,'dadan_jinge'
          ,'dadan_zhanbi'
          ,'zhongdan_jinge'
          ,'zhongdan_zhanbi'
          ,'xiaodan_jinge'
          ,'xiaodan_zhanbi'
          ,'date'
          ]
    edgepath = Path("C:\py\edgedriver\msedgedriver.exe")
    web = webdriver.Edge(executable_path=edgepath)
    url = "https://data.eastmoney.com/zjlx/detail.html"
    web.get(url)
    time.sleep(3)
    next = web.find_element_by_xpath('//*[@id="filter_mkt"]/li[2]')
    i = 1
    while next:
        logger.writeInfoLog('go to page {}'.format(i))
        next.click()
        time.sleep(randint(1, 5))
        html = web.page_source
        onepage = getWebPageData(html)
        for _ in onepage:
            #alldata.append(_)
            insertDB(conn, _)
        logger.writeInfoLog('completed, page {}'.format(i))
        i = i + 1
        next = getNextPage(web)

    #data = DataFrame(data=alldata,columns=col)
    #data.pop('other')
    #data.to_csv('data{}.csv'.format(datetime.now().strftime('%Y%m%d')),index=False)
    processData(conn)
    closeDB(conn)
    #web.quit()


def getR001():
    logger.writeInfoLog('go to R001')
    edgepath = Path("C:\py\edgedriver\msedgedriver.exe")
    web = webdriver.Edge(executable_path=edgepath)
    url = "http://quote.eastmoney.com/bond/sz131810.html"
    web.get(url)
    time.sleep(3)
    interest = web.find_element_by_xpath('//*[@id="app"]/div/div/div[7]/div[1]/div[1]/span[1]/span').text
    today = datetime.now().strftime('%Y-%m-%d')
    df = DataFrame(data=[[today,interest]],columns=['Date','Interest'])
    df.to_csv('R001.csv',index=False,mode='a',header=False)
    logger.writeInfoLog('completed, R001')
    web.quit()

def connectDB():
    try:
        conn = pyodbc.connect(DRIVER='{SQL Server Native Client 11.0}',SERVER='localhost\sqlexpress',DATABASE='stock',Trusted_Connection='Yes')
        logger.writeInfoLog('db connected')
    except pyodbc.Error as e:
        print(e)
    return conn

def closeDB(conn):
    if conn:
        conn.close()
        logger.writeInfoLog('db closed')

def insertDB(conn: pyodbc.Connection,data: list):
    #print(data)
    sql = "insert into daily_zjl_details values \
        ({},'{}','{}',{},{},{},{},{},{},{},{},{},{},{},{},'{}')".format(data[0],data[1],data[2],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[3])
    conn.execute(sql)
    conn.commit()
    
def trunTable(conn):
    logger.writeInfoLog('delete today data')
    sql = "delete from daily_zjl_details where date日期='{}'".format(datetime.now().strftime('%Y-%m-%d'))
    conn.execute(sql)
    conn.commit()

def processData(conn):
    logger.writeInfoLog('start to run sp')
    sql = ['exec update_zjl_details_powerbi','exec update_all_stocks']
    for cmd in sql:
        logger.writeInfoLog(cmd)
        conn.execute(cmd)
        conn.commit()

if __name__ == '__main__':
    logger.startLogger()
    main()
    #getR001()
    logger.stopLogger()