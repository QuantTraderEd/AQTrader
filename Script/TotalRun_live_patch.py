# -*- coding: utf-8 -*-

import os
import sys
import ctypes
import time
import logging
import datetime as dt
import psutil
from subprocess import call
import redis
import pywinauto  # 0.6.3
import win32api, win32con
import win32gui, win32process

from commutil.holiday_util import HoliDayUtil

logger = logging.getLogger('TotalRun')
logger.setLevel(logging.DEBUG)
logger.propagate = False

# create file handler which logs even debug messages
fh = logging.FileHandler('TotalRun.log')
# fh = logging.Handlers.RotatingFileHandler('TotalRun.log', maxBytes=104857, backupCount=3)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to logger
logger.addHandler(fh)
logger.addHandler(ch)

close_notice_pos_x = 1340
close_notice_pos_y = 150

feeder_toggle_pos_x = 900
feeder_toggle_pos_y = 820
feeder_close_pos_x = 1220
feeder_close_pos_y = 800
oms_toggle_pos_x = 900
oms_toggle_pos_y = 620
oms_close_pos_x = 1200
oms_close_pos_y = 590

optionviewer_front_start_pos_x = 40
optionviewer_front_start_pos_y = 750
optionviewer_front_close_pos_x = 860
optionviewer_front_close_pos_y = 710

optionviewer_back_start_pos_x = 40
optionviewer_back_start_pos_y = 460
optionviewer_back_close_pos_x = 860
optionviewer_back_close_pos_y = 415

dbloader_start_stop_pos_x = 1342
dbloader_start_stop_pos_y = 815
dbloader_close_pos_x = 1660
dbloader_close_pos_y = 680

autootmtrader_start_stop_pos_x = 1442
autootmtrader_start_stop_pos_y = 630
autootmtrader_close_pos_x = 1675
autootmtrader_close_pos_y = 425

holiday_util = HoliDayUtil()
holiday_lst = holiday_util.read_holiday_data()

restart_option = False
time_sleep_interval = 10
pjt_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_window_title_pid(title):
    hwnd = win32gui.FindWindow(None, title)
    threadid, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid


def close_window_title(title):
    hwnd = win32gui.FindWindow(None, title)
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    pass


def close_notice_window():
    # title = u'\uacf5\uc9c0\uc0ac\ud56d'
    title_name = u'공지사항'
    pwa_app = pywinauto.application.Application()
    try:
        app = pwa_app.connect(title=title_name, class_name='Afx:00400000:0')
    except pywinauto.ElementNotFoundError as pye:
        logger.info("not found notice window: %s" % pye)
    else:
        afx = app[title_name]
        afx.close()
    pass


def get_process_list():
    prcslst = []

    for proc in psutil.process_iter():
        psinfo = proc.as_dict(attrs=['name'])
        if psinfo['name']: prcslst.append(psinfo['name'])

    return prcslst


def click(x, y):
    # win32api.SetCursorPos((x, y))
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    pass


def cp_start(input_text=''):
    logger.info('start cybos....')
    prcs_lst = get_process_list()
    if ('CpStart.exe' in prcs_lst) or ('DibServer.exe' in prcs_lst):
        logger.info('already run cybos...')
        return True

    app = pywinauto.application.Application()
    app.start('C:/DAISHIN/starter/ncStarter.exe /prj:cp')

    count = 0
    while (1):
        time.sleep(20)
        # window = app.ncStarter
        w_handle_lst = pywinauto.findwindows.find_windows(title=u'CYBOS Starter', class_name='#32770')
        if len(w_handle_lst) == 0 and count <= 3:
            logger.info('there is no handle of cybos')
            count += 1
        elif len(w_handle_lst) > 0:
            w_handle = w_handle_lst[0]
            break
        elif count > 3:
            logger.error('there is no handle of cybos')
            return False

    window = app.window(handle=w_handle)
    window.set_focus()

    time.sleep(5)

    logger.info('get cybos window handler')

    # ctrl = window[u'PLUSButton']
    # ctrl.click()

    ctrl = window[u'ONECLIKEdit2']
    ctrl.draw_outline()
    ctrl.click()
    ctrl.set_edit_text(input_text)

    ctrl = window[u'Button']
    ctrl.draw_outline()
    time.sleep(3)
    ctrl.set_focus()
    ctrl.click()
    time.sleep(30)

    return True
    pass


