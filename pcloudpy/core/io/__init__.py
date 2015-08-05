from ReaderXYZ import ReaderXYZ
from ReaderLAS import ReaderLAS
from ReaderTIFF import ReaderTIFF
from ReaderPLY import ReaderPLY
from ReaderVTP import ReaderVTP

__all__ = ['ReaderXYZ', 'ReaderLAS', 'ReaderTIFF', 'ReaderPLY', 'ReaderVTP']

def select_func_from_extension(extension):
    d = dict({"xyz": ReaderXYZ, "txt": ReaderXYZ,
               "las": ReaderLAS,
               "ply": ReaderPLY,
               "vtp": ReaderVTP,
               "tiff": ReaderTIFF, "tif": ReaderTIFF })
    return d.get(extension)

