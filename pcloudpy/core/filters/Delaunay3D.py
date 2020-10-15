from vtk import vtkDelaunay3D, vtkGeometryFilter, vtkTriangleFilter, vtkPolyData

from pcloudpy.core.filters.base import FilterBase

class  Delaunay3D(FilterBase):
    """
    3D Delaunay triangulation method
    Delaunay3d is a filter that constructs a 3D Delaunay triangulation from a vtkPolyData object

    Parameters
    ----------
    PolyData: vtkPolyData
        An instance of vtkPolyData.

    alpha: float
        Specify alpha (or distance) value to control output of this filter.
        For a non-zero alpha value, only edges or triangles contained within a sphere centered at mesh vertices will be output.
        Otherwise, only triangles will be output.  , optional. (by default = 1.0.)

    tolerance: float
        tolerance to control discarding of closely spaced points, optional. (by default = 0.)


    Returns
    -------
    vtkPolyData
        2D Delaunay triangulation
    """

    def __init__(self, alpha, tolerance):
        super(Delaunay3D, self).__init__()
        self.alpha = alpha
        self.tolerance = tolerance

    def set_input(self, input_data):
        if isinstance(input_data, vtkPolyData):
            super(Delaunay3D, self).set_input(input_data)
            return True
        else:
            return False

    def update(self):
        delaunay = vtkDelaunay3D()
        delaunay.SetInput(self.input_)
        delaunay.SetTolerance(self.tolerance)
        delaunay.SetAlpha(self.alpha)
        delaunay.Update()

        geom = vtkGeometryFilter()
        geom.SetInputConnection(delaunay.GetOutputPort() )

        triangle = vtkTriangleFilter()
        triangle.SetInputConnection(geom.GetOutputPort())
        triangle.Update()
        self.output_ = triangle.GetOutput()
