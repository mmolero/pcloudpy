"""

"""
from vtk import vtkExtractUnstructuredGrid, vtkGeometryFilter, vtkAppendFilter,  vtkPolyData, vtkCleanPolyData
from pcloudpy.core.filters.base import FilterBase

class ExtractPolyData(FilterBase):
    """
    Extent Extraction from a Point Cloud

    Parameters
    ----------

    extent: tuple, shape=6,
        Extent = (xmin, xmax, ymin, ymax, zmin, zmax)

    """
    def __init__(self, extent):
        super(ExtractPolyData, self).__init__()
        self.extent = extent

    def set_input(self, input_data):
        if isinstance(input_data, vtkPolyData):
            super(ExtractPolyData, self).set_input(input_data)
            return True
        else:
            return False

    def update(self):
        """

        """

        appendFilter = vtkAppendFilter()
        appendFilter.AddInput(self.input_)
        appendFilter.Update()

        extractGrid = vtkExtractUnstructuredGrid()
        extractGrid.SetInputData(appendFilter.GetOutput())
        extractGrid.SetExtent(self.extent[0], self.extent[1], self.extent[2],  self.extent[3],  self.extent[4], self.extent[5])

        geom = vtkGeometryFilter()
        geom.SetInputConnection(extractGrid.GetOutputPort() )
        geom.Update()

        clean = vtkCleanPolyData()
        clean.PointMergingOn()
        clean.SetTolerance(0.01)
        clean.SetInput(geom.GetOutput())
        clean.Update()

        self.output_ = clean.GetOutput()

