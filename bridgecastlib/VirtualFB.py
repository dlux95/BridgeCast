import numpy

class VirtualFB(object):
    def __init__(self, width, height, bpp):
        self._width = width
        self._height = height
        self._bpp = bpp

        if self._bpp % 8 != 0:
            raise ValueError("BPP needs to be a multiple of 8")

        self._data = numpy.zeros((self._height, self._width, int(self._bpp/8)), dtype=numpy.uint8)

        self.dirty = True

    def get_rect(self, x, y, width, height):
        return self._data[y:y+height,x:x+width].flatten(order="K").tobytes()

    def fill_rect(self, x, y, width, height, data):
        tmparray = numpy.ndarray((width, height, int(self._bpp/8)), buffer=data, dtype=numpy.uint8)
        self._data[y:y+height,x:x+width,] = tmparray
        self.dirty = True