# -*- coding: utf-8 -*-

import logging
from DataLoader.dataloader.SubscribeReceiverThread import SubscribeThread


class RecvThread(SubscribeThread):
    def __init__(self, parent=None, port=5503):
        SubscribeThread.__init__(self, parent, port)

    def onReceiveData(self, msg_dict):
        print("recv data: %s" % msg_dict)


def main():
    sub_thread = RecvThread(port=5510)
    sub_thread.run()


if __name__ == "__main__":
    main()
