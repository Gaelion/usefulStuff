'''
--------------------------------------------------------

View code for TEMPLATE tool.
Code for maya, works on maya 2016,2017,2018

--------------------------------------------------------
'''


import os
import json
import maya.cmds as cmds

try:
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtUiTools as QtUiTools
    import PySide2.QtWidgets as QtWidgets
except:
    #print "fail to import PySide2, {}".format(__file__)
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtUiTools as QtUiTools
    import PySide.QtGui as QtWidgets


import loadui.loadUiType as loadUiType
import qtutils.utils as utils
import toolTemplate.model as templateModel
import toolTemplate.controller as templateController

     
'''
--------------------------------------------------------

TEMPLATE QWIDGET

--------------------------------------------------------
'''

class TemplateWidget(QtWidgets.QWidget):
    def __init__(self, mainwindow):
        super(TemplateWidget, self).__init__()
        self.mainwindow = mainwindow
        self.initui()
        self.populateUi()
        self.connectUi()
        self.setUi()

    def initui(self):
        uiFile = os.path.join(os.path.dirname(__file__), 'ui/TEMPLATE.ui')
        form_class, base_class = loadUiType(uiFile)
        self.mainUi = form_class()
        self.mainUi.setupUi(self)

    def populateUi(self):
        pass

    def connectUi(self):
        pass

    def setUi(self):
        pass

'''
--------------------------------------------------------
TEMPLATE WINDOW
--------------------------------------------------------
'''
class TemplateWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(TemplateWindow, self).__init__(parent)
        self.setObjectName("Template")
        self.setWindowTitle('Template '+os.getenv("REZ_Template_VERSION")) #If Rez context control available
        self.setWindowFlags(QtCore.Qt.Tool)
        self.templatewidget = TemplateWidget(self)
        self.setCentralWidget(self.templatewidget)
        self.settings = None
        self.readSettings()

    def closeEvent(self, *args, **kwargs):
        '''
		Overwriting close event to close child windows too
        '''
        print 'close event'
        self.writeSettings()

    def writeSettings(self):
        self.settings = QtCore.QSettings("departmentsettings", "template")
        self.settings.beginGroup("MainWindow")
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.endGroup()

    def readSettings(self):
        self.settings = QtCore.QSettings("departmentsettings", "template")
        self.settings.beginGroup("MainWindow")
        self.resize(self.settings.value("size", QtCore.QSize(400, 400)))
        self.move(self.settings.value("pos", QtCore.QPoint(200, 200)))
        self.settings.endGroup()


'''
--------------------------------------------------------
TEMPLATE LAUNCHER
--------------------------------------------------------
'''

def launch():	 
    mainwin = TemplateWindow(utils.getmayamainwindow())
    with open(os.path.join(os.path.dirname(__file__), 'styles/teal'), 'r') as myfile:
        data = myfile.read().replace('\n', '')
    mainwin.setStyleSheet(data)
    mainwin.show()

if __name__ == "__main__":
    launch()

