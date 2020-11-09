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
if __name__ == "__main__":
    json_file = get_json('./js_table.json')
    sum=0
    dellist=[]
    for id in json_file:
        # print(json_file[id])
        if(json_file[id]['ColumnName'][0:8] == '采购需求征求意见'):
            sum=sum+1
            print(str(sum)+":"+id+"、"+delete_path("./page/"+id))
            dellist.append(id)
    for id in dellist:
        del json_file[id]
    with open("js_table.json","w") as f:  
        json.dump(json_file,f,indent=4)      
        # html_path="./page/"+id+"/content.html"
        # print(html_path)
        # with open(html_path,"r",encoding="utf-8") as f:
        #     html_content=f.read();
        # bs_xml=bs4.BeautifulSoup(html_content)
        # print(bs_xml)
        # break