#!/usr/bin/env python3
# coding=utf-8

import socket
import sys
import threading
import time


class Client(object):

    def __init__(self, identity, address, port):
        self.buffer_size = 1024
        self.identity = identity
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_socket.settimeout(2)

        # connect
        try:
            self.client_socket.connect((address, port))
            # 连接后必须发送该客户端的id建立索引
        except Exception as e:
            print("Unable to connect because %s" % e)
            sys.exit()
        else:
            self.client_socket.send(str(self.identity).encode())
            print(self.identity, "connected to server...")

    def send(self, des_id, msg):
        try:
            msg = self.identity + "&" + des_id + "&" + msg
            self.client_socket.send(str(msg).encode())
        except Exception as e:
            print("A不能发送信息，因为%s" % e)
            sys.exit()

    def receive(self):
        while True:
            time.sleep(0.1)
            try:
                data = self.client_socket.recv(self.buffer_size).decode()
            except:
                pass
            else:
                print(data)

    def test_run(self, aim_id, msg):
        print("开始测试")
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        send_thread = threading.Thread(target=self.send, args=(aim_id, msg))
        send_thread.start()
        send_thread.join()

