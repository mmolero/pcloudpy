#Author: Miguel Molero <miguel.molero@gmail.com>

from PySide import QtGui
import markdown2

class LineEdit(QtGui.QLineEdit):
     def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)
        self.setMaximumWidth(60)
        self.setText(str(0))


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


def widget_generator(func, parms, text=""):

    class TemplateWidget(QtGui.QWidget):
        def __init__(self, parent=None, func=None, parms=None, text=""):
            super(TemplateWidget, self).__init__(parent)
            self.parms = None
            self.func = func
            if parms is not None:
                self.init_params(parms, text)
            else:
                self.init_text(text)

        def init_params(self, parms, text):
            self.parms = dict(parms)

            grid = QtGui.QGridLayout()
            index = 0
            for (k,v) in parms.iteritems():

                if v == "Extent":
                    item = Extent()
                    item.setObjectName(k)
                    grid.addWidget(item, index, 0, 1, 1)
                else:
                    item = getattr(QtGui, v)()
                    item.setObjectName(k)
                    grid.addWidget(QtGui.QLabel(k), index, 0, 1, 1)
                    grid.addWidget(item, index, 1, 1, 1)

                index += 1

            self.apply_button = QtGui.QPushButton("Apply")
            self.apply_button.setObjectName("apply")
            self.apply_button.setFixedSize(60,60)

            grid.addWidget(self.apply_button, 0, index+1, index, 3)

            html = markdown2.markdown(str(text))
            textEdit = QtGui.QTextEdit(html)
            textEdit.setMinimumWidth(350)
            textEdit.setMinimumHeight(350)
            textEdit.setReadOnly(True)
            grid.addWidget(textEdit,index, 0, 1, 5)

            self.setLayout(grid)

        def init_text(self, text):

            html = markdown2.markdown(str(text))

            textEdit = QtGui.QTextEdit(html)
            textEdit.setMinimumWidth(350)
            textEdit.setMinimumHeight(350)
            textEdit.setReadOnly(True)

            vBox = QtGui.QVBoxLayout()
            vBox.addWidget(textEdit)

            self.setLayout(vBox)

        def get_parms(self):
            if self.parms:
                d = dict()
                for (k,v) in self.parms.iteritems():
                    if v=="Extent":
                        d[k] = self.findChild(Extent, k).get_extent()
                    else:
                        item = self.findChild(getattr(QtGui, v), k)
                        d[k] = item.value()
                return self.func, d

    return TemplateWidget(None, func, parms, text=text)
