# -*- coding: utf-8 -*-
"""
Created on Mon Jun 02 20:17:20 2014

@author: assa
"""

import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5500")
socket.setsockopt(zmq.SUBSCRIBE,"")

while True:
    msg =  socket.recv()
    print msg