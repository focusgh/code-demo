#!/usr/bin/env python
# coding: utf-8
# __author__ = 'wang tao'

from threading import current_thread
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)
from gevent import (
    spawn,
    monkey,
)
monkey.patch_all()


class TCPServer:

    DEFAULT_IP_PORT = ("127.0.0.1", 8888)
    DEFAULT_BUF_SIZE = 1024
    DEFAULT_HEADER_DICT = {}

    def __init__(self, ip_port=None, buf_size=None, header_dict=None):
        self._ip_port = self.DEFAULT_IP_PORT
        self._buf_size = self.DEFAULT_BUF_SIZE
        self._header_dict = self.DEFAULT_HEADER_DICT

        if ip_port:
            self._ip_port = ip_port
        if buf_size:
            self._buf_size = buf_size
        if header_dict:
            self._header_dict = header_dict

        self._tcp_socket_server = socket(AF_INET, SOCK_STREAM)

    def run(self):
        print("main thread: {}".format(current_thread().getName()))
        self._tcp_socket_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._tcp_socket_server.bind(self._ip_port)
        self._tcp_socket_server.listen(5)

        while True:
            conn, addr = self._tcp_socket_server.accept()
            print(f"client addr: {addr}")

            self.communicate(conn)
            # spawn(communicate, conn)

        self._sk_close()

    def _sk_close(self):
        self._tcp_socket_server.close()

    def communicate(self, conn):
        print("child thread: {}".format(current_thread().getName()))
        while True:
            try:
                data = conn.recv(self._buf_size)
                print(f"client data: {data}")
                if not data:
                    break
                conn.send(data.upper())
            except Exception:
                break

        conn.close()


def communicate(conn):
    print("child thread: {}".format(current_thread().getName()))
    while True:
        try:
            data = conn.recv(1024)
            print(f"client data: {data}")
            if not data:
                break
            conn.send(data.upper())
        except ConnectionResetError:
            break

    conn.close()


if __name__ == "__main__":
    tcp_server = TCPServer()
    g = spawn(tcp_server.run)
    g.join()