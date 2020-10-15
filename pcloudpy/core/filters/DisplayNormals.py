from vtk import vtkArrowSource, vtkGlyph3D, vtkPolyData
from vtk import vtkRenderer, vtkRenderWindowInteractor, vtkPolyDataMapper, vtkActor, vtkRenderWindow


from pcloudpy.core.filters.base import FilterBase

class DisplayNormals(FilterBase):

    def __init__(self):
        super(DisplayNormals, self).__init__()

    def set_input(self, input_data):
        if isinstance(input_data, vtkPolyData):
            super(DisplayNormals, self).set_input(input_data)
            return True
        else:
            return False

    def update(self):
        # Source for the glyph filter
        arrow = vtkArrowSource()
        arrow.SetTipResolution(8)
        arrow.SetTipLength(0.3)
        arrow.SetTipRadius(0.1)

        glyph = vtkGlyph3D()
        glyph.SetSourceConnection(arrow.GetOutputPort())
        glyph.SetInputData(self.input_)
        glyph.SetVectorModeToUseNormal()
        glyph.SetScaleFactor(0.1)
        #glyph.SetColorModeToColorByVector()
        #glyph.SetScaleModeToScaleByVector()
        glyph.OrientOn()
        glyph.Update()

        self.output_ = glyph.GetOutput()



