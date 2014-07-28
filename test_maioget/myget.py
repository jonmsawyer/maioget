#!/usr/bin/env python
# coding: UTF-8

import os, sys
sys.path.insert(0, '/home/thales/Projects')

import maioget

class MyGet(maioget.MaioGetBase):
    pass

if '__main__' == __name__:
    myget = MyGet(**maioget.parse_args())
    myget.command_line()
