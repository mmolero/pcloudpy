from pcloudpy.core.io.ReaderXYZ import ReaderXYZ
from pcloudpy.core.io.ReaderLAS import ReaderLAS
from pcloudpy.core.io.ReaderTIFF import ReaderTIFF
from pcloudpy.core.io.ReaderPLY import ReaderPLY
from pcloudpy.core.io.ReaderVTP import ReaderVTP

__all__ = ['ReaderXYZ', 'ReaderLAS', 'ReaderTIFF', 'ReaderPLY', 'ReaderVTP']

def select_func_from_extension(extension):
    d = dict({"xyz": ReaderXYZ, "txt": ReaderXYZ,
               "las": ReaderLAS,
               "ply": ReaderPLY,
               "vtp": ReaderVTP,
               "tiff": ReaderTIFF, "tif": ReaderTIFF })
    return d.get(extension)

