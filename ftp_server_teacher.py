"""
ftp 文件服务 服务端
多线程并发模型训练
"""

from socket import *
from threading import Thread
import os, time

# 全局变量
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)  # 服务器地址

# 文件库
FTP = "/home/tarena/FTP/"


# 处理客户端请求
class FTPServer(Thread):
    def __init__(self, connfd):
        super().__init__()
        self.connfd = connfd

    def do_list(self):
        # 判断文件库是否为空
        file_list = os.listdir(FTP)
        if not file_list:
            self.connfd.send(b'FAIL')  # 列表为空
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)
            data = "\n".join(file_list)
            self.connfd.send(data.encode())

    # 处理下载
    def do_get(self, filename):
        try:
            f = open(FTP + filename, 'rb')
        except:
            # 文件不存在报异常
            self.connfd.send(b"FAIL")
            return
        else:
            # 文件打开成功
            self.connfd.send(b"OK")
            time.sleep(0.1)
            # 发送文件
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.connfd.send(b"##")  # 文件发送完毕
                    break
                self.connfd.send(data)
            f.close()

    # 处理上传
    def do_put(self, filename):
        if os.path.exists(FTP + filename):
            self.connfd.send(b"FAIL")
            return
        else:
            self.connfd.send(b"OK")
            # 接收文件
            f = open(FTP + filename, 'wb')
            while True:
                data = self.connfd.recv(1024)
                if data == b"##":
                    break
                f.write(data)
            f.close()

    # 作为一个线程内容处理某一个客户端的请求
    def run(self):
        # 总分模式
        while True:
            # 某个客户端所有的请求
            data = self.connfd.recv(1024).decode()
            print("Request:", data)  # 调试
            # 更具不同的请求做不同处理
            if not data or data == 'EXIT':
                self.connfd.close()
                return
            elif data == 'LIST':
                self.do_list()
            elif data[:4] == 'RETR':
                filename = data.split(' ')[-1]
                self.do_get(filename)
            elif data[:4] == 'STOR':
                filename = data.split(' ')[-1]
                self.do_put(filename)


def main():
    # tcp套接字创建
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)
    print("Listen the port %s" % PORT)

    # 循环连接客户端
    while True:
        try:
            connfd, addr = sock.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            sock.close()
            return
        # 为连接进来的客户端创建单独的线程
        t = FTPServer(connfd)  # 使用自定义线程类创建线程
        t.setDaemon(True)  # 主线程退出，分之线程终止服务
        t.start()


if __name__ == '__main__':
    main()
