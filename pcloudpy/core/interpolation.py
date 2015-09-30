#Author: Miguel Molero <miguel.molero@gmail.com>

from matplotlib import mlab
from scipy.interpolate import griddata


def natural_neighbor(x,y,z,xi,yi):
    """
    Natural Neighbor Interpolation Method.

    Natural neighbor interpolation is a method of spatial interpolation, developed by Robin Sibson.
    The method is based on Voronoi tessellation of a discrete set of spatial points.
    This has advantages over simpler methods of interpolation, such as nearest-neighbor interpolation,
    in that it provides a more smooth approximation to the underlying "true" function.
    see <a href="http://en.wikipedia.org/wiki/Radial_basis_function">Radial_basic_function

    zi = natural_neighbor(x,y,z,xi,yi) fits a surface of the form z = f*(*x, y) to the data in the (usually) nonuniformly spaced vectors (x, y, z).<br/>
    griddata() interpolates this surface at the points specified by (xi, yi) to produce zi. xi and yi must describe a regular grid.


    Parameters
    ----------

    x:  array-like, shape= 1D
        x-coord [1D array]

    y:  array-like, shape= 1D
        y-coord [1D array]

    z:  array-like, shape= 1D
        z-coord [1D array]

    xi:  array-like, shape= 2D array
        meshgrid for x-coords [2D array]

    yi:  array-like, shape= 2D array
        meshgrid for y-coords [2D array]

    Returns
    -------

    zi: array-like, shape=2D
        zi interpolated-value [2D array]  for (xi,yi)


    """
    zi = mlab.griddata(x,y,z,xi,yi)
    return zi


def nearest_griddata(x, y, z, xi, yi):
    """
    Nearest Neighbor Interpolation Method.

    Nearest-neighbor interpolation (also known as proximal interpolation or, in some contexts, point sampling) is a simple method of multivariate interpolation in one or more dimensions.<br/>

    Interpolation is the problem of approximating the value of a function for a non-given point in some space when given the value of that function in points around (neighboring) that point.<br/>
    The nearest neighbor algorithm selects the value of the nearest point and does not consider the values of neighboring points at all, yielding a piecewise-constant interpolant. <br/>
    The algorithm is very simple to implement and is commonly used (usually along with mipmapping) in real-time 3D rendering to select color values for a textured surface.<br/>

    zi = nearest_griddata(x,y,z,xi,yi) fits a surface of the form z = f*(*x, y) to the data in the (usually) nonuniformly spaced vectors (x, y, z).<br/>
    griddata() interpolates this surface at the points specified by (xi, yi) to produce zi. xi and yi must describe a regular grid.<br/>

    Parameters
    ----------
    x:  array-like
        x-coord [1D array]
    y:  array-like
        y-coord [1D array]
    z:  array-like
        z-coord [1D array]
    xi: array-like
        meshgrid for x-coords [2D array] see <a href="http://docs.scipy.org/doc/numpy/reference/generated/numpy.meshgrid.html">numpy.meshgrid</a>
    yi: array-like
        meshgrid for y-coords [2D array] see <a href="http://docs.scipy.org/doc/numpy/reference/generated/numpy.meshgrid.html">numpy.meshgrid</a>

    Returns
    -------
    Interpolated Zi Coord

    zi: array-like
        zi interpolated-value [2D array]  for (xi,yi)
    """
    zi = griddata(zip(x,y), z, (xi, yi), method='nearest')
    return zi
