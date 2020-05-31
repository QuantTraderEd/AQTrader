# -*- coding: utf-8 -*-

import sys
import logging
import pythoncom
import redis
import pprint
import datetime as dt

import pyxing as px
from commutil.comm_function import read_config
from OrderManager.zeropositionviewer.zeropositionviewer import Observer_t0441, Observer_CEXAQ31200

logger = logging.getLogger('PositionUpdater')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('PositionUpdater.log')
# fh = logging.Handlers.RotatingFileHandler('PositionUpdater.log', maxBytes=104857, backupCount=0)
fh.setLevel(logging.INFO)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s '
                              '%(filename)s %(funcName)s() %(lineno)d:\t\t'
                              '%(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to logger
logger.addHandler(fh)
logger.addHandler(ch)


def set_auto_config():
    comm_config = read_config()
    auto_config = dict()
    auto_config['id'] = comm_config.get('ebest_id', '')
    auto_config['pwd'] = comm_config.get('ebest_pw', '')
    auto_config['cetpwd'] = comm_config.get('ebest_cetpwd', '')
    auto_config['servertype'] = comm_config.get('ebest_servertype', 1)

    print(auto_config)
    return auto_config


def auto_start_xing(xasession, auto_config):
    server = 'hts.ebestsec.co.kr'
    port = 20001
    servertype = 0
    showcerterror = 1
    user = str(auto_config['id'])
    password = str(auto_config['pwd'].decode('hex'))
    certpw = str(auto_config['cetpwd'].decode('hex'))
    servertype = int(auto_config['servertype'])
    if servertype == 1:
        server = 'demo.ebestsec.co.kr'
    elif servertype == 0:
        server = 'hts.ebestsec.co.kr'

    xasession.ConnectServer(server, port)
    # print 'connect server'
    ret = xasession.Login(user, password, certpw, servertype, showcerterror)

    px.XASessionEvents.session = xasession
    xasession.flag = True
    while xasession.flag:
        pythoncom.PumpWaitingMessages()
    pass


def send_query(accountlist):
    nowtime = dt.datetime.now()
    if nowtime.hour >= 7 and nowtime.hour < 17:
        exchange_code = 'KRX'
        xquery = px.XAQuery_t0441()
        obs_t0441 = Observer_t0441()
        xquery.observer = obs_t0441
        xquery.SetFieldData('t0441InBlock', 'accno', 0, accountlist[1])
        xquery.SetFieldData('t0441InBlock', 'passwd', 0, '0000')
    else:
        exchange_code = 'EUREX'
        xquery = px.XAQuery_CEXAQ31200()
        obs_cexaq31200 = Observer_CEXAQ31200()
        xquery.observer = obs_cexaq31200
        xquery.SetFieldData('CEXAQ31200InBlock1', 'RecCnt', 0, 1)
        xquery.SetFieldData('CEXAQ31200InBlock1', 'AcntNo', 0, accountlist[1])
        xquery.SetFieldData('CEXAQ31200InBlock1', 'InptPwd', 0, '0000')
        xquery.SetFieldData('CEXAQ31200InBlock1', 'BalEvalTp', 0, '1')
        xquery.SetFieldData('CEXAQ31200InBlock1', 'FutsPrcEvalTp', 0, '1')

    xquery.flag = True
    ret = xquery.Request(False)
    while xquery.flag:
        pythoncom.PumpWaitingMessages()

    data = xquery.data
    position_dict = dict()
    tradeprice_dict = dict()

    if exchange_code == 'KRX':
        for i in range(1, len(data)):
            shortcd = data[i]['expcode']
            if data[i]['medocd'] == '1':
                pos = -1 * int(data[i]['jqty'])
            elif data[i]['medocd'] == '2':
                pos = int(data[i]['jqty'])
            else:
                pos = 0

            avgprc = '%.5f' % float(data[i]['pamt'])
            lastprc = '%.2f' % float(data[i]['price'])

            position_dict[shortcd] = pos
            tradeprice_dict[shortcd] = avgprc
    elif exchange_code == 'EUREX':
        for i in range(2, len(data)):
            shortcd = data[i]['FnoIsuNo']
            if data[i]['BnsTpCode'] == '1':
                pos = -1 * int(data[i]['UnsttQty'])
            elif data[i]['BnsTpCode'] == '2':
                pos = int(data[i]['UnsttQty'])
            else:
                pos = 0

            avgprc = '%.5f' % float(data[i]['FnoAvrPrc'])
            lastprc = '%.2f' % float(data[i]['NowPrc'])

            position_dict[shortcd] = pos
            tradeprice_dict[shortcd] = avgprc

    return position_dict, tradeprice_dict


def main():
    auto_config = set_auto_config()
    xasession = px.XASession()
    auto_start_xing(xasession, auto_config)

    if xasession.IsConnected() and xasession.GetAccountListCount():
        accountlist = xasession.GetAccountList()
        servername = xasession.GetServerName()
        logger.info("%s" % accountlist)
        logger.info("%s" % servername)
    else:
        sys.exit()

    position_dict, tradeprice_dict = send_query(accountlist)
    logger.info("%s" % pprint.pformat(position_dict))
    logger.info("%s" % pprint.pformat(tradeprice_dict))

    autotrader_id = "MiniArb001"
    redis_client = redis.Redis(port=6479)

    logger.info("==================OLD====================")
    logger.info("%s" % pprint.pformat(redis_client.hgetall(autotrader_id + "_position_dict")))
    logger.info("%s" % pprint.pformat(redis_client.hgetall(autotrader_id + "_tradeprice_dict")))

    redis_client.delete(autotrader_id + "_position_dict")
    redis_client.delete(autotrader_id + "_tradeprice_dict")
    if len(position_dict) > 0:
        redis_client.hmset(autotrader_id + "_position_dict", position_dict)
        redis_client.hmset(autotrader_id + "_tradeprice_dict", tradeprice_dict)

    redis_client.save()

    msg1 = "%s" % pprint.pformat(redis_client.hgetall(autotrader_id + "_position_dict"))
    msg2 = "%s" % pprint.pformat(redis_client.hgetall(autotrader_id + "_tradeprice_dict"))
    logger.info("==================NEW====================")
    logger.info(msg1)
    logger.info(msg2)

    return msg1, msg2


if __name__ == '__main__':
    main()

