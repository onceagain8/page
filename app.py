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




@app.route('/')
def index(): 
    return render_template("index.html")

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

# @app.route('/resultlist',methods=['post'])
# def resultlist():

#     s=request.form.get('search')
#     print(s)
#     print('len = %d'%len(s))
#     f = open('.'+date_file+'data/js_table.json','r') 
#     d = json.load(f)
#     f.close()
#     match_val={}
#     for it in d:
#         match_val[it]=getmatchval(d[it]['ArticleTitle'],s)
#     ans=0
#     for it in d:
#         if(match_val[it] != len(s) or len(s)==0):
#             continue
#         ans = ans + 1
#     print("finished find")
#     return render_template('resultlist.html',match_val=match_val,d=d,date_file=date_file,Len=len(s),s=s,ans=ans)
@app.route('/resultlist',methods=['GET','POST'])
def resultlist():
    s=request.form.get('search')
    return render_template('resultlist.html',s=s)

@app.route('/api/resultlist/<s>')
def apiresultlist(s):
    print(s)
    print('len = %d'%len(s))
    f = open('.'+date_file+'data/js_table.json','r') 
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
    return jsonify(resultlist)

@app.route('/show/<pro_id>')
def show(pro_id):
    return render_template('show.html',pro_id=pro_id)


@app.route('/api/show/<json_id>')
def find(json_id):
    nowpath=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static','reptile','data','page', json_id, 'main.json')
    print(nowpath)
    if (os.path.exists(nowpath)):
        dic = {}
        with open(nowpath,"r",encoding="utf-8")as f:
            dic=json.load(f)
        f.close()
        return jsonify(dic)
    return '404'



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
@app.route('/cpy')
def cpy():
    return render_template('cpy.html')
@app.route('/login')
def login():
    return render_template('login.html')


if __name__=="__main__":
    app.run(port=12000,host="0.0.0.0",debug=True)