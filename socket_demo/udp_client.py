#!/usr/bin/env python
# coding: utf-8
# __author__ = 'wang tao'

from socket import (
    socket,
    AF_INET,
    SOCK_DGRAM
)


class UDPClient:

    DEFAULT_IP_PORT = ("127.0.0.1", 8888)
    DEFAULT_BUF_SIZE = 10

    def __init__(self, ip_port=None, buf_size=None):
        self._ip_port = self.DEFAULT_IP_PORT
        self._buf_size = self.DEFAULT_BUF_SIZE

        if ip_port:
            self._ip_port = ip_port
        if buf_size:
            self._buf_size = buf_size

        self._socket_client = socket(AF_INET, SOCK_DGRAM)

    def run(self):

        while True:
            input_str = input(">>: ").strip()
            if not input_str:
                continue
            if input_str == "q" or input_str == "quit":
                break

            self._socket_client.sendto(input_str.encode("utf-8"), self._ip_port)
            data, addr = self._socket_client.recvfrom(self._buf_size)
            print(data.decode("utf-8"), addr)

        self.close()

    def close(self):
        self._socket_client.close()


if __name__ == "__main__":
    tcp_client = UDPClient()
    tcp_client.run()
