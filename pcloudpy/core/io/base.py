"""
Bases Classes for the I/O handling
"""
#Author: Miguel Molero <miguel.molero@gmail.com>

from collections import OrderedDict
import copy
import numpy as np

from vtk import vtkPolyData, vtkImageData

from ..utils.vtkhelpers import actor_from_imagedata, actor_from_polydata
from ..io.converters import numpy_from_polydata, polydata_from_numpy

__all__ = ["DataBase", "ImageDataBase", "PolyDataBase", "PointsCloudBase"]


class DataType(object):
    POLYDATA = "polydata"
    POINTCLOUD = "pointcloud"
    IMAGEDATA = "imagedata"



class DataBase(object):
    """
    Data Base Class

    data_: Array
        store array od points of the the point cloud

    props_: OrderedDict
        Dictionary used for the props storing

    """
    def __init__(self):

        self.data_ = None
        self.props_ = None
        self.type_ = None
        self._actor = None

    def get_props(self):
        if self.props_:
            return self.props_

    def get_data(self):
        """
        Gets Container
        """
        if self.type_ in (DataType.POLYDATA, DataType.POINTCLOUD):
            print("get data")
            return self.get_polydata()
        elif self.type_ == DataType.IMAGEDATA:
            return self.get_imagedata()

    def get_actor(self):
        """
        Gets Actor
        """
        if self._actor:
            return self._actor

    def set_actor(self, actor):
        """
        Sets Actor
        """
        self._actor = actor



class ImageDataBase(DataBase):
    """
    ImageData Base Class

    Attributes
    ----------
    props_: OrderedDict
        Dictionary used for the props storing

    data_: array
        raw data


    """
    def __init__(self):
        super(ImageDataBase, self).__init__()
        self.type_ = DataType.IMAGEDATA

    def get_imagedata(self):
        """
        Gets ImageData
        """
        if self._imagedata:
            return self._imagedata

    def set_imagedata(self, imagedata):
        """
        Sets ImageData
        """
        self._imagedata = imagedata
        self._actor = actor_from_imagedata(self._imagedata)
        self.update_props()

    def _update(self):
        pass

    def update(self):
        self._update()
        self.set_imagedata(self._imagedata)
        self.update_props()

    def clone(self):
        """
        Returns a Clone of an ImageDataBase instance
        """
        imagedata = vtkImageData()
        imagedata.DeepCopy(self._imagedata)
        clone = copy.copy(self)
        clone.set_imagedata(imagedata)
        clone.set_actor(actor_from_imagedata(self._imagedata))
        return clone

    def update_props(self):

        if self._imagedata:
            self.props_ = OrderedDict()
            self.props_["Number of Points"] = self._imagedata.GetNumberOfPoints()
            bounds = self._imagedata.GetBounds()

            self.props_["xmin"] = bounds[0]
            self.props_["xmax"] = bounds[1]
            self.props_["ymin"] = bounds[2]
            self.props_["ymax"] = bounds[3]
            self.props_["zmin"] = np.min(self.data_)
            self.props_["zmax"] = np.max(self.data_)



class PolyDataBase(DataBase):
    """
    PolyData Base Class


    Attributes
    ---------
    data_: Array
        store array od points of the the point cloud

    props_: OrderedDict
        Dictionary used for the props storing

    """

    def __init__(self):
        super(PolyDataBase, self).__init__()
        self.type_ = DataType.POLYDATA

    def get_polydata(self):
        """
        Gets PolyData (vtkPolyData)
        """
        if self._polydata:
            return self._polydata

    def set_polydata(self, polydata):
        self._polydata = polydata
        self._actor = actor_from_polydata(self._polydata)
        self.update_props()

    def update(self):
        """
        Update Reader
        """
        self._update()
        self.set_polydata(self._polydata)
        self.update_props()

    def _update(self):
        pass

    def clone(self):
        polydata = vtkPolyData()
        polydata.DeepCopy(self._polydata)

        clone = copy.copy(self)
        clone.set_polydata(polydata)
        clone.set_actor(actor_from_polydata(polydata))
        return clone

    def update_data_from(self, polydata):

        self._data = numpy_from_polydata(polydata)
        self._polydata = polydata
        self._actor = actor_from_polydata(self._polydata)
        self.update_props()

    def update_props(self):

        if self._polydata:
            self.props_ = OrderedDict()
            self.props_["Number of Points"] = self._polydata.GetNumberOfPoints()

            if isinstance(self._polydata, vtkPolyData):
                polys = self._polydata.GetNumberOfPolys()
                lines = self._polydata.GetNumberOfLines()

                if polys !=0:
                    self.props_["Number of Polygons"] = polys
                if lines !=0:
                    self.props_["Number of Lines"] = lines

                verts = self._polydata.GetNumberOfVerts()
                if verts !=0:
                    self.props_["Number of Vertices"] = verts

                strips = self._polydata.GetNumberOfStrips()
                if strips !=0:
                    self.props_["Number of Triangles"] = strips

            bounds = self._polydata.GetBounds()
            self.props_["xmin"] = bounds[0]
            self.props_["xmax"] = bounds[1]
            self.props_["ymin"] = bounds[2]
            self.props_["ymax"] = bounds[3]
            self.props_["zmin"] = bounds[4]
            self.props_["zmax"] = bounds[5]




class PointsCloudBase(PolyDataBase):
    """
    Point Cloud Base Class


    Attributes
    ----------
    data_: Array
        store array od points of the the point cloud


    """
    def __init__(self, *args, **kwargs):
        super(PointsCloudBase, self).__init__(*args, **kwargs)

        self.type_ = DataType.POINTCLOUD

    def update(self):
        self._update()
        self._polydata = polydata_from_numpy(self.data_)
        self.set_polydata(self._polydata)
