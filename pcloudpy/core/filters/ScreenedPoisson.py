import numpy as np
from vtk import vtkPolyData
from base import FilterBase
from ..io.converters import get_points_normals_from, get_polydata_from

from pypoisson import poisson_reconstruction


class ScreenedPoisson(FilterBase):


    def __init__(self, depth=8, full_depth=5, scale=1.1, samples_per_node=1.0, cg_depth=0.0,
                            enable_polygon_mesh=False, enable_density=False):

        super(ScreenedPoisson, self).__init__()
        self.depth= depth
        self.full_depth = full_depth
        self.scale = scale
        self.samples_per_node=samples_per_node
        self.cg_depth=cg_depth
        self.enable_polygon_mesh=enable_polygon_mesh
        self.enable_density = enable_density

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
            super(ScreenedPoisson, self).set_input(input_data)
            return True
        else:
            return False


    def update(self):

        points, normals = get_points_normals_from(self.input_)
        faces, vertices = poisson_reconstruction(points, normals,
                                                    depth=self.depth)

        self.output_ = get_polydata_from(vertices, faces)


