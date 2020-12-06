import json
import os
import constant as con
js_table={}
def init():
    global js_table
    print(os.path.join(con.local_Dir,'data','js_table1.json'))
    #js_table.json文件是招标文件
    #js_table1.json文件是中标文件
    with open(os.path.join(con.local_Dir,'data','js_table1.json'),'r') as cin:
        s=cin.read()
        js_table=json.loads(s)
init()
def close():
    with open(os.path.join(con.local_Dir,'data','js_table1.json'),'w') as fout:
        fout.write(json.dumps(js_table,indent=4))