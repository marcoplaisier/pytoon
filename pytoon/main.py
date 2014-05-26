#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pytoon.connection import BrickConnection


class PyToon(object):
    def main(self):
        host = "192.168.178.35"
        port = 4223
        connection = BrickConnection(host, port)

if __name__ == '__main__':
    sys.exit(PyToon().main())