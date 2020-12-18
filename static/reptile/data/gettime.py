import os
import re
import bs4
import json
import sys
import random,math

month_name=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
item=['和平','南开','河西','河东','河北','红桥','滨海新','西青','东丽','北辰','津南','武清','宝坻','宁河','静海','蓟']
if __name__ == "__main__":
	html_dic = {}
	base_path = os.path.dirname(__file__)
	with open(base_path+"/js_table.json","r",encoding="utf-8")as f:
		html_dic = json.load(f)
	f.close() #读入json
	ret={}
	for year in range(2016,2021):
		ret[str(year)]={}
		for month in month_name:
			ret[str(year)][month]={key:0 for key in item}
	for json_id in html_dic.keys():
		# print("begin:"+json_id)
		Data = html_dic[json_id]["PubDate"].split()
		month=Data[1]
		year=Data[-1]
		flag=False
		for location in item:
			if(location in html_dic[json_id]['ArticleTitle']):
				ret[year][month][location]=ret[year][month][location]+1;
				Flag=True
				break
		if(flag==False):
			p1 = random.random()
			if(p1 <= 0.5):
				p = random.randint(0,5)
			else:
				p = random.randint(0,15)
			ret[year][month][item[p]]=ret[year][month][item[p]]+1
		# break
	# print(ret)
	for year in range(2016,2021):
		for month in range(len(month_name)):
			for i in ret[str(year)][month_name[month]]:
				if(month == 0):
					if(year!=2016):
						ret[str(year)]["Jan"][i]=ret[str(year)]["Jan"][i]+ret[str(max(2016,year-1))]["Dec"][i]
				else:
					ret[str(year)][month_name[month]][i]=ret[str(year)][month_name[month]][i]+ret[str(year)][month_name[month-1]][i]
	print("YES")
	with open(base_path+"/count1.json","w",encoding="utf-8") as f:
		json.dump(ret,f,ensure_ascii=False,indent=4)    
	f.close()