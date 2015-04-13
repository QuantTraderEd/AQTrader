# -*- coding: utf-8 -*-
"""
Created on Mon Apr 06 15:27:41 2015

@author: assa
"""


from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib import rcParams, style

class OptionViewerPlotDlg(QtGui.QWidget):
    def __init__(self, parent=None):
        super(OptionViewerPlotDlg, self).__init__(parent)
        
        self.setWindowTitle('Plot')
        self.resize(600,450)
        
        # a figure instance to plot on
        self.figure = plt.figure()
        
        # this is the Canvas Widget that displays the 'figure'
        # it takes the 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # Just some button connected to 'plot' method
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        
        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)
        
        style.use('ggplot')
        rcParams['font.size'] = 12
        
        # create an axis
        self.ax = self.figure.add_subplot(111)
        
        
    
    def plot(self,xdata=[],data=[]):
        """ 
        plot some random stuff 
        """
        # random data
#        x_data = [240 + i * 2.5 for i in range(9)]
#        data = [
#        0.002142,  
#        0.001950,  
#        0.001831, 
#        0.001727,  
#        0.001644,  
#        0.001581,  
#        0.001534,  
#        0.001517,  
#        0.001583         
#        ]
        
        # discards the old graph
        self.ax.hold(False)
        
        # plot data
        self.ax.plot(xdata,data, 'o-')
        
        #refresh canvas
        self.canvas.draw()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main = OptionViewerPlotDlg()
    main.show()
    
    sys.exit(app.exec_())
