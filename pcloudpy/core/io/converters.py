#Author: Miguel Molero <miguel.molero@gmail.com>

import numpy as np

from vtk import vtkPolyData, vtkPoints, vtkCellArray,  vtkTriangle
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk, get_numpy_array_type, get_vtk_to_numpy_typemap, \
    numpy_to_vtkIdTypeArray
from vtk.vtkCommonPython import vtkPoints, VTK_UNSIGNED_CHAR
from vtk.vtkFilteringPython import vtkCellArray, vtkPolyData


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

    numberArrays = polydata.GetPointData().GetNumberOfArrays()
    for i in range(numberArrays):
        if polydata.GetPointData().GetArrayName(i) == "Normals":
            array_normals = vtk_to_numpy(polydata.GetPointData().GetScalars("Normals"))
            return array, array_normals
    else:
        raise Exception("No available Normals")


def save_to_xyz_normals(polydata, filename):

    array, normals = get_points_normals_from(polydata)
    X = np.c_[array, normals]
    np.savetxt(filename, X, delimiter=' ', newline='\n')


def numpy_from_polydata(polydata):
    """
    Converts vtkPolyData to Numpy Array

    Parameters
    ----------

    polydata: vtkPolyData
        Input Polydata

    """

    nodes_vtk_array = polydata.GetPoints().GetData()
    nodes_numpy_array = vtk_to_numpy(nodes_vtk_array)

    if polydata.GetPointData().GetScalars():
        nodes_numpy_array_colors = vtk_to_numpy(polydata.GetPointData().GetScalars("colors"))
        return np.c_[nodes_numpy_array, nodes_numpy_array_colors]
    else:
        return nodes_numpy_array


def polydata_from_numpy(coords):
    """
    Converts Numpy Array to vtkPolyData

    Parameters
    ----------
    coords: array, shape= [number of points, point features]
        array containing the point cloud in which each point has three coordinares [x, y, z]
        and none, one or three values corresponding to colors.

    Returns:
    --------
    PolyData: vtkPolyData
        concrete dataset represents vertices, lines, polygons, and triangle strips

    """

    Npts, Ndim = np.shape(coords)

    Points = vtkPoints()
    ntype = get_numpy_array_type(Points.GetDataType())
    coords_vtk = numpy_to_vtk(np.asarray(coords[:,0:3], order='C',dtype=ntype), deep=1)
    Points.SetNumberOfPoints(Npts)
    Points.SetData(coords_vtk)

    Cells = vtkCellArray()
    ids = np.arange(0,Npts, dtype=np.int64).reshape(-1,1)
    IDS = np.concatenate([np.ones(Npts, dtype=np.int64).reshape(-1,1), ids],axis=1)
    ids_vtk = numpy_to_vtkIdTypeArray(IDS, deep=True)

    Cells.SetNumberOfCells(Npts)
    Cells.SetCells(Npts,ids_vtk)

    if Ndim == 4:
        color = [128]*len(coords)
        color = np.c_[color, color, color]
    elif Ndim == 6:
        color = coords[:,3:]
    else:
        color = [[128, 128, 128]]*len(coords)

    color_vtk = numpy_to_vtk(
            np.ascontiguousarray(color, dtype=get_vtk_to_numpy_typemap()[VTK_UNSIGNED_CHAR]),
            deep=True)

    color_vtk.SetName("colors")

    PolyData = vtkPolyData()
    PolyData.SetPoints(Points)
    PolyData.SetVerts(Cells)
    PolyData.GetPointData().SetScalars(color_vtk)
    return PolyData


def copy_polydata_add_normals(polydata, normals):

    Points = vtkPoints()
    ntype = get_numpy_array_type(Points.GetDataType())
    normals_vtk = numpy_to_vtk(np.asarray(normals[:,0:3], order='C',dtype=ntype), deep=1)
    normals_vtk.SetName("Normals")

    output = vtkPolyData()
    output.ShallowCopy(polydata)
    output.GetPointData().SetNormals(normals_vtk)
    return output