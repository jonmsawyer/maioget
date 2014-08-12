#!/usr/bin/env python
# coding: UTF-8

import os, sys
# Put ./../../ in the python path
sys.path.insert(0, os.path.dirname(
                     os.path.dirname(
                       os.path.dirname(
                         os.path.realpath(__file__)
                   )))
               )
import maioget

class MyGet(maioget.MaioGetBase):
    pass

if '__main__' == __name__:
    maioargs = maioget.parse_args()
    if maioargs.get('name') == 'UNNAMED':
        maioargs['name'] = 'MyGet'
    myget = MyGet(**maioargs)
    myget.command_line()
