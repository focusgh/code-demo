#!/usr/bin/env python
# coding: utf-8
# __author__ = 'wang tao'

import time
import gevent
from gevent import monkey
monkey.patch_all()


def eat(name):
    print(f"{name} eat 1.")
    time.sleep(1)
    print(f"{name} eat 2.")


def play(name):
    print(f"{name} play 1.")
    time.sleep(2)
    print(f"{name} play 2.")


if __name__ == "__main__":
    g1 = gevent.spawn(eat, "wt")
    g2 = gevent.spawn(play, "wm")

    # g1.join()
    # g2.join()
    gevent.joinall([g1, g2])