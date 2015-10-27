"""Base class for all filters."""
#Author: Miguel Molero <miguel.molero@gmail.com>
# License: BSD 3 clause

from vtk import vtkPolyData

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

    def set_input(self, input_data):

        """
        set input data

        Parameters
        ----------
        input-data : vtkPolyData

        Returns
        -------
        is_valid: bool
            Returns True if the input_data is valid for processing

        """
        if isinstance(input_data, vtkPolyData):
            return True
        else:
            return False


    def get_output(self):

        if self.output_:
            return self.output_

    def update(self):
        pass

