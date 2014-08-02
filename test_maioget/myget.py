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
    def __init__(self, *args, **kwargs):
        super(MyGet, self).__init__(*args, **kwargs)
        self.logger_kwargs = {
            'directory': os.path.join('..', 'logs'),
            'name': 'maioget.MyGet',
            'daemon': kwargs.get('daemon', False),
            'loglevel': kwargs.get('loglevel', 'INFO'),
        }
        self.set_logger(maioget.logger.setup(**self.logger_kwargs))

if '__main__' == __name__:
    myget = MyGet(**maioget.parse_args())
    myget.command_line()
