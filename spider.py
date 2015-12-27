#/usr/bin/env python
#coding:utf-8

import re
import urllib
import urllib2

class Qsbk():
    
    def __init__(self):
        self.page = 1
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
        self.headers = {"User-Agent": self.user_agent}
        self.stories = []
        self.num = 1
        self.next = True

    def getPageHtml(self):
        url = "http://www.qiushibaike.com/8hr/page/" + str(self.page)
        try:
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request, timeout = 3)
            content = response.read()
            return content
        except urllib2.URLError as e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    def getPageStories(self, content):
        pattern = re.compile('<div.*?class="author.*?>.*?<a.*?title="(.*?)".*?<div.*?class="content">.*?\n(.*?)<!--.*?<i.*?class="number">(.*?)</i>',re.S)
        page_stories = re.findall(pattern, content)
        if page_stories:
            self.stories.append(page_stories)

    def getNextStory(self):
        while self.next:

            input = raw_input()
            if input == "Q":
                self.next = False
                print "=====糗事百科爬虫程序停止====="
                break
            print "这是你浏览的第%d个糗事(输入‘Q’按Enter结束糗事之旅)" %(self.num)
            self.num += 1
            if not len(self.stories[0]):
                del self.stories[0]
                print "加载新一页糗事..."
                self.page += 1
                self.getPageStories(self.getPageHtml())
            print "还剩%d个糗事"%len(self.stories[0])
            print "-----------------------------------------"
            print "【糗主】",self.stories[0][0][0],"【赞】",self.stories[0][0][2]
            print "【糗事】",self.stories[0][0][1].strip()
            print "-----------------------------------------"
            del self.stories[0][0]


    def start(self):
        print "=====现在开始按Enter键开启糗事之旅吧====="
        self.getPageStories(self.getPageHtml())
        self.getNextStory()


spider = Qsbk()
spider.start()
