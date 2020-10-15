


"""
Class that define oriented normal estimation method based on PCA Eigen method to fit plane and minimum spanning tree

"""
__all__ = ["OrientedNormalsEstimation"]

import numpy as np
from scipy.linalg import eigh
from sklearn.neighbors import NearestNeighbors
import networkx as nx

from pcloudpy.core.filters.base import FilterBase
from ..io.converters import numpy_from_polydata, copy_polydata_add_normals


class OrientedNormalsEstimation(FilterBase):
    """
     NormalEstimation filter estimates normals of a point cloud using PCA Eigen method to fit plane

    Parameters
    ----------

    number_neighbors: int
        number of neighbors to be considered in the normals estimation


    Attributes
    ----------
    input_: vtkPolyData
        Input Data  to be filtered

    output_: vtkPolyData
        Output Data



    """

    def __init__(self, number_neighbors = 10):

        self.number_neighbors = number_neighbors


    def update(self):

        array_with_color  = numpy_from_polydata(self.input_)
        normals = np.empty_like(array_with_color[:,0:3])
        coord = array_with_color[:,0:3]

        neigh = NearestNeighbors(self.number_neighbors)
        neigh.fit(coord)

        for i in range(0,len(coord)):
            #Determine the neighbours of point
            d = neigh.kneighbors(coord[i])
            #Add coordinates of neighbours , dont include center point to array. Determine coordinate by the index of the neighbours.
            y = np.zeros((self.number_neighbors-1,3))
            y = coord[d[1][0][1:self.number_neighbors],0:3]
            #Get information content
            #Assign information content to each point i.e xyzb
            normals[i,0:3] = self.get_normals(y)

        #Get the point with highest z value , this will be used as the starting point for my depth search
        z_max_point = np.where(coord[:,2]== np.max(coord[:,2]))
        z_max_point = int(z_max_point[0])

        if normals[z_max_point,2] < 0 : #ie normal doesnt point out
            normals[z_max_point,:]=-normals[z_max_point,:]

        #Create a graph
        G = nx.Graph()

        #Add all points and there neighbours to graph, make the weight equal to the distance between points
        for i in range(0,len(coord)):

            d = neigh.kneighbors(coord[i,:3])
            for c in range(1,self.number_neighbors):
                p1 = d[1][0][0]
                p2 = d[1][0][c]
                n1 = normals[d[1][0][0],:]
                n2 = normals[d[1][0][c],:]
                dot = np.dot(n1,n2)
                G.add_edge(p1,p2,weight =1-np.abs(dot))


        T = nx.minimum_spanning_tree(G)

        x=[]
        for i in nx.dfs_edges(T,z_max_point):
            x+=i


        inds = np.where(np.diff(x))[0]
        out = np.split(x,inds[np.diff(inds)==1][1::2]+1)

        for j in range(0,len(out)):
            for i in range(0,len(out[j])-1):
                n1 = normals[out[j][i],:]
                n2 = normals[out[j][i+1],:]
                if np.dot(n2,n1)<0:
                    normals[out[j][i+1],:]=-normals[out[j][i+1],:]


        self.output_ = copy_polydata_add_normals(self.input_, normals)


    def get_normals(self, XYZ):

        #The below code uses the PCA Eigen method to fit plane.
        #Get the covariance matrix
        average = np.sum(XYZ, axis=0)/XYZ.shape[0]
        b  = np.transpose(XYZ - average)
        cov     = np.cov(b)
        #Get eigen val and vec
        e_val,e_vect = eigh(cov, overwrite_a=True, overwrite_b=True)
        norm =  e_vect[:,0]
        return norm