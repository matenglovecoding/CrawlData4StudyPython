#coding=utf-8
# crawl data from BaiDu TieBa
import urllib2
import re

class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

class BDTB:
    def __init__(self,baseUrl,see_lz):
        self.baseUrl = baseUrl
        self.see_lz = see_lz
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.headers={'User-Agent':self.user_agent}
        self.pageNum = 1
        self.TotalNums=0
        self.title = ''
        self.tool=Tool()
        self.file=None

    def getPageCode(self,see_lz,pageNum):
        url = self.baseUrl + '?' + 'see_lz=%s&pn=%s' % (see_lz,pageNum)
        try:
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u'连接百度贴吧失败，错误原因：' + e.reason
                return None
    def countPages(self):
        pageCode = self.getPageCode(self.see_lz,self.pageNum)
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        item = re.search(pattern,pageCode)
        totalNums=int(item.group(1).strip())
        self.TotalNums=totalNums
        return totalNums

    def getTitle(self):
        pageCode = self.getPageCode(self.see_lz,1)
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
        item = re.search(pattern,pageCode)
        title = item.group(1).strip()
        return title

    def  getReply(self,pageNum):
        url = self.baseUrl + '?' + 'see_LZ=%s' % see_lz
        if (pageNum <= self.TotalNums):
            pageCode = self.getPageCode(self.see_lz,pageNum)
            pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
            items = re.findall(pattern,pageCode)
            for item in items:
                self.file.write(self.tool.replace(item.strip()).encode('utf-8'))

baseUrl='https://tieba.baidu.com/p/3138733512'
see_lz = 1
bdtb=BDTB(baseUrl,see_lz)
#print bdtb.getTitle()
bdtb.title=bdtb.getTitle()
try:
    bdtb.file=open(bdtb.title+'.txt','w+')
    for i in range(1,bdtb.countPages()+1):
        print u'正在写入第%d页'%i
        bdtb.getReply(i)
    bdtb.file.close()
except IOError,e:
    if hasattr(e,'reason'):
        print e.reason