def cp_kill():

    for proc in psutil.process_iter():
        if proc.name() in ["pythonw.exe"]:
            logger.info('proc name: %s' % proc.name())
            os.system('TASKKILL /f /im pythonw.exe')
        elif proc.name() in ["DibServer.exe"]:
            psinfo = proc.as_dict(attrs=['name'])
            logger.info("pid:%d %s" % (proc.pid, psinfo['name']))
            logger.info('kill pid: %s proc name: %s' % (proc.name(), proc.pid))
            ret = os.system('TASKKILL /f /im %s' % proc.name())
            logger.info("ret-> %d" % ret)
        elif proc.name() in ["CpStart.exe"]:
            psinfo = proc.as_dict(attrs=['name'])
            logger.info("pid:%d %s" % (proc.pid, psinfo['name']))
            logger.info('kill pid: %s proc name: %s' % (proc.name(), proc.pid))
            taskkillexe = "c:/windows/system32/taskkill.exe"
            taskkillparam = (taskkillexe, '/F', '/IM', proc.name())
            ret = call(taskkillparam)
            logger.info("ret-> %d" % ret)

    pass


def show_task_list():
    for proc in psutil.process_iter():
        if proc.name() in ["python.exe"]:
            logger.info("pid:%d %s" % (proc.pid, proc.name()))
            output = psutil.Process(proc.pid).cmdline()
            logger.info("scrpt: %s" % output[1])


def oms_starter():
    os.chdir(pjt_path + '/OrderManager')
    if not os.path.exists('./orderlist_db/'):
        os.makedirs('./orderlist_db/')
    os.startfile('zerooms_main.py')
    logger.info('start OMS')


def dataloader_starter():
    os.chdir(pjt_path + '/DataLoader/dataloader')
    if not os.path.exists('./TAQ_Data/'):
        os.makedirs('./TAQ_Data/')
    os.startfile('dataloader_main.py')
    logger.info('start DataLoader')


def day_session_starter():
    logger.info('start day session...')

    os.chdir(pjt_path + '/CommUtil/commutil')
    os.startfile('OptionCode.py')
    logger.info('start optioncode.py')

    time.sleep(3)
    os.chdir(pjt_path + '/DataFeeder')
    os.startfile('ZeroFeederMainForm.pyw')
    logger.info('start DataFeeder')

    # time.sleep(5)
    # os.chdir(pjt_path + '\\ZeroTrader\\ZeroOptionViewer\\')
    # os.startfile('zerooptionviewer_main.py')
    # logger.info('start ZeroOptionViewer front month')

    # time.sleep(5)
    # os.chdir(pjt_path + '\\ZeroTrader\\ZeroOptionViewer_BackMonth\\')
    # os.startfile('zerooptionviewer_main.py')
    # logger.info('start ZeroOptionViewer back month')

    time.sleep(5)
    oms_starter()

    time.sleep(5)
    dataloader_starter()
    pass


def auto_test_trader_starter():
    time.sleep(5)
    os.chdir(pjt_path)
    os.chdir('../AutoFutArbTrader/')
    os.startfile('AutoFutArbTrader.py')
    logger.info('start AutoFutArbTrader')
    pass


def click_utck3_sync_button():
    logger.info('click utck3 sync button')
    for i in xrange(10):
        click(1640, 940)  # click at clock
        time.sleep(0.5)
    pass


def clear_ordno_dict():
    try:
        redis_client = redis.Redis()
        ordno_dict = redis_client.hgetall('ordno_dict')
        redis_client.delete('ordno_dict')
        logger.info(str(ordno_dict))
        logger.info('clear ordno_dict')
    except BaseException as e:
        logger.error('Fail to clear ordno_dict: ' + str(e))
        return
    pass


def make_miniarb_research_report():
    time.sleep(3)
    os.chdir(pjt_path + '/Script')
    if not os.path.exists('./miniarb_research/'):
        os.makedirs('./miniarb_research/')
    os.startfile('run_miniarb_research_report.py')
    logger.info('run miniarb_research_report')
    pass


