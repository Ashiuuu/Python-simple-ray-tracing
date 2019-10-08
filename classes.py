from math import *

class Vec3:
    __slots__ = 'x', 'y', 'z'

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def normalize(self):
        mag = sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        self.x = self.x/mag
        self.y = self.y/mag
        self.z = self.z/mag
        return self

    def __add__(self, o):
        return Vec3(self.x+o.x, self.y+o.y, self.z+o.z)

    def __sub__(self, o):
        return Vec3(self.x-o.x, self.y-o.y, self.z-o.z)

    def __mul__(self, o):
        if isinstance(o, self.__class__):
            return self.x*o.x + self.y*o.y + self.z*o.z
        elif isinstance(o, int) or isinstance(o, float):
            return Vec3(self.x*o, self.y*o, self.z*o)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(o))

    def __getitem__(self, key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.z
        else:
            return self.x

class Ray:
    __slots__ = 'origin', 'dir'

    def __init__(self, o=Vec3(), d=Vec3()):
        self.origin = o
        self.dir = d

class Material:
    __slots__ = 'name', 'color', 'idiffuse', 'ispecular', 'alpha'

    def __init__(self, n='', c=Vec3(), d=0.0, s=0.0, alpha=1.0):
        self.name = n
        self.color = c
        self.idiffuse = d #diffuse intensity
        self.ispecular = s #specular intensiy
        self.alpha = alpha #alpha coefficient

class Light:
    __slots__ = 'pos', 'diffuse_intensity', 'specular_intensity'

    def __init__(self, pos=Vec3(), id=0.0, ispe=0.0):
        self.pos = pos
        self.diffuse_intensity = id
        self.specular_intensity = ispe

class Sphere:
    __slots__ = 'center', 'radius', 'mat'

    def __init__(self, center=Vec3(), radius=0.0, m=Material()):
        self.center = center
        self.radius = radius
        self.mat = m
