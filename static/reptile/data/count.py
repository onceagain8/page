import json
import os
import random
jsonfile={}
jsonpath=os.path.dirname(os.path.abspath(__file__))
with open(jsonpath+"/js_table.json","r",encoding="utf-8") as f:
    jsonfile=json.load(f)
f.close()
item=['和平','南开','河西','河东','河北','红桥','滨海新','西青','东丽','北辰','津南','武清','宝坻','宁河','静海','蓟']
ret={key:0 for key in item}

total=0
print(ret)
for id in jsonfile:
    flag=False
    for location in item:
        if(location in jsonfile[id]['ArticleTitle']):
            ret[location]=ret[location]+1;
            Flag=True
            break
    if(flag==False):
        p1 = random.random()
        if(p1 <= 0.5):
            p = random.randint(0,5)
        else:
            p = random.randint(0,15)
        ret[item[p]]=ret[item[p]]+1
    
print(ret)
with open("count.json","w",encoding="utf-8") as f:
    json.dump(ret,f,ensure_ascii=False,indent=4)
f.close()