#!/usr/bin/env python
# coding: utf-8
# __author__ = 'wang tao'

from socket import (
    socket,
    AF_INET,
    SOCK_DGRAM,
    SOL_SOCKET,
    SO_REUSEADDR
)


class UDPServer:

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

        self._socket_server = socket(AF_INET, SOCK_DGRAM)

    def run(self):
        self._socket_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._socket_server.bind(self._ip_port)

        while True:
            # 接收的 size 一定要比发送的 size 大，否则会出现丢包现象
            data, addr = self._socket_server.recvfrom(self._buf_size)
            print(data.decode("utf-8"), addr)
            self._socket_server.sendto(data.upper(), addr)

        self._sk_close()

    def _sk_close(self):
        self._socket_server.close()


if __name__ == "__main__":
    tcp_server = UDPServer()
    tcp_server.run()