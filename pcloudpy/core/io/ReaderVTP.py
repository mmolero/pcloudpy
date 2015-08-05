#Author: Miguel Molero <miguel.molero@gmail.com>

__all__=['ReaderVTP']

from vtk import vtkXMLPolyDataReader

from .base import PolyDataBase

class ReaderVTP(PolyDataBase):
    def __init__(self, filename):
        super(ReaderVTP, self).__init__()
        self.filename_ = filename

    def _update(self):
        reader = vtkXMLPolyDataReader()
        reader.SetFileName(self.filename_)
        reader.Update()
        self._polydata = reader.GetOutput()

