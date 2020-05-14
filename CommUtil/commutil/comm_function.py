# -*- coding: utf-8 -*-

import os
import json

pjt_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def convert_price_to_str(strprice):
    return '%.3f' % round(float(strprice), 2)


def read_config():
    comm_config_dict = dict()
    filename = pjt_path + '/Script/.config'
    with open(filename, 'r') as f:
        comm_config_dict = json.load(f)
    return comm_config_dict


if __name__ == "__main__":
    comm_config_dict = read_config()
    print(comm_config_dict)
