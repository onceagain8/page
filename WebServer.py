#-*- coding: utf-8 -*-
from socket import *
import os

#建立一个映射,首部与首部内容
def get_header(line_list):
    headers = {}
    for line in line_list:
        new_line = line
        index = new_line.find(':')
        key = new_line[:index]
        value = new_line[index+1:].strip()
        headers[key] = value
    return headers


def operation_GET(message,connectionSocket,headers):
    filename = message.split()[1]                                           #得到GET的地址
    if(filename == '/'): filename="/index.html"                             #规定首页是INDEX.HTML
    f=open('./'+filename,'rb')                                              #打开文件并译码，规定只读
    outputdata = f.read()                                                   #打开指定文件，标记为可读
    header =    'HTTP/1.1 200 OK\r\n' \
                'Connection: close\r\n' \
                'Content-Length: %d\r\n\r\n' % (len(outputdata))
    connectionSocket.send(header.encode()+outputdata)                       #状态行+首部行+实体行
    
def operation_POST(message,connectionSocket,headers):
    if(message.find("undefined") == -1):
        lenth = int(headers["Content-Length"])*10000
        message=connectionSocket.recv(lenth).split('\r\n\r\n'.encode())      #POST命令的第二次读取，读取内容
        name = message[0][message[0].find("filename".encode()):].split("\r\n".encode())[0].split('='.encode())[1]#得到要创建的文件名称
        name = name[1:len(name)-1]                                           #承接上面
        f = open(name.decode(),"wb")                                         #新建一个文件，名字为name
        f.write(message[1])                                                  #写入数据
        header = 'HTTP/1.1 200 OK\r\n' \
                 'Connection: close\r\n'\
                 'Content-Length: 0\r\n\r\n'
        connectionSocket.send(header.encode())
    else:
        connectionSocket.send('HTTP/1.1 404 Not Found\r\nConnection:close\r\n\r\n'.encode())

def operation_PUT(message,connectionSocket,headers):
    if(message.find("undefined") == -1):
        filename = message.split()[1][1:]                                   #得到PUT的地址
        lenth = int(headers["Content-Length"])*10000
        message=connectionSocket.recv(lenth).split('\r\n\r\n'.encode())     #得到PUT第二次报文
        if(os.path.exists(filename)):                                       #首先判断存不存在
            f = open("./"+filename,"wb")                                    #和POST一样了
            f.write(message[1])
            header = 'HTTP/1.1 200 OK\r\n'\
                 'Connection: close\r\n'\
                 'Content-Length: 0\r\n\r\n'
            connectionSocket.send(header.encode())
        else :
            connectionSocket.send('HTTP/1.1 404 Not Found\r\nConnection:close\r\n\r\n'.encode())
    else:
        connectionSocket.send('HTTP/1.1 404 Not Found\r\nConnection:close\r\n\r\n'.encode())

def operation_HEAD(message,connectionSocket,headers):
    filename = message.split()[1]                                   #得到HEAD的地址
    f=open('./'+filename,'rb')                                      #打开文件并译码，规定只读
    outputdata = f.read()
    header =    'HTTP/1.1 200 OK\r\n' \
                'Connection: close\r\n'\
                'Content-Length: %d\r\n\r\n' % (len(outputdata))
    connectionSocket.send(header.encode())                          #状态行+首部行+实体行


def operation_DEL(message,connectionSocket,headers):
    filename = message.split()[1]
    if os.path.exists("./"+filename):                               #首先判断要删除的文件是否存在
        os.remove("./"+filename)                                    #如果存在就删除
        connectionSocket.send('HTTP/1.1 200 OK\r\nConnection:close\r\n\r\n'.encode())
    else:                                                           #不存在就404
        connectionSocket.send("HTTP/1.1 404 Not Found\r\nConnection:close\r\n\r\n".encode())

def running():
    print ('Ready to serve... ')
    connectionSocket, addr = serverSocket.accept()
    print('Accept new connection from %s:%s...' % addr)
    try:
        message =  connectionSocket.recv(1024).decode()             #接收报文
        order = message.split()[0]                                  #得到命令类型
        line_list=message.split('\r\n')                             #按照回车和换行依次分割报文
        headers=get_header(line_list)                               #headers得到一个报文映射
        for i in line_list:         print(i)                        #输出报文
        if   (order == 'GET') :     operation_GET(message,connectionSocket,headers)
        elif (order == 'POST') :    operation_POST(message,connectionSocket,headers)
        elif (order == 'PUT'):      operation_PUT(message,connectionSocket,headers)
        elif (order == 'DELETE'):   operation_DEL(message,connectionSocket,headers)
        else :                      operation_HEAD(message,connectionSocket,headers)
        connectionSocket.close()
    except IOError:
        connectionSocket.send('HTTP/1.1 404 Not Found\r\nConnection:close\r\n\r\n'.encode())
        connectionSocket.close()

serverSocket = socket(AF_INET, SOCK_STREAM)
ServerPort = 12000
serverSocket.bind(('',ServerPort))                                      # 将TCP欢迎套接字绑定到指定端口
serverSocket.listen(1)                                                  # 最大连接数为1
while True:
    running()


