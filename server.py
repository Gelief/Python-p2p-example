#!/usr/bin/env python3
# coding=utf-8

import socket
import queue
import threading
import time


class Server(object):
    """
    服务器类
    """

    def __init__(self, address, port=1111):
        '''

        :param port: 端口
        '''
        self.__address = address
        self.__buffer_size = 1024

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        # 检测对方是否崩溃
        self.server.setblocking(0)

        # 端口释放 端口复用
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server.bind((self.__address, port))
        self.server.listen(5)
        print('等待连接...')

        # id : socket 字典
        self.sockets_dict = {}

        # socket : id 字典
        self.id_dict = {}

        # aim_id : message_queue 目标id对应其应当接收的消息
        self.message_queues = {}

    def get_ids_msg(self, data, split_string):
        print(data)
        string = data.split(split_string)
        print(string)
        src_id = string[0]
        aim_id = string[1]
        msg = string[2]
        return src_id, aim_id, msg

    def link(self, sock, addr):
        # 连接之初先发送索引给服务端
        # 阻塞等待接收消息
        while True:
            try:
                sock_id = sock.recv(self.__buffer_size).decode()
            except:
                continue
            else:
                print(sock_id)
                break
        self.sockets_dict[sock_id] = sock
        self.id_dict[sock] = sock_id

        while True:
            time.sleep(0.1)

            try:
                data = sock.recv(self.__buffer_size).decode()
                print("接受的数据是", data)
            except:
                continue
            else:
                print(data)
                src_id, aim_id, msg = self.get_ids_msg(data, "&")

                if not self.sockets_dict[aim_id]:
                    # 如果目的客户端没有连接
                    print("没有%s客户端" % aim_id)
                    continue
                else:
                    aim_sock = self.sockets_dict[aim_id]
                    aim_sock.send(str(msg).encode())


    def test_run(self):
        print("服务端监听")
        while True:
            try:
                conn, address = self.server.accept()
            except:
                continue
            th = threading.Thread(target=self.link, args=(conn, address))
            th.start()


if __name__ == '__main__':
    address = '127.0.0.1'
    port = 1111
    ser = Server(address, port)
    ser.test_run()

