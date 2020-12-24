import json
import re
import bs4
import string
import os
dic={}
def getHTMLfile(html_path):
    with open(html_path,"r",encoding="utf-8") as f:
        htmlfile = f.read()
    html_string_list=str(htmlfile).split("<br/>")
    html_string="".join(html_string_list)
    return bs4.BeautifulSoup(html_string,'lxml')
def work(html_path,pid,pname):
    soup = getHTMLfile(html_path)#得到网页源码
    table = soup.findAll("td")
    for i in range(len(table)):
        table[i]=bs4.BeautifulSoup(str(table[i]),"html.parser").text
    for i in range(len(table)):
        table[i] = "".join(table[i].split())
    global dic
    cnt = -1
    for i in range(len(table)):# 提取出所有table标签
        if("包号" == table[i]):
            cnt = i
            break
    # print("cnt=",cnt)
    try:
        if(cnt == -1):
            raise Exception("Can't find 包号 in page,id="+id)
    except:
        print("Can't find 包号 in page,id="+id)
    table=table[cnt:len(table)]# 
    attr=[]
    for i in range(len(table)):
        if(table[i] == "第1包"):# 从table里面找到包号的属性列表
            break
        attr.append(table[i])
    # print(attr)
    cnt = 0

    # 现在能找到所有的包信息，每个包有供应商名称，和金额
    name=""
    money=""
    for line in attr:
        if("金额" in line):
            money=line
        if("名称" in line):
            name=line

    for i in range(len(attr),len(table)):# 提取出第N包信息
        if(re.match('第[0123456789]+包',table[i])==None):
            break
        cnt = cnt + 1
        tmp={}#这里可以把tmp放入到每个中标文件夹下
        for j in range(len(attr)):
            i=i+1
            tmp[attr[j]]=table[i-1]
        tmp_m=0.0
        tmp_m_p = 1
        flag=False
        for i in tmp[money]:
            
            if(i == '.'):
                flag = True
                continue
            if(not(i.isdigit())):
                continue
            if(flag == False):
                tmp_m = tmp_m*10+int(i)
            else:
                tmp_m_p = tmp_m_p*10
                tmp_m = tmp_m + float(i)/tmp_m_p
        if(tmp[name] in dic.keys()):
            dic[tmp[name]]["数量"]=dic[tmp[name]]["数量"]+1
            diclen = dic[tmp[name]]["数量"]
            dic[tmp[name]]["金额"]=dic[tmp[name]]["金额"]+tmp_m
            dic[tmp[name]]["详细信息"][diclen]={"项目编号":pid,"项目名称":pname,"项目预算":tmp_m}
        else:
            dic[tmp[name]]={}
            dic[tmp[name]]["数量"]=1
            dic[tmp[name]]["金额"]=tmp_m
            dic[tmp[name]]["详细信息"]={}
            dic[tmp[name]]["详细信息"][1]={"项目编号":pid,"项目名称":pname,"项目预算":tmp_m}
            dic['CompanyNumber']=dic['CompanyNumber']+1


if __name__=="__main__":
    # global dic
    dic['CompanyNumber']=0
    base_dir=os.path.dirname(os.path.abspath(__file__))
    json_path=base_dir+"/js_table1.json"
    with open(json_path,"r",encoding="utf-8") as f:
        json_file=json.load(f)
    f.close()
    for id in json_file:
        name=json_file[id]["ArticleTitle"]
        html_path=base_dir+"/page1/"+id+"/content.html"
        work(html_path,id,name)
    with open("result.json","w",encoding="utf-8") as f:
        json.dump(dic,f,ensure_ascii=False,indent=4)
    f.close()