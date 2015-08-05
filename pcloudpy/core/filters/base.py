"""Base class for all filters."""
#Author: Miguel Molero <miguel.molero@gmail.com>
# License: BSD 3 clause

from ..base import BaseObject

class FilterBase(BaseObject):
    """
    Base Class for all Filter Objects

    Attributes
    ----------

    input_: vtkPolyData
        Input Data  to be filtered

    output_: vtkPolyData
        Output Data


    """
    def __init__(self):

        self.input_ = None
        self.output_ = None

    def set_input(self, input_):
        self.input_ = input_

    def get_output(self):
        if self.output_:
            return self.output_

    def update(self):
        pass

