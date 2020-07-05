#!/usr/bin/env python
# coding: utf-8

# In[1]:


#可以自动登录、爬任意影片、选择评论类型的的豆瓣网络爬虫. 
#author:高心莹 2018201953
import time
import random
from selenium import webdriver

class doubancomment_spider():
    def __init__(self,ip,comment_type,txtfile):
        # 声明用的是谷歌浏览器
        driver=webdriver.Chrome()
        #定义对象属性
        self.ip=ip
        self.comment_type=comment_type
        self.txtfile=txtfile
        self.get_comment(driver,ip,comment_type,txtfile)
    def get_comment(self,driver,ip,comment_type,txtfile):
        #一、登陆豆瓣
        # 切换到登录框架中
        driver = driver
        driver.get("http://www.douban.com/")
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
        # 点击"密码登录"
        bottom1 = driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
        bottom1.click()
        # 输入账号
        input1 = driver.find_element_by_xpath('//*[@id="username"]')
        input1.clear()#清空原有内容
        input1.send_keys("13346775941")
        #输入密码
        input2 = driver.find_element_by_xpath('//*[@id="password"]')
        input2.clear()#清空原有内容
        input2.send_keys("yl1xhdxs")
        # 点击登录按钮
        bottom = driver.find_element_by_class_name('account-form-field-submit ')
        bottom.click()
        
        #停留一定时长
        time.sleep(1)
        
        #二、爬取评论并写入文件
        i = 0
        txtlist = []
        while i<25:#即使登录了，豆瓣也只能看到前500条评论，
             num = i*20
             #打开网址
             url = "https://movie.douban.com/subject/"+str(ip)+"/comments?start=" + str(num) +"&amp;limit=20&amp;sort=new_score&amp;status=P"+str(comment_type)
             print(url)#只是为了方便看爬到哪了
             time.sleep(0.5 + float(random.randint(1, 20)) / 20)#以不均匀的时间翻动页面，防止被识别出
             driver.get(url)  
             #找到本页中的全部评论，生成一个列表
             commentlist = driver.find_elements_by_xpath("//span[@class='short']")
             #循环写入20行评价
             k = 0
             while k<20:#只能爬取满20条的页面，爬到不满20条的页就会报错，不过即使报错，在这一页之前的完整页面的数据都爬下来了。
                  comment = commentlist[k].text
                  print(comment)
                  txtlist.append(comment)
                  k = k + 1
             i = i + 1
            #写入txt文件
             with open(txtfile,"w",encoding='utf-8') as f:
                 for x in txtlist:
                      f.write(x)
                      f.write('\n')#分行是便于情感分析
                 f.close#关闭文档
#乘风破浪的姐姐ip:34894589  
#储存位置：C:\\Users\\dell\\编程语言基础\\浪姐                 
ip=input("请输入想要爬取的影视节目的ip（在豆瓣电影中点开想要爬取的影视节目的页面，页面链接中'subject/'后面的一串数字即为影片ip)：")
commenttype=int(input("您想要爬取的评论类型为：（全部类型请输入0，好评请输入1，中评请输入2，差评请输入3）："))
#将输入评论类型的的值转化成评论类型对应的链接片段
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


#jieba分词与wordcloud词云图生成
#author：谢乐滋 2018202008
#实现功能——通过jieba对用户导入的文本文档进行分词并去除停用词，再用wordcloud和matplotlib生成词云图
#设计亮点——用户自选词云底图、词云图尺寸、词云图命名，具有较广泛的适用性；利用停用词表尽量去除没有分析意义的代词、助词、语气词、冠词，提高词云图的质量

from os import path 
import jieba
import matplotlib.pyplot as plt
import numpy as np 
from PIL import Image
from wordcloud import WordCloud,ImageColorGenerator

#依照的图片：C:\\Users\\dell\\编程语言基础\\彩虹500x375.jpg
#储存位置：C:\\Users\\dell\\编程语言基础\\浪姐
backgroundfile = input("请给生成图云希望依照的jpg或png图片文件命名（要加后缀，只能是jpg或png文件，如photo.jpg或picture.png。该文件会被存在本代码所在的文件目录中，如果您想要更改位置，可以在文件名前加上绝对路径):")
w = input("请输入生成词云依照的图片宽度（像素）：")
h = input("请输入生成词云依照的图片高度（像素）：")
ciyun_name = input("请给生成的词云的jpg或png图片文件命名（要加后缀，只能是jpg或png文件，如photo.jpg或picture.png。该文件会被存在本代码所在的文件目录中，如果您想要更改位置，可以在文件名前加上绝对路径):")

with open(txtfile,'r',encoding="utf-8") as file1:
    content = " ".join(file1.readlines())
    content_after = " ".join(jieba.cut(content,cut_all=True))
    content_after = content_after.split(" ")

final_content = ''

with open('C:\\Users\\dell\\编程语言基础\\stopwordX.txt','r',encoding="utf-8") as file2:
    stop = " ".join(file2.readlines()) 

for i in content_after:
    if i not in stop:
        final_content +=' ' + i

bg = np.array(Image.open(backgroundfile))

wc = WordCloud(font_path="msyh.ttc",               background_color="white",
               scale=4,
               collocations = False,
               max_words=800,max_font_size=350,width=w,height=h,
               mask = bg)

wc.generate(final_content)
image_colors = ImageColorGenerator(bg)

wc.recolor(color_func=image_colors)

wc.to_file(ciyun_name)

plt.imshow(wc)
plt.axis('off')
plt.show()

#情感分析
#author谢乐滋 2018202008
#实现功能——对用户导入的文本文档进行情感分析并输出情感得分分布的条形统计图          

from snownlp import SnowNLP
#打开文本文档，编码为utf_8模式
with open(txtfile,'r',encoding="utf-8") as file2:
    words = file2.readlines()
    #设置一个空的列表来装入情绪值得分
    sentimentslist = []
    
#情感分析并返回情绪值，情绪值大小在0~1之间，越大越积极
for i in words:
    score = SnowNLP(i).sentiments
    sentimentslist.append(score)
#打印情绪值   
print(sentimentslist)

#使用直接支持生成直方图的方法hist
#桶按照情感值值域设置为起点0、终点1、步长0.01的排列
plt.hist(sentimentslist, bins = np.arange(0, 1, 0.01), facecolor = 'g')
#命名
plt.xlabel('Sentiments Probability')
plt.ylabel('Quantity')
plt.title('Analysis of Sentiments')
plt.show()


# In[ ]:




