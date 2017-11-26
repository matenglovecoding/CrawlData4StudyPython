#coding=utf-8
import urllib2
import re

class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        self.headers={'User-Agent':self.user_agent}
        self.stories=[]
        self.enable = False

    def getPage(self,pageIndex):
        url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
        request = urllib2.Request(url,headers=self.headers)
        response = urllib2.urlopen(request)
        pageCode = response.read().decode('utf-8')
        #print pageCode
        return pageCode

    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        pattern = re.compile('h2>(.*?)</h2.*?content">(.*?)</.*?number">(.*?)</',re.S)
        items = re.findall(pattern,pageCode)
        pageStories=[]
        for item in items:
            pageStories.append([item[0].strip(),item[1].strip()[6:].strip(),item[2].strip()])
        return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                self.pageIndex+=1
                self.stories.append(pageStories)
    def tellStory(self,pageIndex,pageStories):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input=="Q":
                self.enable=False
                return
            print u"第%d页\t发布人:%s\t赞:%s\n内容:%s" %(pageIndex,story[0],story[2],story[1])

    def start(self):
        print u"正在查看糗事百科，查看请按回车，推出请按Q"
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories=self.stories[0]
                nowPage+=1
                del self.stories[0]
                self.tellStory(nowPage,pageStories)
spider=QSBK()
spider.start()
