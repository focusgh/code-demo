#!/usr/bin/env python
# coding: utf-8
# __author__ = 'wang tao'

from threading import (
    Thread,
    current_thread,
)
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM
)


class TCPClient:

    DEFAULT_IP_PORT = ("127.0.0.1", 8888)
    DEFAULT_BUF_SIZE = 1024

    def __init__(self, ip_port=None, buf_size=None):
        self._ip_port = self.DEFAULT_IP_PORT
        self._buf_size = self.DEFAULT_BUF_SIZE

        if ip_port:
            self._ip_port = ip_port
        if buf_size:
            self._buf_size = buf_size

        self._socket_client = socket(AF_INET, SOCK_STREAM)

    def run(self):

        conn_res = self._socket_client.connect_ex(self._ip_port)

        while True:

            self._socket_client.send("{} hello".format(current_thread().getName()).encode("utf-8"))
            data = self._socket_client.recv(self._buf_size)
            print(data.decode("utf-8"))

        self.close()

    def close(self):
        self._socket_client.close()


if __name__ == "__main__":
    tcp_client = TCPClient()

    for i in range(100):
        t = Thread(target=tcp_client.run)
        t.start()
