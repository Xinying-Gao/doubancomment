# doubancomment
#爬取豆瓣短评并进行词云图分析和情感分析

from os import path 
import jieba
import matplotlib.pyplot as plt
import numpy as np 
from PIL import Image
from wordcloud import WordCloud,ImageColorGenerator

textfile = input("请给爬取的数据放入的txt文件命名（要加后缀，只能是txt文件，如comment.txt。txt文件会被存在本代码所在的文件目录中，如果您想要更改位置，可以在文件名前加上绝对路径):")
backgroundfile = input("请给生成图云希望依照的jpg或png图片文件命名（要加后缀，只能是jpg或png文件，如photo.jpg或picture.png。该文件会被存在本代码所在的文件目录中，如果您想要更改位置，可以在文件名前加上绝对路径):")
w = input("请输入生成词云依照的图片宽度：")
h = input("请输入生成词云依照的图片高度：")
ciyun_name = input("请给生成的词云的jpg或png图片文件命名（要加后缀，只能是jpg或png文件，如photo.jpg或picture.png。该文件会被存在本代码所在的文件目录中，如果您想要更改位置，可以在文件名前加上绝对路径):")

with open(textfile,'r',encoding="utf-8") as file1:
    content = " ".join(file1.readlines())
    content_after = " ".join(jieba.cut(content,cut_all=True))
    content_after = content_after.split(" ")

final_content = ''

with open('stopwordX.txt','r',encoding="utf-8") as file2:
    stop = " ".join(file2.readlines()) 

for i in content_after:
    if i not in stop:
        final_content +=' ' + i


bg = np.array(Image.open(backgroundfile))

wc = WordCloud(font_path="msyh.ttc",\
               background_color="white",
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
from snownlp import SnowNLP
#用户输入情感分析的文本文档，使代码具有开放性
textfile = input("请给爬取的数据放入的txt文件命名（要加后缀，只能是txt文件，如comment.txt。txt文件会被存在本代码所在的文件目录中，如果您想要更改位置，可以在文件名前加上绝对路径):")

#打开文本文档，编码为utf_8模式
with open(textfile,'r',encoding="utf-8") as file2:
    words = file2.readlines()
    #设置一个空的列表来装入情绪值得分
    sentimentslist = []
    
#情感分析并返回情绪值，情绪值大小在0~1之间，越大越积极
for i in words:
    score = SnowNLP(i).sentiments
    sentimentslist.append(score)
#打印情绪值   
print(sentimentslist)


import matplotlib.pyplot as plt
import numpy as np
#使用直接支持生成直方图的方法hist
#桶按照情感值值域设置为起点0、终点1、步长0.01的排列
plt.hist(sentimentslist, bins = np.arange(0, 1, 0.01), facecolor = 'g')
#命名
plt.xlabel('Sentiments Probability')
plt.ylabel('Quantity')
plt.title('Analysis of Sentiments')
plt.show()


