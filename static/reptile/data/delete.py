import os
import json
import copy
import shutil
base_dir=os.path.dirname(os.path.abspath(__file__))
page1 = base_dir+"/page1"
js_table={}
with open(base_dir+"/js_table1.json","r",encoding="utf-8") as f:
    js_table=json.load(f)
f.close()

tmp=copy.deepcopy(js_table)
for id in js_table:
    if ('终止公告' in js_table[id]['ArticleTitle']):
        tmp.pop(id)
        content_dir=base_dir+"/page1/"+id
        try:
            shutil.rmtree(content_dir)
        except:
            print("file not found")
with open(base_dir+"/js_table1.json","w",encoding='utf-8')as f:
    json.dump(tmp,f,ensure_ascii=False,indent=4)
f.close()