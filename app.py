from flask import Flask
from flask import render_template
from flask import request
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

@app.route('/resultlist',methods=['post'])
def resultlist():
    s=request.form.get('search')
    print(s)
    print('len = %d'%len(s))
    f = open('.'+date_file+'data/js_table.json','r') 
    d = json.load(f)
    f.close()
    match_val={}
    for it in d:
        match_val[it]=getmatchval(d[it]['ArticleTitle'],s)
    ans=0
    for it in d:
        if(match_val[it] != len(s) or len(s)==0):
            continue
        ans = ans + 1
    return render_template('resultlist.html',match_val=match_val,d=d,date_file=date_file,Len=len(s),s=s,ans=ans)

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
    