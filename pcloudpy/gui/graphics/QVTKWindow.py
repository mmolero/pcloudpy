#Author: Miguel Molero <miguel.molero@gmail.com>
from PyQt5.QtCore import  *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from pcloudpy.gui.graphics.QVTKWidget import QVTKWidget

class QVTKMainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(QVTKMainWindow, self).__init__(parent)
        self.vtkWidget = QVTKWidget(self)
        self.setCentralWidget(self.vtkWidget)
        self.setWindowTitle("QVTKMainWindow")
        self.setGeometry(50,50, 800,800)


if __name__ == "__main__":

    from vtk import vtkConeSource
    from vtk import vtkPolyDataMapper, vtkActor

    app = QApplication(['QVTKWindow'])

    win = QVTKMainWindow()

    cone = vtkConeSource()
    cone.SetResolution(8)
    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInput(cone.GetOutput())
    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)

    win.vtkWidget.renderer.AddActor(coneActor)
    # show the widget
    win.show()
    # start event processing
    app.exec_()