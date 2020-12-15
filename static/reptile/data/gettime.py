import os
import re
import bs4
import json
import sys
def getHTMLfile(html_path):
    with open(html_path,"r",encoding="utf-8") as f:
        htmlfile = f.read()
    html_string_list=str(htmlfile).split("<br/>")
    html_string=""
    for string in html_string_list:
        html_string=html_string+string
    return bs4.BeautifulSoup(html_string,'html.parser').text

def trans(html_path):
    soup = str(getHTMLfile(html_path))#得到网页源码
    soup="".join(soup.split())
    # soup.decompose()
    # print(soup)
    dl = re.finall(r"\d{4}年\d{1,2}月\d{1,2}日",soup)
    print(dl)
    return 0
if __name__ == "__main__":
    html_dic = {}
    base_path = os.path.dirname(__file__)
    with open(base_path+"/js_table.json","r",encoding="utf-8")as f:
        html_dic = json.load(f)
    f.close()
    for json_id in html_dic.keys():
        html_path = base_path + "/page/"+json_id+"/content.html"
        print("begin:"+json_id)
        try:
            dic = trans(html_path)
        except BaseException:
            print("Eror :"+json_id)
        else:
            print("finished:"+json_id)
            with open(base_path+"/page/"+json_id+"/main.json","w",encoding='utf-8')as f:
                json.dump(dic,f,ensure_ascii=False,indent=4)
            f.close()
        break