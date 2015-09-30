#Author: Miguel Molero <miguel.molero@gmail.com>

import numpy as np
import pandas as pd

from vtk import vtkPolyData, vtkPoints, vtkCellArray,  vtkTriangle
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk, get_numpy_array_type, get_vtk_to_numpy_typemap

def get_polydata_from(points, tr_re):

    numberPoints = len(points)
    Points = vtkPoints()
    ntype = get_numpy_array_type(Points.GetDataType())
    points_vtk = numpy_to_vtk(np.asarray(points, order='C',dtype=ntype), deep=1)
    Points.SetNumberOfPoints(numberPoints)
    Points.SetData(points_vtk)

    Triangles = vtkCellArray()
    for item in tr_re:
        Triangle = vtkTriangle()
        Triangle.GetPointIds().SetId(0,item[0])
        Triangle.GetPointIds().SetId(1,item[1])
        Triangle.GetPointIds().SetId(2,item[2])
        Triangles.InsertNextCell(Triangle)

    polydata = vtkPolyData()
    polydata.SetPoints(Points)
    polydata.SetPolys(Triangles)

    polydata.Modified()
    polydata.Update()

    return polydata



def get_points_normals_from(polydata):

    nodes_vtk_array = polydata.GetPoints().GetData()
    array = vtk_to_numpy(nodes_vtk_array)

    if polydata.GetPointData().GetScalars():
        array_normals = vtk_to_numpy(polydata.GetPointData().GetScalars("Normals"))

    return array, array_normals


def save_to_xyz_normals(polydata, filename):

    array, normals = get_points_normals_from(polydata)

    X = np.c_[array, normals]
    np.savetxt(filename, X, delimiter=' ', newline='\n')








