import numpy as np


def get_grid_from_extent(xmin, xmax, ymin, ymax, spacing_x=1.0, spacing_y=1.0):
    """
    Returns a Regular grid defined for a given extent

    Parameters
    ----------
    xmin: float
        minimum value of x

    xmax: float
        minimum value of x

    ymin:float
        minimum value of y

    ymax: float
        minimum value of y

    spacing_x: integer
        desired size for tile, x-axis (it should be an integer number). Value 1.0 by default.

    spacing_y: integer
        desired size for tile, y-axis (it should be an integer number). Value 1.0 by default.

    Returns
    -------

    xi: array, shape = (N1, N2) where N1=len(xi_v) and N2=len(yi_v)
        xi is a N2 shaped array with the elements of xi_v repeated to fill the matrix along the first dimension.

    yi: array, shape = (N1, N2) where N1=len(xi_v) and N2=len(yi_v)
        yi is a N1 shaped array with the elements of yi_v repeated to fill the matrix along the second dimension.

    xi_v: array
        xi_v evenly spaced samples, calculated over the interval [xmin, xmax].

    yi_v: array
        yi_v evenly spaced samples, calculated over the interval [ymin, ymax].

    """

    nx = int((xmax-xmin)/spacing_x)
    ny = int((ymax-ymin)/spacing_y)
    xi_v = np.linspace(xmin, xmax, nx)
    yi_v = np.linspace(ymin, ymax, ny)
    xi, yi = np.meshgrid(xi_v, yi_v)

    return xi, yi, xi_v, yi_v



def get_division_tiles(xmin, xmax, spacing_tile):
    """
    Divides the given interval [xmin, xmax] to tiles for a given spacing_tile

    If spacing_tile is bigger than the distance of the given interval [xmin, xmax], returns the same interval.
    If spacing_tile is smaller than the distance of the given interval [xmin, xmax], dividing the interval
    into as many tiles as possible with the given size.

    The last tile will have the residuary size.

    Examples:  Interval = [0,  10] and size = 3  =>  result = [ 0, 3, 6, 9, 10]
               Interval = [0,  10] and size = 4  =>  result = [ 0, 4, 8, 10]

    Parameters
    ----------

    xmin: Integer
        Interval Init (it should be a integer number)

    xmax: Integer
        Interval End (it should be a integer number)

    size: Integer
        Desired size between adjacent tiles (it should be an integer number)

    Returns
    -------

    Returns the interval [xmin, xmax] divided into tiles for an given spacing_tile

    xi_v: array
        array of points that divides the interval [xmin, xman] into tiles
    """

    num_tiles = int((xmax -xmin)/spacing_tile)

    if (xmax-xmin) < spacing_tile:
        xi_v = np.array([xmin,xmax])
    else:
        xi_v = np.array([xmin+cont*spacing_tile for cont in range(num_tiles+1) ])
        if xmax > xi_v[-1]:
            np.append(xi_v, xmax)
    return xi_v


