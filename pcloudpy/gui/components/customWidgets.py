from PySide import QtGui

class LineEdit(QtGui.QLineEdit):
     def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)
        self.setMaximumWidth(60)
        self.setText(str(0))

class SpinBox(QtGui.QSpinBox):
    def __init__(self, parent=None):
        super(SpinBox, self).__init__(parent)

    def set_values(self, vmin, vmax, step, value):
        self.setRange(int(vmin), int(vmax))
        self.setSingleStep(int(step))
        self.setValue(int(value))

class DoubleSpinBox(QtGui.QDoubleSpinBox):
    def __init__(self, parent=None):
        super(DoubleSpinBox, self).__init__(parent)

    def set_values(self, vmin, vmax, step, value):
        self.setRange(vmin, vmax)
        self.setSingleStep(step)
        self.setValue(value)


class Extent(QtGui.QWidget):

    def __init__(self, parent=None):
        super(Extent, self).__init__(parent)

        self.xmin_lineedit = LineEdit()
        self.xmax_lineedit = LineEdit()
        self.ymin_lineedit = LineEdit()
        self.ymax_lineedit = LineEdit()
        self.zmin_lineedit = LineEdit()
        self.zmax_lineedit = LineEdit()

        grid = QtGui.QGridLayout()
        grid.addWidget(QtGui.QLabel("xmin"), 0,0)
        grid.addWidget(self.xmin_lineedit, 0,1)
        grid.addWidget(QtGui.QLabel("xmax"), 0,2)
        grid.addWidget(self.xmax_lineedit, 0,3)
        grid.addWidget(QtGui.QLabel("ymin"), 1,0)
        grid.addWidget(self.ymin_lineedit, 1,1)
        grid.addWidget(QtGui.QLabel("ymax"), 1,2)
        grid.addWidget(self.ymax_lineedit, 1,3)
        grid.addWidget(QtGui.QLabel("zmin"), 2,0)
        grid.addWidget(self.zmin_lineedit, 2,1)
        grid.addWidget(QtGui.QLabel("zmax"),2,2 )
        grid.addWidget(self.zmax_lineedit, 2,3)

        self.setLayout(grid)

    def get_extent(self):

        return (float(self.xmin_lineedit.text()), float(self.xmax_lineedit.text()),
                float(self.ymin_lineedit.text()), float(self.ymax_lineedit.text()),
                float(self.zmin_lineedit.text()), float(self.zmax_lineedit.text()))