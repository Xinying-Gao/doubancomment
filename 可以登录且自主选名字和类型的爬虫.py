# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 15:48:30 2020

@author: 高心莹 2018201953
"""

import time
import random
from selenium import webdriver

class doubancomment_spider():
    def __init__(self,ip,comment_type,txtfile):
        # 创建chrome参数对象
        opt = webdriver.ChromeOptions()
        # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
        opt.set_headless()
        # 用的是谷歌浏览器
        driver = webdriver.Chrome(options=opt)
        driver=webdriver.Chrome()
        self.ip=ip
        self.comment_type=comment_type
        self.txtfile=txtfile
        self.get_comment(driver,ip,comment_type,txtfile)
    def get_comment(self,driver,ip,comment_type,txtfile):
    # 切换到登录框架中来.
    # 登录豆瓣网
        driver = driver
        driver.get("http://www.douban.com/")
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
        # 点击"密码登录"
        bottom1 = driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
        bottom1.click()
        # # 输入密码账号
        input1 = driver.find_element_by_xpath('//*[@id="username"]')
        input1.clear()
        input1.send_keys("13346775941")

        input2 = driver.find_element_by_xpath('//*[@id="password"]')
        input2.clear()
        input2.send_keys("yl1xhdxs")

        # 登录
        bottom = driver.find_element_by_class_name('account-form-field-submit ')
        bottom.click()
        time.sleep(1)
        i = 0
        txtlist = []
        while i<25:#即使登录了，豆瓣也只能看到前500条评论
             num = i*20
             #打开网址
             url = "https://movie.douban.com/subject/"+str(ip)+"/comments?start=" + str(num) +"&amp;limit=20&amp;sort=new_score&amp;status=P"+str(comment_type)
             print(url)
             time.sleep(1 + float(random.randint(1, 20)) / 20)#以不均匀的时间翻动页面，防止被识别出
             driver.get(url)  
             #定位评论
             elem = driver.find_elements_by_xpath("//span[@class='short']")
             #循环写入20行评价
             k = 0
             while k<20:#只能爬取满20条的页面，爬到不满20条的页就会报错，不过在这一页之前的完整页面的数据都可以爬。
                  shortcon = elem[k].text
                  print(shortcon)
                  txtlist.append(shortcon)
                  k = k + 1
             i = i + 1
             with open(txtfile,"w",encoding='utf-8') as f:
                 for x in txtlist:
                      f.write(x)
                 f.close
ip=input("请输入想要爬取的影视节目的ip（在豆瓣电影中点开想要爬取的影视节目的页面，页面链接中'subject/'后面的一串数字即为影片ip)：")
commenttype=int(input("您想要爬取的影片类型为：（全部类型请输入0，好评请输入1，中评请输入2，差评请输入3）："))
if commenttype==0:
    comment_type=''
if commenttype==1:
    comment_type='&percent_type=h'
if commenttype==2:
    comment_type='&percent_type=m'
if commenttype==3:
    comment_type='&percent_type=l'
txtfile=input("请给爬取的数据放入的txt文件命名（要加后缀，只能是txt文件，如comment.txt。txt文件会被存在本代码所在的文件目录中，如果您想要更改位置，可以在文件名前加上绝对路径):")
m=doubancomment_spider(ip,comment_type,txtfile)
