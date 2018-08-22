# -*- coding: utf-8 -*-


class FeedCodeList():
    """
    feed code list from read file
    """
    def __init__(self):
        self.futureshortcdlst = []
        self.optionshortcdlst = []
        self.equityshortcdlst = []
        self.indexshortcdlst = []

    def ReadCodeListFile(self):
        try:
            feedcodelistfilep = open('feedcodelist.txt','r')
        except IOError, e:            
            print e
            print "There is no feedcodelist.txt file."
            return 
        state = 0
        
        # FeedCodeFile Parseing        
        
        while 1:
            line = feedcodelistfilep.readline()
            if not line: break
            if line[:-1] == "<Futures/>": state = 1
            elif line[:-1] == "<Options/>": state = 2    
            elif line[:-1] == "<Equity/>": state = 3
            elif line[:-1] == "<Index/>": state = 4
            
            if state == 1 and line[0] != "<":
                self.futureshortcdlst.append(line[:-1])
            elif state == 2 and line[0] != "<":
                self.optionshortcdlst.append(line[:-1])
            elif state == 3 and line[0] != "<":
                self.equityshortcdlst.append(line[:-1])
            elif state == 4 and line[0] != "<":
                self.indexshortcdlst.append(line[:-1])
            


if __name__ == "__main__":
    
    class ConsoleViewer:    
        def Update(self, subject):
            for i in xrange(len(subject.data)): 
                print subject.data[i]            
            pass        
            print '---------------------------'
        pass
        
    from pythoncom import PumpWaitingMessages
    import pycybos as pc
    
    viewer = ConsoleViewer()
    _feedcodelist = FeedCodeList()
    _feedcodelist.ReadCodeListFile()
    
    print _feedcodelist.futureshortcdlst
    print _feedcodelist.optionshortcdlst
    print _feedcodelist.equityshortcdlst
    print _feedcodelist.indexshortcdlst
    
#    futuresoptionTAQfeederlst = []
#    equityTAQfeederlst = []
#    
#    for shcode in _feedcodelist.futureshcodelst:
#        if shcode[-3:] == '000': 
#            newitem = pc.FutureCurOnly(shcode[:-3])
#            newitem.Attach(viewer)
#            newitem.Subscribe()
#            #futuresoptionTAQfeederlst.append(newitem)
#        else:
#            newitem = pc.OptionCurOnly(shcode)
#            newitem.Attach(viewer)
#            newitem.Subscribe()
#            #futuresoptionTAQfeederlst.append(newitem)
#            
#    for shcode in _feedcodelist.equityshcodelst:
#        newitem = pc.StockCur('A' + shcode)
#        newitem.Attach(viewer)
#        newitem.Subscribe()
#        equityTAQfeederlst.append(newitem)
#        
#    print futuresoptionTAQfeederlst
#    print equityTAQfeederlst
#        
#    while 1:
#        PumpWaitingMessages()
        
    