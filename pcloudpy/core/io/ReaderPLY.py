#Author: Miguel Molero <miguel.molero@gmail.com>

__all__ =['ReaderPLY', 'WriterPLY']

import numpy as np
from vtk import vtkPLYReader, vtkPolyData, vtkPLYWriter


from .base import PolyDataBase
from .converters import get_polydata_from

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


class WriterPLY:
    """
    Function library for exporting different data into PLY format


    - from_numpy
    - from_polydata


    """

    @staticmethod
    def from_numpy(points, tr_re, output_filename):

        polydata = get_polydata_from(points, tr_re)
        WriterPLY.from_polydata(polydata, output_filename)


    @staticmethod
    def from_polydata(polydata, output_filename):

        writerPLY = vtkPLYWriter()
        if not output_filename.endswith(".ply"):
            output_filename += ".ply"

        writerPLY.SetFileName(output_filename)
        writerPLY.SetInput(polydata)
        writerPLY.SetFileTypeToASCII()
        writerPLY.Write()

