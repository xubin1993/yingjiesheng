#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("../../")
from common import webutil,xpathutil,mongoutil,pageutil,numberutil,timeutil,RedisQueue_master1,proxyutils
import string
import re
import time
from datetime import date,timedelta
from Queue import Queue
from lxml import etree
from common.logutil import get_logger
import chardet
import codecs
logging = get_logger("./yingjiesheng.log");
class Get_Href():
    def __init__(self):
        self.href=[]
    def Get_href(self,url):
        RedisQueue=RedisQueue_master1.getredisQueuev2('yingjiesheng_href1')
        f1=open('href.txt','ar+')
        proxy=None
        count=10
        while True:
            try:
                
                #proxy=None
                myPage=webutil.request(url,timeout=10,proxy=proxy).decode('gbk').encode('utf-8')
                break
            except Exception as e3:
                print e3
		proxy = proxyutils.choice_proxy(is_debug=False,host="master1",port=8880)

                if count<=0:
                    raise  Exception(u"连续10次失败,放弃")
                count-=1
                time.sleep(1) 
        try:
            pp=re.findall('<a href="(.*?)" target="_blank"><span style="color:(.*?);">(.*?)</a>(.*?)</td>(.*?)<td class="date">(.*?)</td>',myPage,re.S)
            for i in pp:
                m=i[0]
                p=m.split('href="')[-1]
                if p.find('http://')==-1:
                    href='http://www.yingjiesheng.com'+p
                else:
                    href=p
                if href not in f1.read(): 
                    print href,i[-1]

                    hh=href+'BBD'+i[-1]
                    RedisQueue.put(hh)
                    f1.write(href)
                    f1.write('\r\n')
                    f1.write(i[-1])
                    f1.write('\r\n')
            
            print len(pp)
            f1.close()
        except Exception as e2:
            logging.error("product id:%s" %e2)
            print e2
            pass
            

        
if __name__=="__main__":
    ss=Get_Href()
    #url='http://www.yingjiesheng.com/commend-fulltime-1.html'
    j=1
    while(j<3000):
        try:
            print j
            url='http://www.yingjiesheng.com/commend-fulltime-%s.html'%j
            ss.Get_href(url)
            j=j+1
            
        except Exception as e2:
            print e2
            logging.error("url:%s" % url+str(j))
            j=j+1
            pass
   
           
