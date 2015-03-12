# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 15:00:36 2015

@author: assa
"""

import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5501")
socket.setsockopt(zmq.SUBSCRIBE,"")

while True:
    row = socket.recv_pyobj()
    print row['Time'], row['ShortCD'], row['Ask1'], row['Bid1']

