import jieba
import jieba.analyse
import os
from lxml import etree
sentence=""
path=os.getcwd()
# print('path=%s'%path)
with open('%s\\static\\reptile\\test.html'%path,'r',encoding='utf-8') as f:
    sentence = f.read()
# print(sentence)
root = etree.HTML(sentence)
for i in range(len(root)):
    for j in range(len(root[i])):
        print (root[i][j])
HTMLtext=root.xpath("//table/tbody/tr/td/text()")
print(HTMLtext)
