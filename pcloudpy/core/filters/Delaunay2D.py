#Author: Miguel Molero <miguel.molero@gmail.com>


from vtk import vtkDelaunay2D, vtkPolyData
from base import FilterBase

class  Delaunay2D(FilterBase):
    """
    2D Delaunay triangulation method
    Delaunay2d is a filter that constructs a 2D Delaunay triangulation from a vtkPolyData object

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
        super(Delaunay2D, self).__init__()
        self.alpha = alpha
        self.tolerance = tolerance

    def set_input(self, input_data):
        if isinstance(input_data, vtkPolyData):
            super(Delaunay2D, self).set_input(input_data)
            return True
        else:
            return False

    def update(self):
        delaunay = vtkDelaunay2D()
        delaunay.SetInput(self.input_)
        delaunay.SetTolerance(self.tolerance)
        delaunay.SetAlpha(self.alpha)
        delaunay.Update()
        self.output_ = delaunay.GetOutput()
