
class VirtualFB(object):
    def __init__(self, width, height, bpp):
        self._width = width
        self._height = height
        self._bpp = bpp

        if self._bpp % 8 != 0:
            raise ValueError("BPP needs to be a multiple of 8")

        self._data = bytearray(self._width * self._height * self._bpp/8)
        self._dirty = False