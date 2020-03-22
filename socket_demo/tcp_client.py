#!/usr/bin/env python
# coding: utf-8
# __author__ = 'wang tao'

import json
import struct
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM
)


class TCPClient:

    DEFAULT_IP_PORT = ("127.0.0.1", 8888)
    DEFAULT_BUF_SIZE = 10

    def __init__(self, ip_port=None, buf_size=None):
        self._ip_port = self.DEFAULT_IP_PORT
        self._buf_size = self.DEFAULT_BUF_SIZE

        if ip_port:
            self._ip_port = ip_port
        if buf_size:
            self._buf_size = buf_size

        self._tcp_socket_client = socket(AF_INET, SOCK_STREAM)

    def run(self):

        conn_res = self._tcp_socket_client.connect_ex(self._ip_port)

        while True:
            input_str = input(">>: ").strip()
            if not input_str:
                continue
            if input_str == "q" or input_str == "quit":
                break

            self._tcp_socket_client.send(input_str.encode("utf-8"))

            # 1. 接收 4 个 bytes 的报头长度
            header_struct_bytes = self._tcp_socket_client.recv(4)
            header_size = struct.unpack("i", header_struct_bytes)[0]

            # 2. 接收报头
            header_str = self._tcp_socket_client.recv(header_size).decode("utf-8")
            header_dict = json.loads(header_str)

            # 3. 按报头协议，接收真实数据
            sequence = header_dict["sequence"]
            for seq in sequence:
                output_size = header_dict[seq]

                cmd_res = b""
                recv_size = 0
                while recv_size < output_size:
                    output = self._tcp_socket_client.recv(output_size)
                    cmd_res += output
                    recv_size += len(output)

                if cmd_res:
                    print("{}".format(cmd_res.decode("utf-8")))

        self.close()

    def close(self):
        self._tcp_socket_client.close()


if __name__ == "__main__":
    tcp_client = TCPClient()
    tcp_client.run()
