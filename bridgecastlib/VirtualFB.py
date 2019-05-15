import numpy

class VirtualFB(object):
    def __init__(self, width, height, bpp):
        self._width = width
        self._height = height
        self._bpp = bpp

        if self._bpp % 8 != 0:
            raise ValueError("BPP needs to be a multiple of 8")

        self._data = numpy.arange(1280* 720* int(self._bpp/8), dtype=numpy.uint8).reshape(1280, 720, 4, order="F")
        #self._data.fill(255)

        self.dirty = True

    def get_rect(self, x, y, width, height):
        return self._data[x:x+width,y:y+height].flatten(order="K").tobytes()

    def fill_rect(self, x, y, width, height, data):
        tmparray = numpy.frombuffer(data, dtype=numpy.uint8)
        print(tmparray)
        self._data[x:x+width,y:y+height,:].flat = tmparray
        self.dirty = True