'''
--------------------------------------------------------

LOAD UI, methods for loading a UI designer file

--------------------------------------------------------
'''
import logging
import xml.etree.ElementTree as xml
from cStringIO import StringIO

try:
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtUiTools as QtUiTools
    import PySide2.QtWidgets as QtWidgets
except:
    print "fail to import PySide2, {}".format(__file__)
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtUiTools as QtUiTools
    import PySide.QtGui as QtWidgets



try:
    import pysideuic
    from shiboken import wrapInstance
    logging.Logger.manager.loggerDict["pysideuic.uiparser"].setLevel(logging.CRITICAL)
    logging.Logger.manager.loggerDict["pysideuic.properties"].setLevel(logging.CRITICAL)
    
except ImportError:
    import pyside2uic as pysideuic
    from shiboken2 import wrapInstance
    logging.Logger.manager.loggerDict["pyside2uic.uiparser"].setLevel(logging.CRITICAL)
    logging.Logger.manager.loggerDict["pyside2uic.properties"].setLevel(logging.CRITICAL)

def loadUiType(uiFile):
	"""
	Pyside lacks the "loadUiType" command, so we have to convert the ui file to py code in-memory first
	and then execute it in a special frame to retrieve the form_class.
	"""
	parsed = xml.parse(uiFile)
	widget_class = parsed.find('widget').get('class')
	form_class = parsed.find('class').text
	with open(uiFile, 'r') as f:
		o = StringIO()
		frame = {}
		pysideuic.compileUi(f, o, indent=0)
		pyc = compile(o.getvalue(), '<string>', 'exec')
		exec pyc in frame
		form_class = frame['Ui_%s' % form_class]
		base_class = getattr(QtWidgets, widget_class)
	return form_class, base_class
