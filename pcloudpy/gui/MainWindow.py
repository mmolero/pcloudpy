"""
MainWindow Class
"""
#Author: Miguel Molero <miguel.molero@gmail.com>
# License: BSD 3 clause

import os
from collections import OrderedDict

from PyQt5.QtCore import  *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal as Signal

from pcloudpy.gui.components.ViewWidget import ViewWidget
from pcloudpy.gui.ManagerLayer import Layer, ManagerLayer

from pcloudpy.gui.MainWindowBase import MainWindowBase

from ..core import io as IO
from ..core import filters as Filters

class MainWindow(MainWindowBase):
    """
    MainWindow Class.
    """
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.manager_layer = ManagerLayer()
        self._num_views = 1
        self.setMouseTracking(True)
        self.current_view = self.tab_view.currentWidget()
        self.App.setCurrentView(self.current_view)

    def setup_connections(self):
        super(MainWindow, self).setup_connections()

        #Tab View Widget
        self.tab_view.tab.plusClicked.connect(self.add_new_view)
        self.tab_view.tab.currentChanged.connect(self.current_tab)

        #Toolboxes Widget
        self.toolboxes_widget.currentItemClicked.connect(self.manager_toolbox)
        self.toolboxes_widget.currentItemSelected.connect(self.toolbox_item_selected)

        #Datasets Widget
        self.datasets_widget.currentItemChanged.connect(self.manager_datasets)
        self.datasets_widget.itemDeleted.connect(self.delete_dataset)
        self.datasets_widget.tree.clicked.connect(self.set_current_dataset)
        self.datasets_widget.tree.selectionModel().selectionChanged.connect(self.select_item)
        self.datasets_widget.itemCloneRequested.connect(self.clone_dataset)
        self.datasets_widget.filterRequested.connect(self.apply_filter)

        #FilterWidget
        #Put in enable state "Apply Filter"
        self.filter_widget.filterRequested.connect(self.get_filter_parms)

        view = self.tab_view.currentWidget()
        view.layersModified.connect(self.change_on_dataset)

        #AppObject
        self.App._QObj.layerAdded.connect(self.add_layer_from_app)

    def current_tab(self, index):
        self.current_view = self.tab_view.widget(index)
        self.datasets_widget.init_tree(self.current_view.model)
        self.object_inspector_widget.properties_tree.clear()
        self.App.setCurrentView(self.current_view)

    def add_new_view(self):
        self._num_views +=1
        view = ViewWidget()
        view.layersModified.connect(self.change_on_dataset)
        self.tab_view.addTab(view,"Layout#%s"%self._num_views)
        self.tab_view.setCurrentIndex(self._num_views)

    def set_current_dataset(self, index):
        if index.row()>0:
            current_item = index.model().itemFromIndex(index)
            layer = current_item.get_current_view().manager_layer[index.row()-1]
            props = layer.get_container().get_props()
            self.object_inspector_widget.update(props)

    def select_item(self, new_item, _):
        items = new_item.indexes()
        if len(items)!=0:
            index = new_item.indexes()[0]
            self.set_current_dataset(index)

    def delete_dataset(self, index):
        layer = self.datasets_widget.current_item.get_current_view().manager_layer.pop(index)
        layer.get_current_view().remove_actor(layer.get_container().get_actor())
        del layer

    def clone_dataset(self, index):
        layer = self.datasets_widget.current_item.get_current_view().manager_layer[index]
        current_view = layer.get_current_view()

        layer_clone = layer.copy()
        current_view.add_layer(layer_clone)

        current_view.update_render()
        self.datasets_widget.add_dataset(layer_clone, current_view)

    def change_on_dataset(self):
        pass

    def manager_datasets(self, index):
        view = self.tab_view.currentWidget()
        layer = view.manager_layer[index]
        if self.datasets_widget.current_item.checkState() == Qt.CheckState.Checked:
            layer.get_container().get_actor().SetVisibility(1)
        else:
            layer.get_container().get_actor().SetVisibility(0)
        layer.get_current_view().update_render()

    def manager_toolbox(self):
        """
        Method that manages the components of the toolboxes

        - reader
        - filter
        - display

        """

        item = self.toolboxes_widget.get_current_item()
        d = OrderedDict(item.metadata())
        #
        if not "type" in d:
            return

        if d['type'] == 'reader':
            self.filter_widget.remove_filter()
            self.filter_widget.set_filter(d['func'], None, d['text'])

            filenames, _ = QFileDialog.getOpenFileNames(self, d['message'], self.dir_path, d['format'])
            if filenames:
                for filename in filenames:
                    func = getattr(IO, d['func'])
                    self._get_datasets(func, filename)

        elif d['type'] == 'filter':
            self.filter_widget.set_filter(d['func'], d['parms'], d['text'])

        elif d['type'] == 'display':
            self.filter_widget.set_filter(d['func'], None, d['text'], only_apply=True)

    def toolbox_item_selected(self):
        """
        Update the selected item in the toolbox manager

        """
        item = self.toolboxes_widget.get_current_item()
        d = OrderedDict(item.metadata())

        if not "type" in d:
            return

        if d['type'] == 'reader':
            self.filter_widget.set_filter(d['func'], None, d['text'])

        elif d['type'] == 'filter':
            self.filter_widget.set_filter(d['func'], d['parms'], d['text'])

        elif d['type'] == 'display':
            self.filter_widget.set_filter(d['func'], None, d['text'], only_apply=True)


    def file_open(self):
        filters = "*.xyz;;*.txt;;*.las;;*.tif *.tiff;;*.vtp"
        filenames, _ = QFileDialog.getOpenFileNames(self, "Open Dataset[s]", self.dir_path, filters)
        if filenames:
            for filename in filenames:
                func = IO.select_func_from_extension(QFileInfo(filename).suffix())
                if func:
                    self._get_datasets(func,filename)

    def get_filter_parms(self):
        self.func, self.parms = self.filter_widget.get_parms()
        self.datasets_widget.set_enable_filter()

    def apply_filter(self, index):
        self.setCursor(Qt.WaitCursor)
        QApplication.processEvents()
        QApplication.processEvents()
        layer = self.datasets_widget.current_item.get_current_view().manager_layer[index]
        current_view = layer.get_current_view()
        layer_clone = layer.copy()
        name = layer_clone.get_name().replace("clone","")
        name += "_%s"%self.func
        layer_clone.set_name(name)

        #apply filter
        func = getattr(Filters, self.func)
        filter = func(**self.parms)

        data = layer_clone.get_container().get_data()

        if filter.set_input(data):
            try:
                self.setCursor(Qt.WaitCursor)
                QApplication.processEvents()
                filter.update()
            except Exception as e:
                q = QMessageBox(QMessageBox.Critical, "Error Message", e.message)
                q.setStandardButtons(QMessageBox.Ok)
                q.exec_()
                self.setCursor(Qt.ArrowCursor)
                QApplication.processEvents()
                return
            finally:
                self.setCursor(Qt.ArrowCursor)
                QApplication.processEvents()

        else:
            msg = "No suitable Filter for the chosen dataset"
            q = QMessageBox(QMessageBox.Critical, "Error Message", msg)
            q.setStandardButtons(QMessageBox.Ok)
            q.exec_()
            self.setCursor(Qt.ArrowCursor)
            QApplication.processEvents()
            return
        ###

        #Update Actors
        layer_clone.get_container().set_polydata(filter.get_output())
        current_view.add_layer(layer_clone)
        current_view.update_render()
        self.datasets_widget.add_dataset(layer_clone, current_view)


    def add_layer_from_app(self):

        layer = self.App._current_layer
        current_view = self.App._current_view
        self.datasets_widget.add_dataset(layer, current_view)
        props = layer.get_container().get_props()
        self.object_inspector_widget.update(props)

    def _get_datasets(self, func, filename):
        self.setCursor(Qt.WaitCursor)
        QApplication.processEvents()

        name = os.path.basename(filename)
        pcls = func(filename)
        pcls.update()

        current_view = self.tab_view.currentWidget()
        layer = Layer(name)
        layer.set_current_view(current_view)
        layer.set_container(pcls)

        current_view.add_layer(layer)
        current_view.update_render()

        self.App.setCurrentView(current_view)
        self.datasets_widget.add_dataset(layer, current_view)
        props = layer.get_container().get_props()
        self.object_inspector_widget.update(props)

        self.setCursor(Qt.ArrowCursor)
        QApplication.processEvents()