def get_splitting_intervals(xmin, xmax, ymin, ymax, spacing_tile, pixel_size):
    """
    Divides the given extent [xmin, xmax, ymin, ymax] into tiles with the given size (spacing_tile)

    Parameters
    ----------

    xmin: float
        origin of the interval on the x-axis

    xmax: float
        end of the interval on the x-axis

    ymin: float
        origin of the interval on the y-axis

    ymax: float
        end of the interval on the y-axis

    spacing_tile: integer
        Given spacing between adjacent tiles (it should be an integer number)

    pixel_size: integer
        Number of meters of one pixel in the final raster
        (it should be a integer number and pixelOverlap/pixelSize should be an integer number)

    Returns
    -------

    Returns the interval [xmin, xmax, ymin, ymax] divided into tiles with the desired spacing_tile given

    rows: integer
        Number of rows in which the original image is divided

    columns:
        Number of columns in which the original image is divided

    xi_v: array
        array of points that divide the interval [xmin, xmax] into tiles

    yi_v: array
        array of points that divide the interval [ymin, ymax] into tiles

    """

    ixmin, ixmax = _get_integer_intervals(xmin, xmax)
    iymin, iymax = _get_integer_intervals(ymin, ymax)

    xi_v = get_division_tiles(ixmin, ixmax, spacing_tile)
    columns = len(xi_v)-1
    yi_v = get_division_tiles(iymin, iymax, spacing_tile)
    rows = len(yi_v)-1

    #
    xi_v[0], yi_v[0] = xmin, ymin
    xi_v[-1], yi_v[-1] = xmax, ymax

    iniX1, iniX2 = _get_integer_interval_multiple(xi_v[0], xi_v[1], pixel_size)
    iniY1, iniY2 = _get_integer_interval_multiple(yi_v[0], yi_v[1], pixel_size)
    endX1, endX2 = _get_integer_interval_multiple(xi_v[-2], xi_v[-1], pixel_size)
    endY1, endY2 = _get_integer_interval_multiple(yi_v[-2], yi_v[-1], pixel_size)

    xi_v[0], yi_v[0] = iniX1, iniY1
    xi_v[-1], yi_v[-1] = endX2, endY2

    return rows,columns, xi_v, yi_v



def _get_integer_intervals(xmin, xmax):
    """
    For a given interval [xmin, xmax], returns the minimum interval [iXmin, iXmax] that contains the original one where iXmin and iXmax are Integer numbers.

    Examples:  [ 3.45,  5.35]  =>  [ 3,  6]
               [-3.45,  5.35]  =>  [-4,  6]
               [-3.45, -2.35]  =>  [-4, -2]

    Parameters
    ----------

    xmin: float
        origin of the interval

    xmax: float
        end of the interval

    Returns
    -------
    Returns the interval [iXmin, iXmax]

    iXmin: integer
        Minimum value of the integer interval

    iMmax: integer
        Maximum value of the integer interval

    """

    if(xmin<0.0 and xmin!=int(xmin)):
        iXmin=int(xmin-1)
    else:
        iXmin = int(xmin)

    if(xmax==int(xmax)):
        iXmax=xmax
    else:
        iXmax=int(xmax+1)

    return iXmin, iXmax


def _get_integer_interval_multiple(xmin, xmax, number):
    """
    For a given interval [xmin, xmax], returns the minimum interval [iXmin, iXmax] that contains the original one
    where iXmin and iXmax are Integer numbers and the difference (iXmax-iXmin) is a multiple of 'number'.

    Examples:  [xmin,xmax]=[ 3.45,  5.35] , number= 3  =>  [ 3,  6]
               [xmin,xmax]=[ 3.45,  5.35] , number= 7  =>  [-1,  6]
               [xmin,xmax]=[ 3.45,  15.35], number= 7  =>  [ 2, 16]

    Parameters
    ----------

    xmin: float
        origin of the interval

    xmax: float
    end of the interval

    number:  integer
        the final interval (iXmin, iXmax) must meet the following rule: the difference (iXmax-iXmin) will be a multiple of this number.


    Returns
    -------
    Returns the interval [iXmin, iXmax]

    iXmin: integer
        Minimum value of the integer interval

    iMmax: integer
        Maximum value of the integer interval

    """

    a, b = _get_integer_intervals(xmin, xmax)
    while (np.mod(b-a, number) > 0.0):
        a -= 1.0

    return a, b


def horizontal_mosaicing_list(rasters, row, columns):

    result = rasters[row*columns][0]
    for cont in range(1, columns):
        result = np.hstack((result, rasters[row*columns + cont][0]))
    return result


def mosaicing(rasters, rows, columns):

    result = horizontal_mosaicing_list(rasters, 0, columns)
    for cont in range(1, rows):
        h = horizontal_mosaicing_list(rasters, cont, columns)
        result = np.vstack((result,h))

    return result