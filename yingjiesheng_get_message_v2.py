#coding=utf-8
#__author__ = 'xb'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("../../")
from common import webutil,xpathutil,mongoutil,pageutil,numberutil,timeutil,functions,RedisQueue_master1,proxyutils
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
logging = get_logger("./yingjiesheng.log");
class Get_Message():
    def __init__(self):
        self.href_list=[]
	self.key_word=[(u'企业名称',u'公司名称'),(u'所属行业',u'公司行业'),(u"企业规模",u'公司规模'),(u'企业性质',u'公司性质'),(u'企>业网址',u'招聘门户',u"公司网址",u"公司网站"),(u'公司简介',u'招聘简介'),(u'职位名称',u'招聘岗位'),
                     (u'工作地点',u'实习地点'),(u"实习部门",),(u"有效日期",),(u"招聘人数",),(u"招募对象",),(u"职位性质",),(u"职位类型",u"职位类别"),(u"专业标签",),(u"职位描述",),(u"学业要求",u"学历要求",u"专业要求"),(u"任职要求",u"岗位要求"),(u"岗位职责",),(u"岗位应聘条件",),(u"薪酬",u"福利"),
                     (u"联系方式",),(u"邮箱",),(u"简历投递",),(u"联系人",),(u"企业网址",),(u"联系地址",),(u"邮编",),(u"职位名称工作地点",),(u"上一职位",)
                       ]
    def Get_message(self,url,date):
        db_yjs=mongoutil.getmondbv2(db.mongo_host,db.mongo_port,db.yjs_db_name,db.yjs_table_name,username=db.mongo_user,password=db.mongo_pwd,timeout=30)
        now=timeutil.format("%Y-%m-%d",time.time())
        proxy=None
        count=10
        while True:
            try:
               
                #proxy=None
                myPage=webutil.request(url,timeout=10,proxy=proxy,encoding="gbk")
                break
            except Exception as e3:
                print e3
		proxy = proxyutils.choice_proxy(is_debug=False,host="master1",port=8880)
                if count<=0:
                    raise  Exception(u"连续10次失败,放弃")
                count-=1
                time.sleep(1) 
        tree=etree.HTML(myPage)
        
        jiben=xpathutil.get_all_text(tree,".//*[@id='container']/div[3]/div[2]/div/ul",num=0,split=u" ")#.//*[@id='container']/div[3]/div[2]/div/ul/li[2]
        text=xpathutil.get_all_text(tree,".//*[@id='wordDiv']/div/div",num=0,split=u" ")
        print len(text)
        if len(text)<=10:
            text=xpathutil.get_all_text(tree,".//*[@id='container']/div[3]",num=0,split=u" ")
        else:
            pass
	    p=functions.remove_all_space_char(text)
        p=functions.remove_all_space_char(p)
        emeail=re.compile('[\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+')
                    
        e=emeail.findall(p)
        a=[]
        phone_number=re.compile('^(?:\+86)?(\d{3})\d{8}$|^(?:\+86)?(0\d{2,3})\d{7,8}$')
        pn=phone_number.findall(p)
        posdict=dict()
                   
        for  key in self.key_word:
		found=False
                for j in key:
			index=p.find(j)
                        if index>=0:
				if found:
                                    print "error"
                                else:
                                    posdict[j]=index
                                    found=True
        for key in  posdict:
		a.append(posdict[key])
	a.sort()
	save_data=dict()
	for i in range(0,len(a)):
		if i+1<len(a):
			text3=''
                        text3=p[int(a[i]):int(a[i+1])].replace('：',':',1).replace("：",":",1).replace("：",":",1)
                        text3=text3.split(':')

                        if len(text3)>1:
				if len(text3)==2:
                                        save_data[text3[0]]=text3[1]

                                else:
                                        save_data[text3[0]]=text3[1]+text3[2]
                        elif len(text3)==1:
                               	save_data[text3[0]]='None'
                        else:
				pass
		
		else:
			pass

        if e:
            save_data["邮箱"]=e[0]
        else:
            save_data["邮箱"]="无"
        if pn:
               	save_data['电话']=pn[0]
        else:
                save_data["电话"]="无"
    
	
        myPage=myPage.encode('utf-8')
        title=re.findall('<title>(.*?)</title>',myPage)
        if not title:
            title=xpathutil.get_all_text(tree,".//*[@id='container']/div[3]/div[1]/h1/a",num=0,split=u" ")
            name= title
        else:
            name=title[0]
        print name

        p=''
        if not jiben:
            pp=re.findall('<div class="info clearfix"><ol><li>\xe5\x8f\x91\xe5\xb8\x83\xe6\x97\xb6\xe9\x97\xb4：<u>(.*?)</u></li><li>\xe5\xb7\xa5\xe4\xbd\x9c\xe5\x9c\xb0\xe7\x82\xb9：<u>(.*?) </u></li><li>\xe8\x81\x8c\xe4\xbd\x8d\xe7\xb1\xbb\xe5\x9e\x8b：<u>(.*?)</u></li><li>\xe6\x9d\xa5\xe6\xba\x90：<a href="#" onclick="window.open(.*?)">(.*?)</a></li>',myPage)
            for i in pp:
                for j in i:
                    if j.find('(')==-1:
                        p=p+j+'\r\n'
        else:
            jiben=jiben.replace('\t','')
            jiben=jiben.split('\r\n')
            for i in jiben:
                p=p+i.split('：')[-1].replace('\n','')+'\r\n' 
        print p 
        myPage=myPage.decode('utf-8')
        keys=url+now
	save_data["公司名称"]=name
	save_data["发布时间"]=date
	save_data["文本1"]=p
	save_data['文本2']=text
	save_data["页面链接"]=url
	save_data["页面源码"]=myPage
	save_data['dotime']=now
	save_data['uptime']=time.time()
	save_data['source']="yingjiesheng"
	save_data["type"]="1"
        mongoutil.updatev3(db_yjs,keys,save_data)
	print("数据入库成功！")

def run():
    ss=Get_Message()
    
    
    try:
        RedisQueue=RedisQueue_master1.getredisQueuev2('yingjiesheng_href1')
	    
	while(not RedisQueue.empty()):
            href=RedisQueue.getv2()
	    if href:
            	href=href.split('BBD')
            	url=href[0]
		print url
            	date=href[1]
            	ss.Get_message(url,date)
            else:
            	pass
                #raw_input('sssssssssss')    
    except Exception as e2:
            print e2
            logging.error("url:%s" % url+time.ctime()) 
            pass
if __name__=="__main__":
    count=100
    while True:
	try:
	    run()
	except Exception as e3:
                print e3
                if count<=0:
                    raise  Exception(u"连续100次失败,放弃")
                count-=1
                time.sleep(1)

    

    
                
        
