# -*- coding:utf-8 -*-
import urllib
import urllib2
from pyquery import PyQuery as pq

#获取到糗事百科热门的页面
def getpage(page):
    url = 'http://www.qiushibaike.com/8hr/page/' + str(page)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    try:
        request = urllib2.Request(url,headers = headers)
        response = urllib2.urlopen(request)
        the_page = response.read().decode('utf-8')
        qsbk_hot = pq(the_page)
        return qsbk_hot
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason


# 获取糗事百科除图片外的热门段子，作者，以及评论数
def getinfo(qsbk_hot_page):
    cont_text = []
    auth_text = []
    comment_text = []
    inpage = qsbk_hot_page("div.article.block.untagged")
    for i in inpage.items():
        if not (i.hasClass("thumb")):
            if i.find(".author.clearfix").find('a').text():
                auth_text.append(i.find(".author.clearfix").find('a').text())
            else:
                auth_text.append(i.find(".author.clearfix").find('span').text())
        cont_text.append(i.find(".content").text())
        temp = i.find(".stats").text().split()
        comment_text.append(temp[0])
    return cont_text, auth_text, comment_text


def run_main():
    page_now = 1
    run_enable = True
    print "正在读取糗事百科热门页面，按回车查看热门段子，按Q退出"
    count = 0
    while run_enable:
        qsbk_hot = getpage(page_now)
        contlist, authorlist, commentlist = getinfo(qsbk_hot)
        inpu = raw_input()
        if inpu == 'q' or inpu == 'Q':
            run_enable = False
        else:
            if count < len(contlist):
                print "********============================================================================********"
                print "作者：" + authorlist[count].encode('utf8')
                print "内容：" + contlist[count].encode('utf8')
                print "评论：有" + commentlist[count].encode('utf8') + "人觉得好笑"
                print "********============================================================================********"
                print ""
                count += 1
                continue
            else:
                page_now += 1
                count = 0
                print "正在切换至下一页，按回车继续查看段子，按Q退出"
                print ""
                continue

if __name__=="__main__":
    run_main()
