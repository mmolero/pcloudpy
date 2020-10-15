"""helper methods
"""
#Author: Miguel Molero <miguel.molero@gmail.com>

import numpy as np
from vtk.util.numpy_support import numpy_to_vtk
from vtk import vtkPolyDataMapper, vtkActor
from vtk import vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor
from vtk import vtkImageActor, vtkImageData, vtkDataSetMapper


def actor_from_unstructuredgrid(data):
    mapper = vtkDataSetMapper()
    mapper.SetInputData(data)
    actor = vtkActor()
    actor.SetMapper(mapper)
    return actor


def actor_from_polydata(PolyData):
    """
    Returns the VTK Actor from vtkPolyData Structure
    """
    mapper = vtkPolyDataMapper()
    mapper.SetInputData(PolyData)
    actor = vtkActor()
    actor.SetMapper(mapper)
    #actor.GetProperty().SetPointSize(2)
    return actor

def actor_from_imagedata(imagedata):
    actor = vtkImageActor()
    actor.SetInputData(imagedata)
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