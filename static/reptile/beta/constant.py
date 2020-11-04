import os
import random

TimeLimit = 3000

version=1.0

local_Dir=os.getcwd()

top_dir='''http://www.ccgp-tianjin.gov.cn/'''

initial_Dir='''http://www.ccgp-tianjin.gov.cn/portal/topicView.do?id=1662'''

init_header = {
    "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}


debug_pages = 2**30

page_contains = ['SiteName','SiteDomain','SiteIDCode','ColumnName','ArticleTitle','PubDate']
pa_contains = ['url','l','r']

def sleep_time_f():
    return 4+(random.random()-0.5)*1

def turn_page_on(url,x) :
    return url.rsplit('&',1)[0]+'&page='+str(x)