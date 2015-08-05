#Author: Miguel Molero <miguel.molero@gmail.com>

from PySide.QtCore import *
from PySide.QtGui import *

from widgetGenerator import widget_generator

class FilterWidget(QScrollArea):
    def __init__(self, *args, **kwargs):
        super(FilterWidget, self).__init__(*args, **kwargs)

    filterRequested = Signal()

    def set_filter(self, func, parms, text):
        self.remove_filter()
        widget = widget_generator(func=func, parms=parms, text=text)
        apply = widget.findChild(QPushButton, "apply")
        if apply:
            apply.pressed.connect(self.apply_widget)
        self.setWidget(widget)

    def remove_filter(self):
        widget = self.takeWidget()
        del widget

    def apply_widget(self):
        self.filterRequested.emit()

    def get_parms(self):
        widget = self.widget()
        return widget.get_parms()