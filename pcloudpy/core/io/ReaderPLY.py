#Author: Miguel Molero <miguel.molero@gmail.com>

__all__ =['ReaderPLY']

from vtk import vtkPLYReader
from .base import PolyDataBase

class ReaderPLY(PolyDataBase):
    """
    Reader for PLY Files

    example:
        reader = ReaderPLY(filename)
        reader.update()

    """
    def __init__(self, filename):
        super(ReaderPLY, self).__init__()
        self.filename_ = filename

    def _update(self):
        reader = vtkPLYReader()
        reader.SetFileName(self.filename_)
        reader.Update()
        self._polydata = reader.GetOutput()




