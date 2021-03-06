from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
# from flask_pageinate import Pageination,get_page_parameter
import os
import json
import sys
app = Flask(__name__)

date_file='/static/reptile/'



# 首页
@app.route('/')
def index(): 
    return render_template("index.html")
# 搜索算法
def getmatchval(s1,s2):
    len1 = len(s1)
    len2 = len(s2)
    ret = 0
    for i in range(0,len1):
        k = 0
        for j in range(i,len1):
            if(k < len2 and s1[j] == s2[k]):
                k = k+1
        ret = max(ret,k)
    # print('ret = %d'%ret)
    return ret
#搜索后结果显示页面
@app.route('/resultlist',methods=['GET','POST'])
def resultlist():
    typed=request.form.get('type')
    s=request.form.get('search')
    return render_template('resultlist.html',typed=typed,s=s)

#搜索后的结果显示页面api（调用搜索引擎）
@app.route('/api/resultlist/<typed>/<s>')
def apiresultlist(typed,s):
    print(typed+" "+s)
    print('len = %d'%len(s))
    if(typed == "招标公告"):
        f = open('.'+date_file+'data/js_table.json','r',encoding="utf-8")
        #招标公告json文件
    elif(typed == "中标公告"):
        f = open('.'+date_file+'data/js_table1.json','r',encoding="utf-8")
        #中标公告json文件
    d = json.load(f)
    f.close()
    ans=0
    resultlist={}
    for it in d:
        if(s in d[it]['ArticleTitle']):
            resultlist[str(ans)]=(it,d[it]['ArticleTitle'])
            ans = ans + 1
    resultlist["total"] = ans
    print("finished find")
    return jsonify(resultlist)#传回json文件。

#这个展示的是文档
@app.route('/show/<typed>/<pro_id>')
def show(typed,pro_id):
    return render_template('show.html',typed=typed,pro_id=pro_id)

#招标中标文件api
@app.route('/api/show/<typed>/<json_id>')
def find(typed,json_id):
    page="page"
    if(typed == "中标公告"):
        page="page1"
    nowpath=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static','reptile','data',page, json_id, 'main.json')
    htmlpath=os.path.join(os.path.dirname(os.path.abspath(__file__)),'static','reptile','data',page, json_id,'content.html')
    print(nowpath)
    if (os.path.exists(nowpath)):
        dic = {}
        with open(nowpath,"r",encoding="utf-8")as f:
            dic=json.load(f)
        f.close()
        return jsonify(dic)
    html_content=""
    with open(htmlpath,"r",encoding="utf-8") as f:
        html_content=f.read()
    f.close()
    return '404\n'+html_content
#分时间展示招标分布的api
@app.route('/api/zdata/<year>/<int:month>')
def zdata(year,month): 
    month_mapping={1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    nowpath=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static','reptile','data','count1.json')
    with open(nowpath,"r",encoding="utf-8") as f:
        zdata_dic=json.load(f)
    f.close()
    month=month_mapping[month]
    return jsonify(zdata_dic[year][month])

# 查询排名的api
@app.route('/api/rank/<type>')
def get_numberjson(type):

    if(type == 'number'):
        filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)),'static','reptile','data','number.json')
    elif(type == 'money'):
        filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)),'static','reptile','data','money.json')
    else:
        return '404'
    with open(filepath,"r",encoding='utf-8') as f:
        ret_dic=json.load(f)
    f.close()
    return jsonify(ret_dic)
@app.route("/company/<string:name>")
def welcomecompany(name):
    return render_template("company.html",name=name)

@app.route("/company/t/<string:name>")
def showcompany(name):
    print(name)
    return render_template("company_show.html",name=name)

#用来反馈排行榜部分企业详细信息api
@app.route("/api/company/<string:name>")
def apifind(name):
    json_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'static','reptile','data','result.json')
    with open(json_path,"r",encoding="utf-8") as f:
        json_dic=json.load(f)
    if(name in json_dic.keys()):
        return jsonify(json_dic[name])
    return "404"
# 导航栏
@app.route('/game/2048')
def game_2048():
    return render_template('/game/2048.html')
@app.route('/game/snake')
def game_snake():
    return render_template('/game/snake.html')
@app.route('/game')
def game():
    return render_template('game.html')
@app.route('/gov')
def gov():
    return render_template('gov.html')
@app.route('/rank/number')
def number():
    return render_template('/rank/number.html')
@app.route('/rank/money')
def money():
    return render_template('/rank/money.html')
@app.route('/login')
def login():
    return render_template('login.html')


if __name__=="__main__":
    app.run(port=12000,host="0.0.0.0",debug=True)