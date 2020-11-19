import bs4
import json
import shutil
import stat
import os




# def delete_path(file_path):
#     if os.path.exists(file_path):
#         for fileList in os.walk(file_path):
#             for name in fileList[2]:
#                 os.chmod(os.path.join(fileList[0],name), stat.S_IWRITE)
#                 os.remove(os.path.join(fileList[0],name))
#         shutil.rmtree(file_path)
#         return "delete ok"
#     else:
#         return "no filepath"

def get_json(file_path):
    f = open(file_path)
    ret=json.load(f)
    f.close()
    return ret


if __name__ == "__main__":
    file_path = "./static/reptile/data/js_table.json"
    print(file_path)
    with open(file_path,"r",encoding='utf-8') as f:
        json_file = json.load(f)
    f.close()
    dellist=[]
    for id in json_file:     
        html_path="./static/reptile/data/page/"+id+"/content.html"
        # print(html_path)
        with open(html_path,"r",encoding="utf-8") as f:
            html_content=f.read();
        f.close()
        bs_xml=bs4.BeautifulSoup(html_content)
        with open("tmp.html","w",encoding="utf-8") as f:
            f.write(str(bs_xml))
        f.close()