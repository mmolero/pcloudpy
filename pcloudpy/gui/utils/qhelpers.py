"""Helper Methods
"""

import collections
from PySide.QtCore import *
from PySide.QtGui import *


def read_file(filename):

    fd = QFile(filename)
    if fd.open(QIODevice.ReadOnly | QFile.Text):
        text = QTextStream(fd).readAll()
        fd.close()
        return text
    else:
        return None


def createAction(parent, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):

    """
    Helper Method for the creation of Action Objects

    :param  parent
    :param  text
    :param  slot
    :param  shortcut
    :param  icon
    :param  tip
    :param  checkable
    :param  signal
    """

    action = QAction(text, parent)
    if icon is not None:
        action.setIcon(QIcon(":/%s" % icon))
    if shortcut is not None:
        action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if slot is not None:
        parent.connect(action, SIGNAL(signal), slot)
    if checkable:
        action.setCheckable(True)
    return action


def addActions(target, actions):

    if not isinstance(actions, collections.Iterable):
        target.addAction(actions)
    else:
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


def addWidgets(target, widgets):
    if not isinstance(widgets, collections.Iterable):
        target.addWidget(widgets)
    else:
        for widget in widgets:
            target.addWidget(widget)

def setEnabled(actions, state):

    if not isinstance(actions, collections.Iterable):
        actions.setEnabled(state)
    else:
        for action in actions:
            if action is not None:
                action.setEnabled(state)


def setVisible(target, state):
    if not isinstance(target, collections.Iterable):
        target.setVisible(state)
    else:
        for item in target:
            if item is not None:
                item.setVisible(state)





