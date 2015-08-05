"""
Basic Window handling custom operations from QVTKRenderWindowInteractor
"""
#Author: Miguel Molero <miguel.molero@gmail.com>

from PySide import QtCore, QtGui

import numpy as np
from vtk import vtkWindowToImageFilter, vtkPNGWriter
from vtk import vtkPoints, vtkCellArray, vtkUnsignedCharArray, vtkPolyData, vtkPolyDataMapper, vtkActor
from vtk import vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor,vtkGenericRenderWindowInteractor, vtkInteractorStyleTrackballCamera
from vtk import vtkCellPicker, vtkAreaPicker, vtkCleanPolyData, vtkDataSetSurfaceFilter
from vtk import vtkExtractPolyDataGeometry, vtkExtractGeometry, vtkImplicitSelectionLoop, vtkImplicitBoolean
from vtk import vtkOrientedGlyphContourRepresentation,  vtkContourWidget, vtkOrientationMarkerWidget, vtkAxesActor


from QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class QVTKWidget(QVTKRenderWindowInteractor):

    def __init__(self, parent=None):
        super(QVTKWidget, self).__init__(parent)
        self._enable_axis = False
        self._Iren.SetInteractorStyle (vtkInteractorStyleTrackballCamera ())

        self.renderer = vtkRenderer()
        self.renderer.GradientBackgroundOn()
        self.renderer.SetBackground2(255.0,255.0,255.0)
        self.renderer.SetBackground(37/255.0, 85/255.0,152/255.0)

        self.GetRenderWindow().AddRenderer(self.renderer)
        self.Initialize()
        self.Start()
        self.add_axes()

    def keyPressEvent(self, ev):
        QVTKRenderWindowInteractor.keyPressEvent(self, ev)
        if ev.key() < 256:
            key = str(ev.text())
        else:
            # Has modifiers, but an ASCII key code.
            #key = chr(ev.key())
            key = chr(0)

    def add_axes(self):
        self.axis_widget = vtkOrientationMarkerWidget()
        axes = vtkAxesActor()
        axes.SetShaftTypeToLine()
        axes.SetTotalLength(0.5, 0.5, 0.5)
        self.axis_widget.SetOutlineColor(0.9300,0.5700,0.1300)
        self.axis_widget.SetOrientationMarker(axes)
        self.axis_widget.SetInteractor(self._Iren)
        self.axis_widget.SetViewport(0.80, 0.0, 1.0,0.25)

        self._enable_axis = True
        self.axis_widget.SetEnabled(self._enable_axis)
        self.axis_widget.InteractiveOff()

    def camera_control(self, roll, pitch, yaw):

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().Elevation(pitch)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().Roll(roll)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().Azimuth(yaw)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().OrthogonalizeViewUp()

        self.Render()
        self.show()

    def viewMX(self):

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetPosition(0, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetFocalPoint(-1, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp(0, 0, 1)

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCamera()
        self.Render()
        self.show()

    def viewMY(self):

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetPosition(0, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetFocalPoint(0, -1, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp(0, 0, 1)

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCamera()
        self.Render()
        self.show()

    def viewMZ(self):

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetPosition(0, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetFocalPoint(0, 0, -1)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp(0, 1, 0)

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCamera()
        self.Render()
        self.show()

    def viewPX(self):

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetPosition(0, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetFocalPoint(1, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp(0, 0, 1)

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCamera()
        self.Render()
        self.show()

    def viewPY(self):

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetPosition(0, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetFocalPoint(0, 1, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp(0, 0, 1)

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCamera()
        self.Render()
        self.show()

    def viewPZ(self):

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetPosition(0, 0, 0)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetFocalPoint(0, 0, 1)
        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActiveCamera().SetViewUp(0, 1, 0)

        self._Iren.GetRenderWindow().GetRenderers().GetFirstRenderer().ResetCamera()
        self.Render()
        self.show()

    def reset_view(self):

        self.renderer.ResetCamera()
        self.Render()
        self.show()

    def set_interactor_style(self, style):
        self.renderer.ResetCamera()
        self._Iren.SetInteractorStyle(style)

    def get_interactor(self):
        return self._Iren


if __name__ == "__main__":

    from vtk import vtkConeSource

    app = QtGui.QApplication(['QVTKWidget'])

    renderer = vtkRenderer()
    renderer.GradientBackgroundOn()
    renderer.SetBackground2(0.0,0.0,0.0)
    renderer.SetBackground(128/255.0, 128/255.0,128/255.0)

    vtkWidget = QVTKWidget()
    vtkWidget.GetRenderWindow().AddRenderer(renderer)

    vtkWidget.Initialize()
    vtkWidget.Start()
    vtkWidget.add_axes()

    cone = vtkConeSource()
    cone.SetResolution(8)
    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInput(cone.GetOutput())
    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)
    renderer.AddActor(coneActor)

    # show the widget
    vtkWidget.show()
    # start event processing
    app.exec_()