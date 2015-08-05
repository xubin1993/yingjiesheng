#coding=utf-8
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
import urllib2
logging = get_logger("./yingjiesheng_xjh.log");
class Get_Href():
    def __init__(self):
        self.href=[]
    def Get_href(self,url):
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
        try:
            city=re.findall('<td width="40"><a href="(.*?)" >(.*?)</a></td>',myPage)
            date=re.findall('<td width="115">(.*?)</td>',myPage)
            gongsi=re.findall('<a class="f14" href="(.*?)" >(.*?)</a>',myPage)
            xuexiao=re.findall('<a class="f14"  href="(.*?)">(.*?)</a></td>',myPage)
            address=re.findall('<td class="left f14">(.*?)</td>',myPage)
            time_href=re.findall('<td width="100" class="en left"><img src="(.*?)"></td>',myPage)
            xq_href=re.findall('<td  width="75" class="left"><a href="(.*?)" target="_blank">',myPage)
            time_image_list=[]
            gongsi_name_list=[]
            for i in city:
                print i[-1] 
            for i in date:
                print i 
            for i in gongsi :
                gongsi1=re.findall(u'[\u4e00-\u9fa5]+',i[-1])
                if gongsi1:
                    print gongsi1[0]
                    gongsi_name_list.append(gongsi1[0])
                else:
                    gongsi_name=i[-1]
                    gongsi_name_list.append(gongsi_name)
            for i in xuexiao:
                print i[-1]
            for i in address:
                print i 
            for i in xq_href:
                print i 
            for i in time_href:
		url=''
                url='http://my.yingjiesheng.com'+i
                
                time_image_list.append(url)
            if len(time_image_list)==len(xq_href)==len(address)==len(xuexiao)==len(gongsi_name_list)==len(date)==len(city):
                for i in range(0,len(xq_href)):
                    key=gongsi_name_list[i]+date[i]
                    mongoutil.updatev3(db_yjs,key,{"企业名称":gongsi_name_list[i],"举办时间":date[i],"具体时间":time_image_list[i],"详情链接":xq_href[i],'学校':xuexiao[i][-1],"具体地点":address[i],"城市":city[i][-1],"dotime":now,"uptime":time.time(),"source":"yingjiesheng","type":"3"})      
            else:
                pass
            
           
                    
                    

        except Exception as e2:
            logging.error("product id:%s" %e2)
            print e2
            pass

        
            

        
if __name__=="__main__":
    ss=Get_Href()
    #url='http://www.yingjiesheng.com/commend-fulltime-1.html'
    j=1
    while(j<60):
        try:
            print j
            url='http://my.yingjiesheng.com/index.php/personal/xjhinfo.htm/?page=%s&cid=&city=0&word=&province=0&schoolid=&sdate=&hyid=0'%(j)
            ss.Get_href(url)
            j=j+1
           
            
        except Exception as e2:
            print e2
            j=j+1
            logging.error("url:%s" % url+str(j))

            pass
