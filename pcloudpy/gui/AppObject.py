
__all__ = ['AppObject']


from PyQt5.QtCore import  *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal as Signal

from pcloudpy.gui.ManagerLayer import Layer

class AppObject(object):
    """
    Application Object



    """
    def __init__(self):

        super(AppObject, self).__init__()
        self._current_view = None
        self._current_layer = None

        class QObj(QObject):
            def __init__(self):
                super(QObj, self).__init__()
            layerAdded = Signal()

        self._QObj = QObj()


    def currentView(self):
        """
        Gets the Current View




        """
        return self._current_view

    def setCurrentView(self, view):
        """

        """
        self._current_view = view

    def getLayers(self):
        """

        """
        if self._current_view:
            return self._current_view.manager_layer.layers()

    def addObject(self, obj, name):
        """

        """
        layer = Layer(name)
        layer.set_current_view(self._current_view)
        layer.set_container(obj)

        self._current_layer = layer
        self._current_view.add_layer(layer)
        self._current_view.update_render()

        self._QObj.layerAdded.emit()