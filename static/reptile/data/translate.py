import bs4
import json
import shutil
import stat
import os




def delete_path(file_path):
    if os.path.exists(file_path):
        for fileList in os.walk(file_path):
            for name in fileList[2]:
                os.chmod(os.path.join(fileList[0],name), stat.S_IWRITE)
                os.remove(os.path.join(fileList[0],name))
        shutil.rmtree(file_path)
        return "delete ok"
    else:
        return "no filepath"

def get_json(file_path):
    f = open(file_path)
    ret=json.load(f)
    f.close()
    return ret

def find_project_id(file):
    return file.find_all('div',attrs={'class':'segement','class':'line'})
def find_project_name(file):
    return file.find_all('div',attrs={'class':'line'})
def count_wining_source(file):
    now = file.find('table',attrs={'id':'projectBundleList'})
    now = now.find_all('tr',attrs={'class':False})
    ans = []
    for it in now:
        v = it.find_all('td')
        ans.append((v[1].text.strip(),v[3].text.strip()))
    return ans

if __name__ == "__main__":
    file_path = os.getcwd()+"/data/js_table.json"
    print(file_path)
    with open(file_path,"r",encoding='utf-8') as f:
        json_file = json.load(f)
    f.close()
    sum=0
    dellist=[]
    for id in json_file:
    #     # print(json_file[id])
    #     if(json_file[id]['ColumnName'][0:8] == '采购需求征求意见'):
    #         sum=sum+1
    #         print(str(sum)+":"+id+"、"+delete_path("./page/"+id))
    #         dellist.append(id)
    # for id in dellist:
    #     del json_file[id]
    # with open("js_table.json","w") as f:  
    #     json.dump(json_file,f,indent=4)      
        html_path=os.getcwd()+"/data/page/"+id+"/content.html"
        # print(html_path)
        with open(html_path,"r",encoding="utf-8") as f:
            html_content=f.read();
        f.close()
        bs_xml=bs4.BeautifulSoup(html_content)
        with open("tmp.html","w",encoding="utf-8") as f:
            f.write(str(bs_xml))
        f.close()
        # print(bs_xml)
        bags = count_wining_source(bs_xml)
        # print("bags=",bags)
        project_id = find_project_id(bs_xml)
        # print("project_id=",project_id)
        project_name = find_project_name(bs_xml) 
        # print("project_name=",project_name)         
        break