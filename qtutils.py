import os

INMAYA = False
try:
    import maya.cmds as cmds
    import on_sys_builder.noPopSys # FOR POP SYSTEM OF RIG
    INMAYA = True
except:
    pass

try:
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtUiTools as QtUiTools
    import PySide2.QtWidgets as QtWidgets
    # import PySide2.QtCompat as QtCompat
    print "USING PYSIDE2"
except:
    print "fail to import PySide2, %s" % __file__
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtUiTools as QtUiTools
    import PySide.QtGui as QtWidgets


'''
--------------------------------------------------------

UTILS FUNCTIONS

--------------------------------------------------------
'''

import inspect

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def getmayamainwindow():
    """Return Maya's main window"""
    for obj in QtWidgets.qApp.topLevelWidgets():
        try:
            if obj.objectName() == 'MayaWindow':
                return obj
        except:
            print '-'*20
            print obj
            print 'has no object type'
            print '-'*20
    raise RuntimeError('Could not find MayaWindow instance')

def isanimfile(filename):
    s = os.path.splitext(filename)[0]+'_thumbs'
    if os.path.isdir(s):
        return True
    return False

def mayarefreshviewport():
    cmds.undoInfo(stateWithoutFlush=False)
    time = cmds.currentTime(query=True)
    cmds.currentTime(time, edit=True)
    cmds.refresh(force=True)
    cmds.undoInfo(stateWithoutFlush=True)


def getobjectnamespace(objectname):
    namespace=objectname.rpartition(':')[0]
    return namespace


def getriggednamspaces():
    #get rigs namspace in scene....
    namespaces=[]
    if INMAYA:
        rigs=cmds.ls( "*:x__rig__grp__*")
        print 'current rigs in scene ',rigs
        for rig in rigs:
            splitted=rig.split(':')
            if len(splitted)>0:
                namespaces.append(splitted[0])
    return namespaces


def connectconstraints(fullobjnames):
    #connect constraints after applying an anim (playmo rig)
    for fullobjname in fullobjnames:
        if cmds.objExists(fullobjname + '.on_SysType'):
            if cmds.getAttr(fullobjname + '.on_SysType') =='noPop':
                s = on_sys_builder.noPopSys.NoPopSys()
                s.getInfosFromGrp(fullobjname)
                s.connectControlToConstraintKeys(_connectConstraintToControl = False)

def messageok(title, message):
    # oK message box
    msgBox = QtWidgets.QMessageBox()
    msgBox.setText(title)
    msgBox.setInformativeText(message)
    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    ret = msgBox.exec_()
    return ret

'''
--------------------------------------------------------------------------------
Progressbardialog
SOLVED PROBLEM OF MODALITY, solved by claude
--------------------------------------------------------------------------------
'''
class Progressbardialog():

    def __init__(self, title, message, maxvalue):
        self.pd = QtWidgets.QProgressDialog(message, None, 0, maxvalue)
        self.pd.setWindowModality(QtCore.Qt.NonModal)
        self.pd.setWindowTitle(title)
        self.pd.show()
        self.pdwascancelled = False
        self.pd.setValue(0)

    def __del__(self):
        self.pd.close()

    def incrementvalue(self):
        self.pd.setValue(self.pd.value() + 1)

    def addvalue(self,count):
        self.pd.setValue(self.pd.value() + count)

    def setvalue(self,count):
        self.pd.setValue(count)

'''
--------------------------------------------------------------------------------

CUSTOM EVENTS AND CUSTOM CLASSES

--------------------------------------------------------------------------------
'''

class mouseoverEvent(QtCore.QObject):
    # put this on your class if needed
    # self.filter = mouseoverEvent(self)
    # self.installEventFilter(self.filter)
    def __init__(self, parent):
        super(mouseoverEvent, self).__init__(parent)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.HoverLeave:
            print "Exit!"
            return True

        if event.type() == QtCore.QEvent.HoverMove:
            print "moving...!"
            print event.pos()
            return True

        if event.type() == QtCore.QEvent.HoverEnter:
            print "Enter!"
            return True
        return False

class mouseClickEvent(QtCore.QObject):
    # put this on your class if needed
    # self.filter = mouseClickEvent(self)
    # self.installEventFilter(self.filter)
    def __init__(self, parent):
        super(mouseClickEvent, self).__init__(parent)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            print "Clicked !"
            print object
            return True

        return False

class ExtendedQPushButton(QtWidgets.QPushButton):
    # put this on your class if needed
    # self.filter = mouseoverEvent(self)
    # self.iconlabel.installEventFilter(self.filter)
    def __init__(self, parent):
        super(ExtendedQPushButton, self).__init__(parent)

    def wheelEvent(self, ev):
        # self.emit(QtCore.SIGNAL('pressed()'))
        self.emit(QtCore.SIGNAL('scroll(int)'), ev.delta())
        # self.emit(QtCore.SIGNAL(('scroll(int)'), ev.delta()))

class ExtendedQToolButton(QtWidgets.QToolButton):
    # put this on your class if needed
    # self.filter = mouseoverEvent(self)
    # self.iconlabel.installEventFilter(self.filter)
    def __init__(self, parent):
        super(ExtendedQToolButton, self).__init__(parent)

