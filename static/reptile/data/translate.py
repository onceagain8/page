import bs4
import re
import json
import os
import sys
print("\n".join(sys.path))

def getHTMLfile(html_path):
    with open(html_path,"r",encoding="utf-8") as f:
        htmlfile = f.read()
    html_string_list=str(htmlfile).split("<br/>")
    html_string=""
    for string in html_string_list:
        html_string=html_string+string
    return bs4.BeautifulSoup(html_string,'lxml')

def get_overview(main_div):
    head_div = main_div.findAll('div')[0]
    overview = head_div.findAll('div',{'class':'line'})[0]
    overview = bs4.BeautifulSoup(str(overview),"html.parser").text
    overview = " ".join(str(overview).split())
    return overview

def get_title(main_div):
    final_title = [s.extract() for s in main_div("b")][0]#找到项目名称
    final_title = bs4.BeautifulSoup(str(final_title),'html.parser').text
    return final_title.split()

def get_table(table):
    tr_list = table.findAll('tr')
    ret = {}
    item = bs4.BeautifulSoup(str(tr_list[0]),"html.parser").text.split()

    count = 0
    for line in tr_list[1:len(tr_list)]:
        count = count + 1
        tmpdic = {}
        linestring = bs4.BeautifulSoup(str(line),"html.parser").text
        linelist = linestring.split()
        for id in range(len(linelist)):
            tmpdic[item[id]] = linelist[id]
            ret[count] = tmpdic
        # print(tmpdic)
    return ret
def get_base(main_div):
    final_base = {}
    head_div = main_div.findAll('div')[0]
    # div_list = head_div.findAll('div')
    table = [s.extract() for s in head_div('table')][0]
    tmp = head_div.findAll('div',{'class':'line'})
    for line in tmp:
        linestring = str(bs4.BeautifulSoup(str(line),"html.parser").text)
        linestring = "".join(linestring.split())
        item = re.split("[:|：]",linestring)
        if(item[0] == '采购需求'):
            item[1] = get_table(table)
        if(len(item) == 1):
            final_base['其他'] = item[0]
        else:
            final_base[item[0]] = item[1]
        # print(item)
    return final_base
def get_2(main_div):
    div_2=main_div.findAll('div')[0]
    div_2.decompose()
    div_list = main_div.findAll('div')
    ret = {}
    count = 0
    for div in div_list:
        if(div['class'] == ['segement']):
            break;
        count = count+1
        divstring = bs4.BeautifulSoup(str(div),"html.parser").text
        divstring = " ".join(divstring.split())
        ret[count]=divstring
    for div in div_list:
        if(div['class'] == ['segement']):
            break
        div.decompose()
    return ret
def get_3(main_div):
    div_3=main_div.findAll('div')[0]
    div_3.decompose()
    div_list = main_div.findAll('div')
    ret = {}
    count = 0
    for div in div_list:
        if(div['class'] == ['segement']):
            break;
        count = count+1
        divstring = bs4.BeautifulSoup(str(div),"html.parser").text
        divstring = " ".join(divstring.split())
        item = re.split("[:|：]",divstring)
        ret[item[0]]=":".join(item[1:len(item)])
    for div in div_list:
        if(div['class'] == ['segement']):
            break
        div.decompose()
    # print(ret)
    return ret
def get_7(main_div):
    div_7 = main_div.findAll('div')[0]
    div_7.decompose()
    div = main_div.findAll('div')[0];
    divstring = bs4.BeautifulSoup(str(div),"html.parser").text
    linelist = divstring.split()
    ret = {}
    for line in range(len(linelist)):
        ret[line+1] = linelist[line]
    div.decompose()
    return ret

def get_8(main_div):
    div_8 = main_div.findAll('div')[0]
    div_8.decompose()
    divlist = main_div.findAll('div')
    ret = {}
    pre = ""
    for div in divlist:
        if(div['class'] == ['segement']):
            break
        divstring = bs4.BeautifulSoup(str(div),"html.parser").text
        divstring = "".join(divstring.split())
        if((":" in divstring)or("：" in divstring)):
            item = re.split("[:|：]",divstring)
            ret[pre+","+item[0]] = item[1]
        else:
            # print("WRONG:"+divstring)
            pre = divstring.split(".")[1]
    # print (ret)
    return ret
    

def trans(html_path):
    soup = getHTMLfile(html_path)#得到网页源码


    main_div = soup.findAll('div',{'class':'pageInner'})#提取出主要信息在的div
    main_div = main_div[0].findAll('td')#继续删除外部没有用的标签
    del_div = main_div[0].findAll('div',{'id':'crumbs'})#删除导航栏
    del_script=main_div[0].findAll('script')#删除script部分代码
    del_style =main_div[0].findAll('style')#删除css样式
    for d in del_div:
        d.decompose()
    for d in del_script:
        d.decompose()
    for d in del_style:
        d.decompose()

    #下面开始提取信息，提取到的信息会进行删除操作。
    
    #提取标题
    final_title=get_title(main_div[0])
    # print(final_title)
    #[0:发起机关，1:项目名称，2：项目编号及方式]
    #删除项目于名称所在的标签块。
    del_p1 = main_div[0].findAll('p',{'align':'center'})
    for d in del_p1:
        d.decompose()

    #提取项目概况
    final_overview = get_overview(main_div[0])
    # 项目名称 采购项目的潜在供应商应在 地点 获取采购文件，并于 时间 （北京时间）前提交响应文件。
    del_overview = main_div[0].findAll('div')[0].findAll('div')[0]
    del_overview.decompose()
    
    del_colgroup = main_div[0].findAll('colgroup')[0]
    del_colgroup.decompose()

    #一、项目基本情况
    final = [[] for x in range(0,10)]
    final[1] = get_base(main_div[0])
    main_div[0].findAll('div')[0].decompose()

    #二、申请人的资格要求
    final[2] = get_2(main_div[0])#同时删除
    #三、获取采购文件
    final[3] = get_3(main_div[0])
    #四、响应文件提交
    final[4] = get_3(main_div[0])
    #五、开启
    final[5] = get_3(main_div[0])
    #六、公告期限
    final[6] = get_2(main_div[0])
    # print(final_6)
    #七、其他补充事宜
    final[7] = get_7(main_div[0])
    # print(final_7)
    # 八、联系方式
    final[8] = get_8(main_div[0])
    with open("result.html","w",encoding='utf-8') as f:
        f.write(str(main_div[0]))
    f.close()
    itemlist=["一、项目基本情况","二、申请人的资格要求","三、获取采购文件","四、响应文件提交",
    "五、开启","六、公告期限","七、其他补充事宜","八、联系方式"]
    final_dic={}
    final_dic["标题"]=final_title
    final_dic["项目概况"] = final_overview
    for i in range(len(itemlist)):
        final_dic[itemlist[i]] = final[i+1]
    return final_dic

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
        # print(dic)
        with open(base_path+"/page/"+json_id+"main.json","w",encoding='utf-8')as f:
            json.dump(dic,f,ensure_ascii=False,indent=4)
        f.close()