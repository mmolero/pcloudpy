#Author: Miguel Molero <miguel.molero@gmail.com>

__all__=['ReaderXYZ']

import pandas as pd
from .base import PointsCloudBase

class ReaderXYZ(PointsCloudBase):
    """
    Opens XYZ[RGB] format files. XYZ Coordinates,
    Color:
        - RGB Color,
        - one scalar
        - None
    """
    def __init__(self, filename):
        super(ReaderXYZ, self).__init__()
        self.filename_ = filename

    def _update(self):
        """
        Reads XYZ[RGB] Format file
        """
        df = pd.read_csv(self.filename_, sep=' ')
        #export to numpy array
        self.data_ = df.to_numpy()







