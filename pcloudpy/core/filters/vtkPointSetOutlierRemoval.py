

import numpy as np
from vtk import vtkPoints, vtkCellArray, vtkPolyData, vtkIdList
from vtk import vtkKdTreePointLocator
from vtk import vtkSphereSource, vtkXMLPolyDataWriter, vtkVertexGlyphFilter
from math import sqrt


from sklearn.neighbors import KDTree
from ..utils.vtkhelpers import numpy_from_polydata,  polydata_from_numpy
from base import FilterBase

def Distance2BetweenPoints(pt1, pt2):
    return sqrt(pt1[0]-pt1[0])**2 + (pt1[1]-pt2[1])**2 +(pt1[2]-pt2[2])**2


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




def generateData():

    sphereSource = vtkSphereSource()
    sphereSource.SetRadius(1.0)
    sphereSource.SetPhiResolution(20)
    sphereSource.SetThetaResolution(20)
    sphereSource.Update()

    points = vtkPoints()
    points.DeepCopy(sphereSource.GetOutput().GetPoints())

    polyData = vtkPolyData()
    polyData.SetPoints(points)

    glyphFilter = vtkVertexGlyphFilter()
    glyphFilter.SetInputData(polyData)
    glyphFilter.Update()

    #Write the result to a file
    polyDataWriter = vtkXMLPolyDataWriter()
    polyDataWriter.SetInputData(glyphFilter.GetOutput())
    polyDataWriter.SetFileName("SpherePoints.vtp")
    polyDataWriter.Write()


def generateOutlierData():

    #Create a bunch of clustered points
    points = vtkPoints()
    spacing = .01
    for i in range(10):
        for j in range(10):
            for k in range(10):
                points.InsertNextPoint(i*spacing, j*spacing, k*spacing)




    #Add some outlier points
    val = .02
    points.InsertNextPoint(val, val, val)
    points.InsertNextPoint(-val, val, val)
    points.InsertNextPoint(val, -val, val)

    #Create cells
    vertices = vtkCellArray()
    for i in range(points.GetNumberOfPoints()):
        vertices.InsertNextCell(1)
        vertices.InsertCellPoint(i)

    polydata = vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetVerts(vertices)

    writer = vtkXMLPolyDataWriter()
    writer.SetFileName("Input.vtp")
    writer.SetInput(polydata)
    writer.Write()

    return polydata


if __name__== "__main__":

    polydata = generateOutlierData()
    outlierRemoval = vtkPointSetOutlierEstimation()
    outlierRemoval.set_input(polydata)
    outlierRemoval.set_percent_to_remove(0.01)
    outlierRemoval.update()

    writer = vtkXMLPolyDataWriter()
    writer.SetFileName("Output.vtp")
    writer.SetInput(outlierRemoval.GetOutput())
    writer.Write()


