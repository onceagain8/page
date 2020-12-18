import os

import verb
import constant as con
import GrabPages
import GrabError
import mainTools


if 0:
    print('running :')
    while True:
        print(mainTools.run(input()))
if __name__ == "__main__":
    try:
        with open('./beta/采购网目录.txt','r',encoding='utf-8') as fin:
            网页目录 = fin.readlines()
        for line in 网页目录:
            最上级网址,备注 = line.split()
            print(f'\033[41m正在爬取{最上级网址}({备注})\033[0m')
            GrabPages.grab(最上级网址,备注,l=2000,r=4000)
    except Exception as e:
        GrabError.write_error(con.local_Dir,e)
    verb.close()