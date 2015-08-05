#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("../../")
from common import webutil,xpathutil,mongoutil,pageutil,numberutil,timeutil
import string
import re
import time
import os
from datetime import date,timedelta
from Queue import Queue
from lxml import etree
from common.logutil import get_logger
import chardet
import codecs
import db
logging = get_logger("./yingjiesheng_zph.log");
class Get_Href():
    def __init__(self):
        self.href=[]
    def Get_href(self,url):

        f1=open('href_zph.txt','a+')
        #
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
        try:
            href_list=re.findall('] <a href="(.*?)" target="_blank"',myPage,re.S)
            address_list=re.findall('<td width="220" class="left">(.*?)</td>',myPage)
            city_list=re.findall('class="city">(.*?)</a>]',myPage)
            date_list=[]
            name_list=[]
            for i in href_list:
                if i.find('http://')==-1:
                    href='http://zph.yingjiesheng.com'+i
                    
                else:
                    href=i
                if href not in f1.read():
                    print href
                    f1.write(href)
                    f1.write('\r\n')
                else:
                    pass
            f1.close()
           
                    
                    

        except Exception as e2:
            logging.error("product id:%s" %e2)
            print e2
            pass
        #key=url+now
       # mongoutil.updatev3(db_yjs,key,{"公司名称":name,"发布时间":date,"文本1":p,"文本2":text,'页面链接':url,"页面源码":myPage,"dotime":now,"uptime":time.time(),"source":"yingjiesheng","type":"2"})
        
            

        
if __name__=="__main__":
    ss=Get_Href()
    #url='http://www.yingjiesheng.com/commend-fulltime-1.html'
    j=0
    file='href_zph.txt'
    if os.path.exists(file):
        os.remove(file)
    else:
		pass
    while(j<11):
        try:
            print j
            url='http://zph.yingjiesheng.com/zphlist.php?start=%s'%(j*40)
            ss.Get_href(url)
            j=j+1
            #raw_input('wwwwww')
            
        except Exception as e2:
            print e2
            logging.error("url:%s" % url+str(j))
            j=j+1
            pass
    j=0
    while(j<2000):
        try:
            print j
            url='http://zph.yingjiesheng.com/old.php?start=%s'%(j*40)
            ss.Get_href(url)
            j=j+1
            
        except Exception as e2:
            print e2
            logging.error("url:%s" % url+str(j))
            j=j+1
            pass        
