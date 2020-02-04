# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .models import Positions

import redis

redis_client = redis.Redis(port=6479)


def index(request):
    position_dict = redis_client.hgetall('MiniArb001_position_dict')
    tradeprice_dict = redis_client.hgetall('MiniArb001_tradeprice_dict')
    print("#######################################")
    print('position: ', str(position_dict))
    print('tradeprice: ', str(tradeprice_dict))
    # Positions.full_clean()
    for key in position_dict:
        positions = Positions.objects.filter(shortcd=key)
        mid_price = (float(redis_client.hget('bid1_dict', key)) + float(redis_client.hget('ask1_dict', key))) * 0.5
        qty = int(position_dict[key])
        tradeprice = float(tradeprice_dict.get(key, 0.0))
        pnl_open = (mid_price - tradeprice) * qty
        if key[:3] in ['105']:
            pnl_open = pnl_open * 0.2
        print('mid: ', key, mid_price)
        if len(positions) == 0:
            position = Positions()
            position.shortcd = key
            position.qty = qty
            position.tradeprice = tradeprice
            position.mark = mid_price
            position.pnl_open = pnl_open
            position.save()
        else:
            position = positions[0]
            position.qty = qty
            position.tradeprice = tradeprice
            position.mark = mid_price
            position.pnl_open = pnl_open
            position.save()

    positions = Positions.objects.all()
    context = {'positions': positions}
    return render(request, 'aqtrader/index.html', context)
