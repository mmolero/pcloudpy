#Author: Miguel Molero <miguel.molero@gmail.com>
import markdown2

from PyQt5.QtCore import  *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal as Signal

from pcloudpy.gui.components import customWidgets


def widget_generator(func, parms, text="", only_apply=False):

    class TemplateWidget(QWidget):
        def __init__(self, parent=None, func=None, parms=None, text="", only_apply=False):
            super(TemplateWidget, self).__init__(parent)
            self.parms = None
            self.func = func
            self.only_apply = only_apply

            if only_apply:
                self.init_apply(text)
            else:
                if parms is not None:
                    self.init_params(parms, text)
                else:
                    self.init_text(text)

        def init_apply(self, text):
            grid = QGridLayout()

            self.apply_button = QPushButton("Apply")
            self.apply_button.setObjectName("apply")
            self.apply_button.setFixedSize(60,60)
            grid.addWidget(self.apply_button, 0, 0)

            html = markdown2.markdown(str(text))
            textEdit = QTextEdit(html)
            textEdit.setMinimumWidth(350)
            textEdit.setMinimumHeight(350)
            textEdit.setReadOnly(True)
            grid.addWidget(textEdit,1, 0, 1, 5)

            self.setLayout(grid)


        def init_params(self, parms, text):
            self.parms = dict(parms)

            grid = QGridLayout()
            index = 0
            for (k,v) in parms.items():

                if v['type'] == "Extent":
                    item = customWidgets.Extent()
                    item.setObjectName(k)
                    grid.addWidget(item, index, 0, 1, 1)
                else:
                    item = getattr(customWidgets, v['type'])()
                    item.setObjectName(k)
                    item.set_values(*map(float,v['values'].strip().split(',')))
                    item.setToolTip(v.get('tooltip', ""))

                    grid.addWidget(QLabel(k), index, 0, 1, 1)
                    grid.addWidget(item, index, 1, 1, 1)

                index += 1

            self.apply_button = QPushButton("Apply")
            self.apply_button.setObjectName("apply")
            self.apply_button.setFixedSize(60,60)

            grid.addWidget(self.apply_button, 0, 3, index, 3)

            html = markdown2.markdown(str(text))
            textEdit = QTextEdit(html)
            textEdit.setMinimumWidth(350)
            textEdit.setMinimumHeight(350)
            textEdit.setReadOnly(True)
            grid.addWidget(textEdit,index, 0, 1, 5)

            self.setLayout(grid)

        def init_text(self, text):

            html = markdown2.markdown(str(text))

            textEdit = QTextEdit(html)
            textEdit.setMinimumWidth(350)
            textEdit.setMinimumHeight(350)
            textEdit.setReadOnly(True)

            vBox = QVBoxLayout()
            vBox.addWidget(textEdit)

            self.setLayout(vBox)

        def get_parms(self):

            if self.only_apply:
                return self.func, dict()

            if self.parms:
                d = dict()
                for (k,v) in self.parms.items():
                    if v['type'] =="Extent":
                        d[k] = self.findChild(customWidgets.Extent, k).get_extent()
                    else:
                        item = self.findChild(getattr(customWidgets, v['type']), k)
                        d[k] = item.get_values()
                return self.func, d

    return TemplateWidget(None, func, parms, text=text, only_apply=only_apply)
