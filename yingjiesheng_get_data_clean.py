#coding=utf-8
__author__ = 'xb'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("../../")
from common import webutil,xpathutil,mongoutil,pageutil,numberutil,timeutil,functions,RedisQueue_master1
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
logging = get_logger("./data_clean.log");
class Clean_data():
    def __init__(self):
        self.key_word=[(u'企业名称',u'公司名称'),(u'所属行业',u'公司行业'),(u"企业规模",u'公司规模'),(u'企业性质',u'公司性质'),(u'企业网址',u'招聘门户',u"公司网址",u"公司网站"),(u'公司简介',u'招聘简介'),(u'职位名称',u'招聘岗位'),
                     (u'工作地点',u'实习地点'),(u"实习部门",),(u"有效日期",),(u"招聘人数",),(u"招募对象",),(u"职位性质",),(u"职位类型",u"职位类别"),(u"专业标签",),(u"职位描述",),(u"学业要求",u"学历要求",u"专业要求"),(u"任职要求",u"岗位要求"),(u"岗位职责",),(u"岗位应聘条件",),(u"薪酬",u"福利"),
                     (u"联系方式",),(u"邮箱",),(u"简历投递",),(u"联系人",),(u"企业网址",),(u"联系地址",),(u"邮编",),(u"职位名称工作地点",),(u"上一职位",)
                       ]
        
            
    def Clean(self,key):
        try:
            db_yjs=mongoutil.getmondbv2(db.mongo_host,db.mongo_port,db.yjs_db_name,db.yjs_table_name,username=db.mongo_user,password=db.mongo_pwd,timeout=30)
            hh=db_yjs.find({'type':'1'})
            number=0
            for i in hh:
                if i:
                    p=i.get(u"文本2")
		    
		   
                    id=i.get("_id")
                    p=functions.remove_all_space_char(p)
                    emeail=re.compile('[\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+')
                    #p=p.decode('utf-8','ignore') '
                    #print p 
                    e=emeail.findall(p)
                    a=[]
		    phone_number=re.compile(r'^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$')
		    pn=phone_number.findall(p)
                    posdict=dict()
                    #print p[53:102]
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
                        save_data["邮箱"]="None"
		    if pn:
			save_data['电话']=pn[0]
		    else:
			save_data["电话"]="None"
		    save_data['文本3']='None'
                    for i in save_data:
			print i,save_data[i]
                    number=number+1
                    mongoutil.updatev3(db_yjs,id,save_data)
		    print "更新成功！%s"%number
		    
		   
                else:
                    pass
	    logging.error("完毕！")
	    logging.error("%s"%number)
               
        except Exception as e2:
            print e2
	    logging.error("错误:%s" %e2)
	    logging.error("数量%s" %number)
            self.Clean(key)
            
                #quit()
                
                        
                    
                
  
ss=Clean_data()
ss.Clean(50665)
        
    
