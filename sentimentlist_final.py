# -*- coding: utf-8 -*-
#情感分析
#author谢乐滋 2018202008
'''
实现功能——对用户导入的文本文档进行情感分析并输出情感得分分布的条形统计图
设计亮点——文件文本可以用户自己输入，代码具有广泛适用性；
          
'''

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
