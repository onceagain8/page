import json
import os
import constant as con
js_table={}
def init():
    global js_table
    print(os.path.join(con.local_Dir,'data','js_table.json'))
    with open(os.path.join(con.local_Dir,'data','js_table.json'),'r') as cin:
        s=cin.read()
        js_table=json.loads(s)
init()
def close():
    with open(os.path.join(con.local_Dir,'data','js_table.json'),'w') as fout:
        fout.write(json.dumps(js_table,indent=4))