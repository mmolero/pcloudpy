
__all__ = ["vtkPointSetOutlierEstimation"]

import numpy as np
from vtk import vtkPoints, vtkCellArray, vtkPolyData, vtkIdList
from vtk import vtkKdTreePointLocator
from vtk import vtkSphereSource, vtkXMLPolyDataWriter, vtkVertexGlyphFilter

from sklearn.neighbors import KDTree
from ..utils.vtkhelpers import actor_from_imagedata, actor_from_polydata
from ..io.converters import numpy_from_polydata, polydata_from_numpy
from pcloudpy.core.filters.base import FilterBase


class vtkPointSetOutlierEstimation(FilterBase):
    """
    Outlier Removal - vtkPointSetOutlierRemoval,
    Python implementation based on Point Set Processing for VTK by David Doria
    see  https://github.com/daviddoria/PointSetProcessing
         http://www.vtkjournal.org/browse/publication/708

    We take the simple definition of an outlier to be a point that is farther away from its nearest neighbor than
    expected. To implement this definition, for every point p in the point set, we compute the distance from p to
    the nearest point to p. We sort these distances and keep points whose nearest point is in a certain percentile
    of the entire point set. This parameter is specified by the user as percent_to_remove

    """

    def __init__(self, percent_to_remove):

        self.percent_to_remove = percent_to_remove

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
            super(vtkPointSetOutlierEstimation, self).set_input(input_data)
            return True
        else:
            return False

    def set_percent_to_remove(self, value):
        self.percent_to_remove = value

    def update(self):

        array_full = numpy_from_polydata(self.input_)

        array = array_full[:,0:3]
        color = array_full[:,3:]

        #KDTree object (sklearn)
        kDTree = KDTree(array)
        dx, _ = kDTree.query(array[:, :], k = 2)
        dx  = dx[:,1:].ravel()

        Indices = np.argsort(dx, axis=0)
        Npts = np.shape(Indices)[0]
        numberToKeep = int( (1 - self.percent_to_remove ) * Npts)

        idx = Indices[0:numberToKeep]

        new_array = np.copy(array[idx])
        new_color = np.copy(color[idx])
        array = np.c_[new_array, new_color]

        output = polydata_from_numpy(array)
        self.output_ = output



