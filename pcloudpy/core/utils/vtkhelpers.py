"""helper methods
"""
#Author: Miguel Molero <miguel.molero@gmail.com>

import numpy as np
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
from vtk.util.numpy_support import get_numpy_array_type, create_vtk_array, get_vtk_array_type, numpy_to_vtkIdTypeArray
from vtk.util.numpy_support import get_vtk_to_numpy_typemap
from vtk import vtkPoints, vtkCellArray, vtkIdTypeArray, vtkUnsignedCharArray, vtkPolyData, vtkPolyDataMapper, vtkActor
from vtk import vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor
from vtk import VTK_POINTS, VTK_FLOAT, VTK_CHAR, VTK_UNSIGNED_CHAR
from vtk import  vtkPlaneSource, vtkLookupTable, vtkTexture, vtkImageMapToColors, vtkImageActor, vtkImageData, vtkDataSetMapper


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


def actor_from_unstructuredgrid(data):
    mapper = vtkDataSetMapper()
    mapper.SetInput(data)
    actor = vtkActor()
    actor.SetMapper(mapper)
    return actor


def actor_from_polydata(PolyData):
    """
    Returns the VTK Actor from vtkPolyData Structure
    """
    mapper = vtkPolyDataMapper()
    mapper.SetInput(PolyData)
    actor = vtkActor()
    actor.SetMapper(mapper)
    #actor.GetProperty().SetPointSize(2)
    return actor

def actor_from_imagedata(imagedata):
    actor = vtkImageActor()
    actor.SetInput(imagedata)
    actor.InterpolateOff()
    return actor



def display_from_actor(actor):
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    renderer.AddActor(actor)
    # enable user interface interactor
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renderWindow)
    iren.Initialize()
    renderWindow.Render()
    iren.Start()


def numpy_to_image(numpy_array):
    """
    @brief Convert a numpy 2D or 3D array to a vtkImageData object
    @param numpy_array 2D or 3D numpy array containing image data
    @return vtkImageData with the numpy_array content
    """

    shape = numpy_array.shape
    if len(shape) < 2:
        raise Exception('numpy array must have dimensionality of at least 2')

    h, w = shape[0], shape[1]
    c = 1
    if len(shape) == 3:
        c = shape[2]

    # Reshape 2D image to 1D array suitable for conversion to a
    # vtkArray with numpy_support.numpy_to_vtk()
    linear_array = np.reshape(numpy_array, (w*h, c))
    vtk_array = numpy_to_vtk(linear_array)

    image = vtkImageData()
    image.SetDimensions(w, h, 1)
    image.AllocateScalars()
    image.GetPointData().GetScalars().DeepCopy(vtk_array)

    return image