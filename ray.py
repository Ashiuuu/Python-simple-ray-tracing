import numpy as np
import cv2
from math import *

#Utility classes
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

class Ray:
    __slots__ = 'origin', 'dir'

    def __init__(self, o=Vec3(), d=Vec3()):
        self.origin = o
        self.dir = d

class Material:
    __slots__ = 'name', 'color', 'diffuse'

    def __init__(self, n='', c=Vec3(), d=0.0):
        self.name = n
        self.color = c
        self.diffuse = d

class Light:
    __slots__ = 'pos', 'intensity'

    def __init__(self, pos=Vec3(), intensity=0.0):
        self.pos = pos
        self.intensity = intensity

class Sphere:
    __slots__ = 'center', 'radius', 'mat'

    def __init__(self, center=Vec3(), radius=0.0, m=Material()):
        self.center = center
        self.radius = radius
        self.mat = m

#Utility functions
def scalar(v1, v2):
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

def norm(v):
    return sqrt(scalar(v, v))

def vec_add(v1, v2):
    return Vec3(v1.x+v2.x, v1.y+v2.y, v1.z+v2.z)

def vec_sub(v1, v2):
    return Vec3(v1.x-v2.x, v1.y-v2.y, v1.z-v2.z)

def vec_mul(v1, scal):
    return Vec3(v1.x*scal, v1.y*scal, v1.z*scal)

#global variables
nbr_pixels_y, nbr_pixels_x = 1024, 720
fov = radians(45) #real fov / 2
img = np.zeros((nbr_pixels_x, nbr_pixels_y, 3), dtype=np.uint8)

mat_list = dict() #material dictionnary
mat_list["Blue"] = Material('Blue', Vec3(255, 181, 96), 1.0) #BGR and not RGB !!

light_list = list() #all lights in the scene
light_list.append(Light(Vec3(2,2, -3), 1.0))

sphere_list = list() #all spheres in the scene
sphere_list.append(Sphere(Vec3(0,0, -5), 1.0, mat_list["Blue"]))

def compute_ray(ray, s):
    AO = vec_sub(s.center, ray.origin) #vector from the ray origin to the sphere center
    dAC = scalar(ray.dir, AO)
    AC = vec_mul(ray.dir, dAC) #vector from ray origin to sphere center projection
    CO = vec_sub(AO, AC)
    dOC = norm(CO) #distance from the center of the sphere to its projection on the ray

    if dOC > s.radius: #if the projection of the sphere center is farther than the radius, then obviously it is not in the sphere
        return None #thus we stop here

    dCP = sqrt(s.radius*s.radius - dOC*dOC) #finding the two intersection points
    dAP = dAC - dCP
    dAPp = dAC + dCP

    if dAP < 0: #if the first point of intersection is behind us (we are inside the sphere or the sphere is behind us)
        dAP = dAPp
    if dAP < 0: #if the second one is behind us, we're in the case where the whole sphere is behind us
        return None

    return vec_add(ray.origin, vec_mul(ray.dir, dAP)) #return the coordinates of the point of intersection


def cast_ray(ray):
    for s in sphere_list:
        point = compute_ray(ray, s)
        if point != None:
            illumination = 0 #total illumination //TODO : change
            for l in light_list:
                normal = vec_sub(point, s.center).normalize() #vector from sphere center to point, which is the normal vector
                p2l = vec_sub(l.pos, point).normalize() #vector from point of intersection with sphere to light l
                if scalar(normal, p2l) >= 0:
                    illumination += s.mat.diffuse*scalar(normal, p2l)*l.intensity #diffuse intensity
            return (s.mat.color.x*illumination, illumination*s.mat.color.y, illumination*s.mat.color.z) #color to render for that pixel
    return (114,255,138) #background


def render():
    for i in range(nbr_pixels_x):
        for j in range(nbr_pixels_y):
            x = ((i+0.5)/nbr_pixels_x-0.5)*2*tan(fov)*nbr_pixels_x/nbr_pixels_y #calculating the x coordinate in the world for the ith pixel
            y = ((j+0.5)/nbr_pixels_y-0.5)*2*tan(fov) #same for y
            z = -1 #looking in z=-1 direction
            img[i][j] = cast_ray(Ray(Vec3(0,0,0), Vec3(x, y, z).normalize())) #cast a ray to get the pixel color

    cv2.imshow("render", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

render()
