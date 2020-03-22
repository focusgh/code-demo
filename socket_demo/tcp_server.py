#!/usr/bin/env python
# coding: utf-8
# __author__ = 'wang tao'

import json
import struct
import subprocess
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)


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
        self._tcp_socket_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._tcp_socket_server.bind(self._ip_port)
        self._tcp_socket_server.listen(5)

        while True:
            conn, addr = self._tcp_socket_server.accept()
            print(f"client addr: {addr}")

            while True:
                cmd = conn.recv(self._buf_size)
                print(f"client cmd: {cmd}")
                if not cmd:
                    break

                res = subprocess.Popen(cmd.decode("utf-8"), shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
                stdout = res.stdout.read()
                stderr = res.stderr.read()

                # 1. 制作报头
                header_dict = self._header_dict
                header_dict["stdout_size"] = len(stdout)
                header_dict["stderr_size"] = len(stderr)
                header_dict["sequence"] = ["stdout_size", "stderr_size"]

                # 2. 发送 4 个 bytes 大小的报头长度
                header_str = json.dumps(header_dict)
                header_size = struct.pack("i", len(header_str))
                conn.send(header_size)

                # 3. 发送报头
                conn.send(header_str.encode("utf-8"))

                # 4. 发送真实数据
                conn.send(stdout)
                conn.send(stderr)

            conn.close()

        self._sk_close()

    def _sk_close(self):
        self._tcp_socket_server.close()


if __name__ == "__main__":
    tcp_server = TCPServer()
    tcp_server.run()