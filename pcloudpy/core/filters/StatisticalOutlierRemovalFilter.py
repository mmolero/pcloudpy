"""
Statistical Outlier Removal Filter uses point neighborhood statistics to filter outlier data.
"""
#Author: Miguel Molero <miguel.molero@gmail.com>
# License: BSD 3 clause


import numpy as np

from vtk import vtkPoints, vtkCellArray, vtkPolyData
from sklearn.neighbors import KDTree

from ..utils.vtkhelpers import actor_from_imagedata, actor_from_polydata
from ..io.converters import numpy_from_polydata, polydata_from_numpy
from pcloudpy.core.filters.base import FilterBase

class StatisticalOutlierRemovalFilter(FilterBase):
    """

    Statistical Outlier Removal Filter uses point neighborhood statistics to filter outlier data.
    Statistical Outlier Removal Filter is a python implementation based on the pcl::StatisticalOutlierRemoval from Point Cloud Library

    The algorithm iterates through the entire input twice.

    During the first iteration it will update the average distance that each point has to its nearest k neighbors.
    The value of k can be set using mean_k.
    Next, the mean and standard deviation of all these distances are computed in order to determine a distance threshold.
    The distance threshold will be equal to: mean + std_dev * stddev.
    The multiplier for the standard deviation can be set using std_dev.

    During the next iteration the points will be classified as inlier or outlier if their average neighbor distance is below or above this threshold respectively


    Parameters
    ----------
    mean_k : float
        The number of points to use for mean distance estimation.

    std_dev: float
        The standard deviation multiplier.
        The distance threshold will be equal to: mean + stddev_mult * stddev.
        Points will be classified as inlier or outlier if their average neighbor distance is below or above this threshold respectively.


    Notes
    -----
    For more information.

    class pcl::StatisticalOutlierRemoval (Radu Bogdan Rusu)

    R. B. Rusu, Z. C. Marton, N. Blodow, M. Dolha, and M. Beetz.
    Towards 3D Point Cloud Based Object Maps for Household Environments Robotics and Autonomous Systems Journal (Special Issue on Semantic Knowledge), 2008.


    """

    def __init__(self, mean_k, std_dev):
        super(StatisticalOutlierRemovalFilter, self).__init__()
        self.mean_k = mean_k
        self.std_dev = std_dev

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
            super(StatisticalOutlierRemovalFilter, self).set_input(input_data)
            return True
        else:
            return False

    def set_mean_k(self, value):
        self.mean_k = value

    def set_std_dev(self, value):
        self.std_dev = value

    def update(self):
        """
        Compute filter.
        """

        array_full = numpy_from_polydata(self.input_)

        array = array_full[:,0:3]
        color = array_full[:,3:]

        #KDTree object (sklearn)
        kDTree = KDTree(array, leaf_size = 5)
        dx, idx_knn = kDTree.query(array[:, :], k = self.mean_k + 1)
        dx, idx_knn = dx[:,1:], idx_knn[:,1:]

        distances = np.sum(dx, axis=1)/(self.mean_k - 1.0)
        valid_distances = np.shape(distances)[0]

        #Estimate the mean and the standard deviation of the distance vector
        sum = np.sum(distances)
        sq_sum = np.sum(distances**2)

        mean = sum / float(valid_distances)
        variance = (sq_sum - sum * sum / float(valid_distances)) / (float(valid_distances) - 1)
        stddev = np.sqrt (variance)

        # a distance that is bigger than this signals an outlier
        distance_threshold = mean + self.std_dev * stddev
        idx = np.nonzero(distances < distance_threshold)
        new_array = np.copy(array[idx])
        new_color = np.copy(color[idx])

        output = polydata_from_numpy(np.c_[new_array, new_color])
        self.output_ = output



