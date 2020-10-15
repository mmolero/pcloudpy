#Author: Miguel Molero <miguel.molero@gmail.com>

import numpy as np


from PyQt5.QtCore import  *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtCore import pyqtSignal as Signal


from vtk import vtkInteractorStyleImage, vtkInteractorStyleTrackballCamera, vtkActor, vtkImageActor
from vtk import vtkAreaPicker, vtkContourWidget, vtkOrientedGlyphContourRepresentation, vtkImplicitSelectionLoop
from vtk import vtkCleanPolyData, vtkImplicitBoolean, vtkDataSetSurfaceFilter, vtkExtractGeometry, vtkExtractPolyDataGeometry

from ..graphics.QVTKWidget import QVTKWidget

from ..utils.qhelpers import *
from ..ManagerLayer import ManagerLayer

from pcloudpy.core.utils.vtkhelpers import actor_from_polydata


class QVTKWidgetKeyEvents(QVTKWidget):
    def __init__(self, parent = None):
        super(QVTKWidgetKeyEvents, self).__init__(parent)

    keyEventRequested = Signal(int)

    def keyPressEvent(self, ev):
        super(QVTKWidgetKeyEvents, self).keyPressEvent(ev)
        self.keyEventRequested.emit(ev.key())


class ViewWidget(QWidget):
    def __init__(self, parent=None):
        super(ViewWidget,self).__init__(parent)

        self.setAttribute(Qt.WA_DeleteOnClose)

        self._is_extract = False
        self._contour_widget = None
        self.manager_layer = ManagerLayer()
        self._current_layer = None

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        self.toolbar = QToolBar()
        self.toolbar.setStyleSheet("""
            QToolBar { border: 0px }
        """)
        self.toolbar.setIconSize(QSize(16,16))

        self.vtkWidget = QVTKWidgetKeyEvents(self)
        self.vtkWidget.keyEventRequested.connect(self.key_press_event)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.vtkWidget)
        self.setLayout(layout)

        self.setup_toolbar()
        self.init_model()

    layersModified = Signal()

    def setup_toolbar(self):

        self.reset_view_action = QAction(QIcon(":/pqResetCamera32.png"), "Reset View/Camera", self)
        self.reset_view_action.setStatusTip("Reset View/Camera")
        self.reset_view_action.setToolTip("Reset View/Camera")
        self.reset_view_action.triggered.connect(self.vtkWidget.reset_view)

        self.set_view_direction_to_mx_action = QAction(QIcon(":/pqXMinus24.png"), "View Direction -x", self)
        self.set_view_direction_to_mx_action.setStatusTip("View Direction -x")
        self.set_view_direction_to_mx_action.setToolTip("View Direction -x")
        self.set_view_direction_to_mx_action.triggered.connect(self.vtkWidget.viewMX)

        self.set_view_direction_to_my_action = QAction(QIcon(":/pqYMinus24.png"), "View Direction -y", self)
        self.set_view_direction_to_my_action.setStatusTip("View Direction -y")
        self.set_view_direction_to_my_action.setToolTip("View Direction -y")
        self.set_view_direction_to_my_action.triggered.connect(self.vtkWidget.viewMY)

        self.set_view_direction_to_mz_action = QAction(QIcon(":/pqZMinus24.png"), "View Direction -z", self)
        self.set_view_direction_to_mz_action.setStatusTip("View Direction -z")
        self.set_view_direction_to_mz_action.setToolTip("View Direction -z")
        self.set_view_direction_to_mz_action.triggered.connect(self.vtkWidget.viewMZ)

        self.set_view_direction_to_px_action = QAction(QIcon(":/pqXPlus24.png"), "View Direction +x", self)
        self.set_view_direction_to_px_action.setStatusTip("View Direction +x")
        self.set_view_direction_to_px_action.setToolTip("View Direction +x")
        self.set_view_direction_to_px_action.triggered.connect(self.vtkWidget.viewPX)

        self.set_view_direction_to_py_action = QAction(QIcon(":/pqYPlus24.png"), "View Direction +y", self)
        self.set_view_direction_to_py_action.setStatusTip("View Direction +y")
        self.set_view_direction_to_py_action.setToolTip("View Direction +y")
        self.set_view_direction_to_py_action.triggered.connect(self.vtkWidget.viewPY)

        self.set_view_direction_to_pz_action = QAction(QIcon(":/pqZPlus24.png"), "View Direction +z", self)
        self.set_view_direction_to_pz_action.setStatusTip("View Direction +z")
        self.set_view_direction_to_pz_action.setToolTip("View Direction +z")
        self.set_view_direction_to_pz_action.triggered.connect(self.vtkWidget.viewPZ)

        self.selection_action = QAction(QIcon(":/pqSelectSurfPoints24.png"), "Select Points", self)
        self.selection_action.setStatusTip("Select Points")
        self.selection_action.setToolTip("Select Points")
        self.selection_action.triggered.connect(self.select_points)

        self.extract_action = QAction(QIcon(":/pqExtractSelection.png"), "Extract Selected Points", self)
        self.extract_action.setStatusTip("Extract Selected Points")
        self.extract_action.setToolTip("Extract Selected Points")
        self.extract_action.triggered.connect(self.extract_points)

        self.clean_action = createAction(self, "Clean Selected Points", self.clean_points, icon="clean.png")

        self.clean_action  = QAction(QIcon(":/clean.png"), "Clean Selected Points", self)
        self.clean_action .setStatusTip("Clean Selected Points")
        self.clean_action .setToolTip("Clean Selected Points")
        self.clean_action .triggered.connect(self.clean_points)


        addActions(self.toolbar, self.reset_view_action)
        addActions(self.toolbar, self.set_view_direction_to_mx_action)
        addActions(self.toolbar, self.set_view_direction_to_my_action)
        addActions(self.toolbar, self.set_view_direction_to_mz_action)
        addActions(self.toolbar, self.set_view_direction_to_px_action)
        addActions(self.toolbar, self.set_view_direction_to_py_action)
        addActions(self.toolbar, self.set_view_direction_to_pz_action)
        self.toolbar.addSeparator()
        addActions(self.toolbar, self.selection_action)
        addActions(self.toolbar, self.extract_action)
        addActions(self.toolbar, self.clean_action)

        self.extract_action.setEnabled(False)
        self.clean_action.setEnabled(False)

    def init_model(self):
        self.model = QStandardItemModel()
        root = self.model.invisibleRootItem()
        item = QStandardItem("build:")
        item.setIcon(QIcon(":/pqServer16.png"))
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        root.appendRow(item)

    def set_interactor_style_image(self):
        self.vtkWidget.set_interactor_style(vtkInteractorStyleImage())

    def set_interactor_style_trackball(self):
        self.vtkWidget.set_interactor_style(vtkInteractorStyleTrackballCamera())

    def add_layer(self, layer):
        self.manager_layer += layer
        self.add_actor(layer.get_container().get_actor())
        self._current_layer = layer

    def set_current_layer(self, layer):
        self._current_layer =layer

    def add_actor(self, actor):
        if isinstance(actor, vtkActor):
            self.vtkWidget.renderer.AddActor(actor)
            self.set_interactor_style_trackball()

        elif isinstance(actor, vtkImageActor):
            self.vtkWidget.renderer.AddActor2D(actor)
            self.set_interactor_style_image()

    def remove_actor(self, actor):
        self.vtkWidget.renderer.RemoveActor(actor)
        self.update_render()

    def update_render(self):
        self.vtkWidget.reset_view()
        self.vtkWidget.Render()
        self.vtkWidget.show()

    def select_points(self):
        self._is_extract = not self._is_extract
        if self._is_extract:

            self.setCursor(QCursor(Qt.CrossCursor))

            self._contour_widget = vtkContourWidget()
            self._contour_widget.SetInteractor(self.vtkWidget.get_interactor())
            self._contour_representation = vtkOrientedGlyphContourRepresentation()

            self._contour_widget.SetRepresentation(self._contour_representation)
            self._contour_representation.GetLinesProperty().SetColor(1,1,0)
            self._contour_representation.GetLinesProperty().SetLineWidth(2.0)
            self._contour_representation.GetLinesProperty().SetPointSize(10.0)
            self._contour_representation.SetAlwaysOnTop(1)
            self._contour_widget.EnabledOn()

        else:
            self.vtkWidget.get_interactor().GetRenderWindow().SetCurrentCursor(0)
            self._contour_widget.CloseLoop()
            self._contour_widget.ProcessEventsOff()
            self.vtkWidget.get_interactor().GetRenderWindow().Render()

        self.extract_action.setEnabled(True)
        self.clean_action.setEnabled(True)

    def _extract_polygon(self, PolyData, is_clean):

        self._contour_widget.EnabledOff()
        print("Init Extracting")

        self.setCursor(QCursor(Qt.WaitCursor))
        QApplication.processEvents()

        polydata_rep = self._contour_representation.GetContourRepresentationAsPolyData()
        planes = self.get_frustrum()
        normal = planes.GetNormals()

        nor = np.array([0,0,0])
        normal.GetTuple(5, nor)

        #progressBar.setValue(10)
        #QApplication.processEvents()

        selection = vtkImplicitSelectionLoop()
        selection.SetLoop(polydata_rep.GetPoints())
        selection.SetNormal(nor[0], nor[1], nor[2])

        #progressBar.setValue(20)
        #QApplication.processEvents()

        tip = vtkImplicitBoolean()
        tip.AddFunction(selection)
        tip.AddFunction(planes)
        tip.SetOperationTypeToIntersection()
        tip.Modified()

        #progressBar.setValue(40)
        #QApplication.processEvents()

        if is_clean:
            extractGeometry = vtkExtractPolyDataGeometry()
        else:
            extractGeometry = vtkExtractGeometry()

        extractGeometry.SetInputData(PolyData)
        extractGeometry.SetImplicitFunction(tip)

        if is_clean:
            extractGeometry.ExtractInsideOff()
        extractGeometry.Update()

        if is_clean:
            clean = vtkCleanPolyData()
            clean.SetInputConnection(extractGeometry.GetOutputPort())
            clean.Update()
        #progressBar.setValue(80)
        #QApplication.processEvents()

        filter = vtkDataSetSurfaceFilter()
        if is_clean:
            filter.SetInputConnection(clean.GetOutputPort())
        else:
            filter.SetInputConnection(extractGeometry.GetOutputPort())
        filter.Update()

        #progressBar.setValue(90)
        #QApplication.processEvents()

        self.setCursor(QCursor(Qt.ArrowCursor))
        QApplication.processEvents()
        self.extract_action.setEnabled(False)
        self.clean_action.setEnabled(False)

        print("End Extracting")
        return filter.GetOutput()

    def extract_points(self):
        self._apply_extraction(is_clean=False)

    def clean_points(self):
        self._apply_extraction(is_clean=True)

    def _apply_extraction(self, is_clean):
        if self._is_extract:
            self._is_extract = False
            self.vtkWidget.get_interactor().GetRenderWindow().SetCurrentCursor(0)
            self._contour_widget.CloseLoop()
            self._contour_widget.ProcessEventsOff()
            self.vtkWidget.get_interactor().GetRenderWindow().Render()

        #for idx, layer in enumerate(self.manager_layer.layers()):
        layer = self._current_layer
        actor = layer.get_container().get_actor()

        if actor.GetVisibility():
            polydata = self._extract_polygon(actor.GetMapper().GetInput(), is_clean=is_clean)
            self.vtkWidget.renderer.RemoveActor(actor)
            actor = actor_from_polydata(polydata)
            layer.get_container().update_data_from(polydata)
            layer.get_container().set_actor(actor)
            #todo
            #update data -> numpy_from_polydata

            self.add_actor(actor)

        self.update_render()

    def get_frustrum(self):

        render = self._contour_representation.GetRenderer()
        numberNodes = self._contour_representation.GetNumberOfNodes()

        V = list()
        for i in range(numberNodes):
            v = np.array([0,0])
            self._contour_representation.GetNthNodeDisplayPosition(i, v)
            V.append(v)

        xmin = np.min(np.array(V)[:,0])
        ymin = np.min(np.array(V)[:,1])
        xmax = np.max(np.array(V)[:,0])
        ymax = np.max(np.array(V)[:,1])

        p1 = np.array([xmin, ymax])
        p2 = np.array([xmax, ymin])

        picker = vtkAreaPicker()
        picker.AreaPick( p1[0], p1[1], p2[0], p2[1], render)

        planes = picker.GetFrustum()
        return planes

    def key_press_event(self, key):
        if key == Qt.Key_Escape:
            if isinstance(self._contour_widget, vtkContourWidget):
                self.vtkWidget.get_interactor().GetRenderWindow().SetCurrentCursor(0)
                self._contour_widget.ProcessEventsOff()
                self._contour_widget.SetEnabled(0)
                self.vtkWidget.get_interactor().GetRenderWindow().Render()