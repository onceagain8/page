import sqlite3
import json
from bs4 import BeautifulSoup as BS

def strstr(s):
    return '\''+s+'\''

def make_line(wining_source,project_name,project_id,wining_amount,index):
    return f'''
        INSERT INTO wining (
            wining_source,
            project_name,
            project_id,
            wining_amount,
            project_seq
        ) VALUES (
            {strstr(wining_source)},
            {strstr(project_name)},
            {strstr(project_id)},
            {strstr(wining_amount)},
            {strstr(index)}
        );
    '''
def find_project_id(file):
    return file.find_all('div',attrs={'class':'segement'})[0].text.strip().split(':')[1]
def find_project_name(file):
    return file.find_all('div',attrs={'class':'segement'})[1].text.strip().split(':')[1]
def count_wining_source(file):
    now = file.find('table',attrs={'id':'projectBundleList'})
    now = now.find_all('tr',attrs={'class':False})
    ans = []
    for it in now:
        v = it.find_all('td')
        ans.append((v[1].text.strip(),v[3].text.strip()))
    return ans

def insert_wining(file,index):
    global cur,db
    bags = count_wining_source(file)
    project_id = find_project_id(file)
    project_name = find_project_name(file)
    for it in bags:
        s=make_line(it[0],project_name,project_id,it[1],index)
        print(s)
        print(db)
        cur.execute(s)
        input()

db = sqlite3.connect('./sql/test.db')
cur=db.cursor()
cur.execute('SET IDENTITY_INSERT wining OFF;')
with open('./data/js_table.json') as f:
    js_table = json.load(f)
for index in js_table:
    if js_table[index]['note'] not in ['采购结果公告-市级','采购结果公告-区级']:
        continue
    with open(f'./data/page/{index}/content.html','r',encoding= 'utf-8') as f:
        file=BS(f.read(),'html.parser')
    insert_wining(file,index)
