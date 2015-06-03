import math

def zoomed_scale(zoom):
    return 2 ** zoom


def better_round(num, base):
    return int(base * math.ceil(float(num) / base))


class Location(object):
    def __init__(self, x, y):
        self._x = int(x)
        self._y = int(y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class TileLocation(Location):
    def __init__(self, x, y, zoom=0):
        super(TileLocation, self).__init__(x, y)
        self.zoom = zoom

    def make_range(self, width, height):
        """Get range of tiles with tiles location in center. Center is rounded by zoomed level first.
        """
        zs = zoomed_scale(self.zoom)
        tmp_x = better_round(self.x, zs)
        tmp_y = better_round(self.y, zs)
        from_x, to_x = sorted([tmp_x - width * zs, tmp_x + width * zs])
        from_y, to_y = sorted([tmp_y + height * zs, tmp_y - height * zs])
        return Location(from_x, from_y), Location(to_x, to_y)


class MinecraftLocation(Location):
    def __init__(self, x, y, z, wtm):
        super(MinecraftLocation, self).__init__(x, y)
        self._worldtomap = wtm
        #self._scale = scale
        self.z = int(z)

    def to_tile_location(self, zoom_from_mapzoomin):
        """Convert location in Minecraft coordinates to x,y tiles location.

        zoom - zoom level distance from maximum inzoom level. Each dynmap server might have different mapzoomin
        settings in configuration so this has to be config independent value. With maxzoomin tiles are numbered in sequence ..., 41, 42, 43, ....
        With maxzoomin + 1 tiles are numbered ..., 40, 42, 44, ..., with maxzoomin + 2 ..., 40, 44, 48, ... and so on.
        """
        zs = zoomed_scale(zoom_from_mapzoomin)

        xx = self._worldtomap[0] * self.x + self._worldtomap[1] * self.y + self._worldtomap[2] * self.z
        yy = self._worldtomap[3] * self.x + self._worldtomap[4] * self.y + self._worldtomap[5] * self.z
        #scale_div = 2 ** (zoom + self._scale)
        scale_div = 128
        return TileLocation(better_round(xx / scale_div, zs), better_round(-(128-yy) / scale_div, zs), zoom_from_mapzoomin)
