from socket import *
from select import *

HOST = '0.0.0.0'
PORT = 8988
ADDR = (HOST, PORT)

tcp_socket = socket()
tcp_socket.bind(ADDR)
tcp_socket.listen(5)

tcp_socket.setblocking(False)

p = epoll()
p.register(tcp_socket, EPOLLIN)

map = {
    tcp_socket.fileno(): tcp_socket,
}

while True:
    events = p.poll()  # !!! 不是p.epoll !!!
    for fd, event in events:
        if fd == tcp_socket.fileno():
            connfd, addr = map[fd].accept()
            print('Connect from', addr)
            connfd.setblocking(False)
            p.register(connfd, EPOLLIN)
            map[connfd.fileno()] = connfd
        elif event == EPOLLIN:
            data = map[fd].recv(1024).decode()
            if not data:
                p.unregister(map[fd])  # p.unregister(fd)
                map[fd].close()
                del map[fd]
                continue
            print(data)
            map[fd].send(b'OK')
