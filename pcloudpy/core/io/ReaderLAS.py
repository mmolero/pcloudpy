#Author: Miguel Molero <miguel.molero@gmail.com>

__all__=['ReaderLAS']


import numpy as np
from laspy.file import File as FileLAS

from .base import PointsCloudBase


class ReaderLAS(PointsCloudBase):
    """
    Reader for LAS Files

    example:
        reader = ReaderLAS(filename)
        reader.update()


    """
    def __init__(self, filename):
        super(ReaderLAS, self).__init__()
        self.filename_ = filename

    def _update(self):

        f = FileLAS(self.filename_, mode='r')
        points = f.get_points()
        name = points.dtype.fields.keys()

        x = f.get_x_scaled()
        y = f.get_y_scaled()
        z = f.get_z_scaled()

        #Check is the LAS File contains red property
        if 'red' in points.dtype.fields[name[0]][0].fields.keys():
            red = np.int32(255.0*f.red/65536.0)
            green = np.int32(255.0*f.green/65536.0)
            blue = np.int32(255.0*f.blue/65536.0)
            self.data_ = np.c_[x, y, z, red, green, blue]
        else:
            N = f.X.shape[0]
            color = 128*np.ones((N,), dtype=np.int32)
            self.data_ = np.c_[x, y, z, color, color, color]






