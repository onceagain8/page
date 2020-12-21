from bs4 import BeautifulSoup as BS
import constant as con
import GrabSignlePage as SP
import requests
import re
import os
import verb
import chardet

head_name_table = set(['SiteName','SiteDomain','SiteIDCode','ColumnName','ArticleTitle','PubDate'])

def get_head(file) :
    now = file.find_all('meta',attrs={'name':True})
    table = {}
    for it in now:
        if (it['name'] in head_name_table):
            table[it['name']] = it['content']
    return table

def get_content(file) :
    now = file.find('div',id='pageContent')
    return now.prettify()

def get_accessory(file):
    now = file.find_all('a',href=re.compile(r'/stock/'),target='_blank')
    if not now :
        return 
    if len(now) >1 :
        raise Exception("Error, more than one accessory with code 192si4")
    now=now[0]
    return (now.text,now['href'])

def make_content(now_dir,content):
    with open(os.path.join(now_dir,'content.html'),'w',encoding='UTF-8') as fout:
        fout.write(content)

def make_accessory(now_dir,item) :
    if not item:
        return 
    try:
        with open(os.path.join(now_dir,item[0]),'wb') as fout:
            file_dir = os.path.join(con.top_dir,item[1][1:])
            now = requests.get(file_dir,headers=con.init_header,stream=True)
            for it in now.iter_content(chunk_size=512):
                if it:
                    fout.write(it)
    except Exception:
        return

def grab(text,id,url):
    file = requests.get(url,headers=con.init_header,verify=False)
    if file.status_code != 200:
        raise Exception("Error cannot open url(%s) with code 07823u"%url)
    file.encoding = chardet.detect(file.content)['encoding']

    file = BS(file.text,"html.parser")
    head = get_head(file)
    content = get_content(file)
    accessory = get_accessory(file)
    head['note']=text
    print(head['ArticleTitle'],head['note'])
    now_dir = os.path.join(con.local_Dir,'data','page1',str(id))
    #page存储的是招标文件
    #page1存储中标文件
    if not os.path.exists(now_dir):
        os.makedirs(now_dir)
    
    make_content(now_dir,content)
    make_accessory(now_dir,accessory)
    
    verb.js_table[str(id)] = head
    return True