"""
Class that define a normal estimation method based on PCA Eigen method to fit plane
"""
__all__ = ["NormalsEstimation"]

import numpy as np
from scipy.linalg import eigh
from sklearn.neighbors import NearestNeighbors

from base import FilterBase
from ..io.converters import numpy_from_polydata, copy_polydata_add_normals



class NormalsEstimation(FilterBase):
    """
    NormalEstimation filter estimates normals of a point cloud using PCA Eigen method to fit plane

    Parameters
    ----------

    number_neighbors: int
        number of neighbors to be considered in the normals estimation


    Attributes
    ----------
    input_: vtkPolyData
        Input Data  to be filtered

    output_: vtkPolyData
        Output Data

    """

    def __init__(self, number_neighbors = 10):
        self.number_neighbors = number_neighbors

    def update(self):

        array_with_color  = numpy_from_polydata(self.input_)
        normals = np.empty_like(array_with_color[:,0:3])
        coord = array_with_color[:,0:3]

        neigh = NearestNeighbors(self.number_neighbors)
        neigh.fit(coord)

        for i in xrange(0,len(coord)):
            #Determine the neighbours of point
            d = neigh.kneighbors(coord[i])
            #Add coordinates of neighbours , dont include center point to array. Determine coordinate by the index of the neighbours.
            y = np.zeros((self.number_neighbors-1,3))
            y = coord[d[1][0][1:self.number_neighbors],0:3]
            #Get information content
            #Assign information content to each point i.e xyzb
            normals[i,0:3] = self.get_normals(y)


        self.output_ = copy_polydata_add_normals(self.input_, normals)



    def get_normals(self, XYZ):

        #The below code uses the PCA Eigen method to fit plane.
        #Get the covariance matrix
        average = np.sum(XYZ, axis=0)/XYZ.shape[0]
        b  = np.transpose(XYZ - average)
        cov     = np.cov(b)
        #Get eigen val and vec
        e_val,e_vect = eigh(cov, overwrite_a=True, overwrite_b=True)
        norm =  e_vect[:,0]
        return norm