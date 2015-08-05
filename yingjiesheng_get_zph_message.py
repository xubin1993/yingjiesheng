#coding=utf-8
#__author__ = 'xb'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("../../")
from common import webutil,xpathutil,mongoutil,pageutil,numberutil,timeutil,functions
import string
import re
import time
from datetime import date,timedelta
from Queue import Queue
from lxml import etree
from common.logutil import get_logger
import chardet
import codecs
import db
#from yingjiesheng_get_href import Get_Href
logging = get_logger("./yingjiesheng_zph.log");
class Get_Message():
    def __init__(self):
        self.href_list=[]
    def Get_message(self,url):
        db_yjs=mongoutil.getmondbv2(db.mongo_host,db.mongo_port,db.yjs_db_name,db.yjs_table_name,username=db.mongo_user,password=db.mongo_pwd)
        now=timeutil.format("%Y-%m-%d",time.time())
        proxy=None
        count=10
        while True:
            try:
                #proxy = proxyutils.choice_proxy(is_debug=False,host="master1",port=8880)
                #proxy=None
                myPage=webutil.request(url,timeout=10,proxy=proxy,encoding="gbk")
                break
            except Exception as e3:
                print e3
                if count<=0:
                    raise  Exception(u"连续10次失败,放弃")
                count-=1
                time.sleep(1) 
        tree=etree.HTML(myPage)
        title=xpathutil.get_all_text(tree,".//*[@id='mainNav']/div[2]/table/caption/h1",num=0,split=u" ")
        #address=xpathutil.get_all_text(tree,".//*[@id='mainNav']/div[2]/table/tbody/tr[3]/td",num=0,split=u" ")
        #pp=re.findall('<td>汉阳郭茨口香格里都3楼腾飞人才市场</td>')
        print title
        myPage=myPage.encode('utf-8')
        address1=re.findall('<th width="90">(.*?)</th>(.*?)<td>(.*?)</td>',myPage,re.S)
        j=0
        for i in address1:
            if j==0:
                city1=re.findall('">(.*?)</a>',i[-1])
                city=city1[0]
            elif j==1:
                date=i[-1]
            elif j==2:
                address=i[-1]
            j=j+1
        
        print len(address)
        print city
        print date
        print address
        key=url+now
        mongoutil.updatev3(db_yjs,key,{"标题":title,"城市":city,"招聘会时间":date,'招聘会地点':address,"页面链接":url,"dotime":now,"uptime":time.time(),"source":"yingjiesheng","type":"2"})
        
if __name__=="__main__":
    ss=Get_Message()
    while(True):
        f2=open('href_zph.txt','r')
        f4=open('href_zph_dd.txt','a+')
        for i in f2.readlines():    
            url=i
            if url.find('http:')!=-1:
                print url
                try:
                    if url not in f4.read():
                        f4.write(url)
                        f4.write('\r\n')
                        ss.Get_message(url)
                    else:
                        pass
                except Exception as e2:
                    print e2
                    logging.error("url:%s" % url+time.ctime()) 
                    pass
            else:
                pass
        f2.close()
        f4.close()
        time.sleep(60)
