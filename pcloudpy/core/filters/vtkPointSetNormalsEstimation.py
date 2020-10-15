"""
Class that define a normal estimation method based on vtkPointSetNormalsEstimation by David Doria
"""
__all__ = ["vtkPointSetNormalsEstimation"]
from pcloudpy.core.filters.base import FilterBase

import numpy as np
from vtk import vtkPolyDataAlgorithm, vtkFloatArray, vtkKdTree, vtkPlane, vtkPolyData, vtkIdList
from scipy.linalg import eigh

FIXED_NUMBER = 0
RADIUS = 1

class vtkPointSetNormalsEstimation(FilterBase):
    """
     vtkPointSetNormalEstimation filter estimates normals of a point set using a local best fit plane.

     At every point in the point set, vtkPointSetNormalEstimation computes the best
     fit plane of the set of points within a specified radius of the point (or a fixed number of neighbors).
     The normal of this plane is used as an estimate of the normal of the surface that would go through
     the points.

     vtkPointSetNormalEstimation Class is a python implementation based on the version included in PointSetProcessing by
     David Doria, see https://github.com/daviddoria/PointSetProcessing
    """

    def __init__(self, number_neighbors = 10, mode = 0,  radius = 1):

        self.mode = mode #FIXED_NUMBER
        self.number_neighbors = number_neighbors
        self.radius = radius


    def set_mode_to_fixednumber(self):
        self.mode = FIXED_NUMBER

    def set_mode_to_radius(self):
        self.mode = RADIUS

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
            super(vtkPointSetNormalsEstimation, self).set_input(input_data)
            return True
        else:
            return False



    def update(self):

        normalArray = vtkFloatArray()
        normalArray.SetNumberOfComponents( 3 )
        normalArray.SetNumberOfTuples( self.input_.GetNumberOfPoints() )
        normalArray.SetName( "Normals" )

        kDTree = vtkKdTree()
        kDTree.BuildLocatorFromPoints(self.input_.GetPoints())

        # Estimate the normal at each point.
        for pointId  in range(0, self.input_.GetNumberOfPoints()):

            point = [0,0,0]
            self.input_.GetPoint(pointId, point)
            neighborIds = vtkIdList()

            if self.mode == FIXED_NUMBER:
                kDTree.FindClosestNPoints(self.number_neighbors, point, neighborIds)

            elif self.mode == RADIUS:
                kDTree.FindPointsWithinRadius(self.radius, point, neighborIds)
                #If there are not at least 3 points within the specified radius (the current
                # #point gets included in the neighbors set), a plane is not defined. Instead,
                # #force it to use 3 points.
                if neighborIds.GetNumberOfIds() < 3 :
                    kDTree.FindClosestNPoints(3, point, neighborIds)

            bestPlane = vtkPlane()
            self.best_fit_plane(self.input_.GetPoints(), bestPlane, neighborIds)

            normal = bestPlane.GetNormal()
            normalArray.SetTuple( pointId, normal )

        self.output_ = vtkPolyData()
        self.output_.ShallowCopy(self.input_)
        self.output_.GetPointData().SetNormals(normalArray)

    def best_fit_plane(self, points, bestPlane, idsToUse):

        #Compute the best fit (least squares) plane through a set of points.
        dnumPoints = idsToUse.GetNumberOfIds()

        #Find the center of mass of the points
        center = self.center_of_mass(points, idsToUse)

        a = np.zeros((3,3))
        for pointId in range(0, dnumPoints):

            x = np.asarray([0,0,0])
            xp = np.asarray([0,0,0])
            points.GetPoint(idsToUse.GetId(pointId), x)
            xp = x - center
            a[0,:] += xp[0] * xp[:]
            a[1,:] += xp[1] * xp[:]
            a[2,:] += xp[2] * xp[:]

        #Divide by N-1
        a /= (dnumPoints-1)

        eigval, eigvec = eigh(a, overwrite_a=True, overwrite_b=True)
        #Jacobi iteration for the solution of eigenvectors/eigenvalues of a 3x3 real symmetric matrix.
        #Square 3x3 matrix a; output eigenvalues in w; and output eigenvectors in v.
        #Resulting eigenvalues/vectors are sorted in decreasing order; eigenvectors are normalized.
        #Set the plane normal to the smallest eigen vector
        bestPlane.SetNormal(eigvec[0,0], eigvec[1,0], eigvec[2,0])
        #Set the plane origin to the center of mass
        bestPlane.SetOrigin(center[0], center[1], center[2])


    def center_of_mass(self, points, idsToUse):
        #Compute the center of mass of a set of points.
        point = np.asarray([0.0, 0.0, 0.0])
        center = np.asarray([0.0,0.0,0.0])
        for i in range(0, idsToUse.GetNumberOfIds() ):
            points.GetPoint(idsToUse.GetId(i), point)
            center += point

        numberOfPoints = float(idsToUse.GetNumberOfIds())
        center /= numberOfPoints
        return center




