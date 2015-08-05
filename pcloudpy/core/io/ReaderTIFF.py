#Author: Miguel Molero <miguel.molero@gmail.com>

__all__=['ReaderTIFF']

import gdal
import numpy as np

from ..utils.vtkhelpers import numpy_to_image
from .base import ImageDataBase


class ReaderTIFF(ImageDataBase):

    def __init__(self, filename):
        super(ReaderTIFF, self).__init__()
        self.filename_ = filename

    def _update(self):

        dataset = gdal.Open(self.filename_)
        band = dataset.GetRasterBand(1)
        self.data_ = band.ReadAsArray().astype(np.float32)
        vmin = self.data_.min()
        data = np.uint8(255*(self.data_-vmin)/ float(self.data_.max()-vmin))
        self._imagedata = numpy_to_image(data)
