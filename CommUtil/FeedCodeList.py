# -*- coding: utf-8 -*-
from os import path


class FeedCodeList:
    """
    feed code list from read file
    """
    def __init__(self):
        self.future_shortcd_list = []
        self.option_shortcd_list = []
        self.equity_shortcd_list = []
        self.index_shortcd_list = []

    def read_code_list(self):
        state = 0
        filename = path.join(path.dirname(__file__), 'feedcodelist.txt')
        feedcodelistfilep = open(filename, 'r')

        # FeedCodeFile Parseing        
        
        while 1:
            line = feedcodelistfilep.readline()
            if not line: break
            if line[:-1] == "<Futures/>": state = 1
            elif line[:-1] == "<Options/>": state = 2    
            elif line[:-1] == "<Equity/>": state = 3
            elif line[:-1] == "<Index/>": state = 4
            
            if state == 1 and line[0] != "<":
                self.future_shortcd_list.append(line[:-1])
            elif state == 2 and line[0] != "<":
                self.option_shortcd_list.append(line[:-1])
            elif state == 3 and line[0] != "<":
                self.equity_shortcd_list.append(line[:-1])
            elif state == 4 and line[0] != "<":
                self.index_shortcd_list.append(line[:-1])

        feedcodelistfilep.close()
        pass


if __name__ == "__main__":

    _feedcodelist = FeedCodeList()
    _feedcodelist.read_code_list()
    
    print _feedcodelist.future_shortcd_list
    print _feedcodelist.option_shortcd_list
    print _feedcodelist.equity_shortcd_list
    print _feedcodelist.index_shortcd_list
