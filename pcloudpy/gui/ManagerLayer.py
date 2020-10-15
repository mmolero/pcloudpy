"""
ManagerLayer Class
"""
#Author: Miguel Molero <miguel.molero@gmail.com>

import copy

class Layer(object):
    """
    Layer Class

    Attributes
    ----------

    _container: pcloudpy.core.io.base.DataBase

    _current_view: pcloudpy.gui.components.ViewWidget

    _is_visible: Bool

    _name: String


    """
    def __init__(self, name):

        self._name = name
        self._is_visible = True
        self._current_view = None
        self._container = None

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_current_view(self, view):
        self._current_view = view

    def get_current_view(self):
        return self._current_view

    def get_visibility(self):
        return self._is_visible

    def set_visibility(self, state):
        self._is_visible = state

    def set_container(self, container):
        self._container = container

    def get_container(self):
        if self._container:
            return self._container

    def copy(self):
        layer = copy.copy(self)
        layer.set_name(self._name + "_clone")
        layer.set_container(self._container.clone())
        return layer


class ManagerLayer(object):

    def __init__(self):
        self._layers = list()

    def layers(self):
        return self._layers

    def append(self, layer):
        self._layers.append(layer)

    def pop(self, index=-1):
        return self._layers.pop(index)

    def remove(self, layer):
        self._layers.remove(layer)

    def __add__(self, layer):
        self._layers.append(layer)
        return self

    def __getitem__(self, item):
        if item < len(self._layers):
            return self._layers[item]
        raise Exception("Empty List")


if __name__== '__main__':

    manager = ManagerLayer()

    layer1 = Layer("layer")
    print(isinstance(layer1, Layer))
    layer2 = Layer("layer")

    manager += layer1
    manager += layer2

    print(manager._layers)

    print(manager.pop(1))
    print(manager._layers)