def main():
    global time_sleep_interval
    logger.info('init TotalRun')

    prcslst = get_process_list()

    if not ("redis-server.exe" in prcslst):
        os.chdir('C:/Redis-x64-2.8.2103')
        # os.startfile('redis-server.exe redis.conf')
        redis_exe = "C:/Redis-x64-2.8.2103/redis-server.exe"
        redis_opt = "redis.conf"
        ctypes.windll.shell32.ShellExecuteA(0, 'open', redis_exe, redis_opt, None, 1)
        logger.info('start redis-server...')
    else:
        logger.info('redis-server ok')

    if not ("UTCk3.exe" in prcslst):
        logger.info('start clock...')
        target_path = 'C:\\Program Files (x86)\\KRISS\\UTCk3.0'
        if not os.path.exists(target_path):
            target_path = 'C:\\Program Files (x86)\\KRISS\\UTCk3.1'
        app = pywinauto.application.Application()
        app = app.start(target_path + '\\utck3.exe')
    else:
        logger.info('UTCK3 ok')

    # if not ("TeamViewer.exe" in prcslst):
    #     logger.info('start team veiwer...')
    #     app = pywinauto.application.Application()
    #     app.start('C:\\Program Files (x86)\\TeamViewer\\TeamViewer.exe')
    # else:
    #     logger.info('TeamViewer ok')

    if restart_option:
        logger.info('start restart...')

        if not ("DibServer.exe" in prcslst):
            is_logon_to_cp = cp_start()
            if not is_logon_to_cp:
                sys.exit()
            time.sleep(10)
            logger.info('close notice')
            # click(close_notice_pos_x, close_notice_pos_y)
            close_notice_window()

        prcslst = get_process_list()
        if "DibServer.exe" in prcslst:
            day_session_starter()

        logger.info('end restart')

    else:
        logger.info('wait session trigger..')

    day_session_trigger = False
    night_session_trigger = False
    night_session_close_trigger = True
    report_trigger = False

    nowtime = time.localtime()
    if nowtime.tm_hour >= 18 or nowtime.tm_hour <= 5:
        day_session_trigger = False
        night_session_trigger = True
        night_session_close_trigger = False

    test_open_trigger = True
    test_close_trigger = False

    logger.info('day_session_trigger: ' + str(day_session_trigger))
    logger.info('night_session_trigger: ' + str(night_session_trigger))
    logger.info('night_session_close_trigger: ' + str(night_session_close_trigger))

    nowdatetime = dt.datetime.now()
    if nowdatetime.weekday() >= 5:
        logger.info('Stop@WeekEnd')
        time_sleep_interval = 60 * 5
    elif nowdatetime.strftime('%Y%m%d') in holiday_lst:
        logger.info('Stop@Holiday')
        time_sleep_interval = 60 * 5
    else:
        time_sleep_interval = 30

    logger.info('Run TotalRun Loop')
    logger.info('time_sleep_interval-> %d' % time_sleep_interval)

    while True:
        time.sleep(time_sleep_interval)
        nowtime = time.localtime()
        nowdatetime = dt.datetime.now()

        # if nowtime.tm_hour == 13 and 0 <= nowtime.tm_min <= 58 and test_open_trigger:
        # if (nowtime.tm_hour in [7,] and nowtime.tm_min >= 15 and nowtime.tm_min <= 59 and not day_session_trigger) or \
        if nowtime.tm_hour in [8, ] and nowtime.tm_min >= 0 and nowtime.tm_min <= 10 and not day_session_trigger:
            if nowdatetime.weekday() >= 5:
                logger.info('Stop@WeekEnd')
                time_sleep_interval = 60 * 5
                continue
            elif nowdatetime.strftime('%Y%m%d') in holiday_lst:
                logger.info('Stop@Holiday')
                time_sleep_interval = 60 * 5
                continue
            else:
                time_sleep_interval = 30

            logger.info('time_sleep_interval-> %d' % time_sleep_interval)

            day_session_starter()
            auto_test_trader_starter()

            day_session_trigger = True
            night_session_trigger = False

            test_open_trigger = False
            test_close_trigger = True

        elif nowtime.tm_hour == 17 and nowtime.tm_min >= 0 and nowtime.tm_min <= 35 and \
                not night_session_trigger and day_session_trigger:

            clear_ordno_dict()
            logger.info('End_day_session_trigger')
            day_session_trigger = False
            night_session_trigger = False

        elif nowtime.tm_hour == 17 and nowtime.tm_min >= 40 and nowtime.tm_min <= 55 and not night_session_trigger:
            nowdatetime = dt.datetime.now()
            if nowdatetime.weekday() >= 5:
                logger.info('Pass@WeekEnd')
                continue
            elif nowdatetime.strftime('%Y%m%d') in holiday_lst:
                logger.info('Pass@Holiday')
                continue

            time.sleep(5)
            dataloader_starter()

            day_session_trigger = False
            night_session_trigger = True
            night_session_close_trigger = False
            report_trigger = False

        elif nowtime.tm_hour == 18 and nowtime.tm_min == 45 and not report_trigger:
            if nowdatetime.weekday() >= 5:
                logger.info('Pass@WeekEnd')
                continue
            elif nowdatetime.strftime('%Y%m%d') in holiday_lst:
                logger.info('Pass@Holiday')
                continue
            make_miniarb_research_report()
            report_trigger = True

        # elif nowtime.tm_hour == 23 and nowtime.tm_min >= 0:
        elif nowtime.tm_hour == 6 and nowtime.tm_min >= 15 and not night_session_close_trigger:

            cp_kill()
            clear_ordno_dict()

            night_session_close_trigger = True
            day_session_trigger = False

            # test_close_trigger = False
            # test_open_trigger = False
            # print 'test done'


if __name__ == "__main__":
    main()
