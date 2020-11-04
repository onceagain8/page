import constant as con
import GrabSignlePage as SP
import requests
import re
import time
import verb
from bs4 import BeautifulSoup as BS
def get_max_pages(file) :
    max_page=file.find("span",class_="countPage").b.text
    return int(max_page)

def make_pages(text,file):
    pages=re.finditer(r'/viewer\.do\?id=([0-9]*)&amp;ver=2',file.prettify())
    pages= [(it.group(1),con.top_dir[:-1]+it.group()) for it in pages]
    for it in pages:
        if it[0] not in verb.js_table:
            SP.grab(text,int(it[0]),it[1])
            time.sleep(con.sleep_time_f())

def grab(url,text,l=None,r=None):

    file=requests.get(url,headers=con.init_header,timeout=con.TimeLimit)
    if file.status_code != 200:
        raise Exception("Error,cannot visit url(%s)"%(url))
    file=BS(file.text,'html.parser')
    max_page=min(get_max_pages(file),con.debug_pages)

    if l==None:
        l=1
    if r==None:
        r=max_page
    else:
        r=min(r,max_page)
    if type(l)!=int or type(r)!=int or l<0 or r<0 or l>r :
        raise Exception("Page Number Error")

    url=url +'&page='+str(l)
    for i in range(l,r+1):
        time.sleep(con.sleep_time_f())
        url=con.turn_page_on(url,i)
        file = requests.get(url,headers=con.init_header,timeout=con.TimeLimit)
        if file.status_code != 200:
            raise Exception("Error,cannot open page%d"%i)
        file=BS(file.text,'html.parser')
        make_pages(text,file)
        with open('temp.html','w',encoding="UTF-8") as cout:
            cout.write(file.prettify())
        print('Complete page %d'%i)
