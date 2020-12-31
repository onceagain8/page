import json

json_dic={}
with open("./result.json","r",encoding="utf-8") as f:
    json_dic = json.load(f)
f.close()

company_name=json_dic.keys()
number_first={}
money_first={}
for company in company_name:
    if(company == "CompanyNumber"):
        continue
    # print(company)
    number_first[company]=json_dic[company]["数量"]
    money_first[company] =round(json_dic[company]["金额"],4)

number_first=sorted(number_first.items(),key=lambda d:d[1],reverse=True)
money_first=sorted(money_first.items(),key=lambda d:d[1],reverse=True)
cnt = 1
for line in number_first:
    json_dic[line[0]]["数量排名"]=cnt
    cnt = cnt + 1
cnt = 1
for line in money_first:
    json_dic[line[0]]["金额排名"]=cnt
    cnt = cnt + 1
with open("number.json","w",encoding="utf-8") as f:
    json.dump(number_first,f,ensure_ascii=False,indent=4)
f.close()
with open("money.json","w",encoding="utf-8") as f:
    json.dump(money_first,f,ensure_ascii=False,indent=4)
f.close()
with open("result1.json","w",encoding="utf-8") as f:
    json.dump(json_dic,f,ensure_ascii=False,indent=4)
f.close()