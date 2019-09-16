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

#Utility functions
def norm(v):
    return sqrt(v*v)

def vec_to_list(vector):
    return (vector.x, vector.y, vector.z)



#global variables
nbr_pixels_y, nbr_pixels_x = 1024, 720
fov = radians(45) #real fov / 2
img = np.zeros((nbr_pixels_x, nbr_pixels_y, 3), dtype=np.uint8)





mat_list = dict() #material dictionnary
mat_list["Blue"] = Material('Blue', Vec3(255, 181, 96), 1.0, 0.25, 1.0) #BGR and not RGB !!
mat_list["White"] = Material('White', Vec3(255, 255, 255), 1.0, 1.0, 2.0)
mat_list["Full blue"] = Material('Full Blue', Vec3(255, 0, 0), 1.5, 0.75, 2.0)

light_list = list() #all lights in the scene
light_list.append(Light(Vec3(2,2, -3), 1.0, 1.0))

sphere_list = list() #all spheres in the scene
sphere_list.append(Sphere(Vec3(0,0, -5), 1.0, mat_list["Blue"]))
sphere_list.append(Sphere(Vec3(3, 3, -7), 1.5, mat_list["White"]))
sphere_list.append(Sphere(Vec3(-3, 3, -7), 0.75, mat_list["Full blue"]))




def compute_ray(ray, s):
    AO = s.center - ray.origin #vector from the ray origin to the sphere center
    dAC = ray.dir * AO
    AC = ray.dir * dAC #vector from ray origin to sphere center projection
    CO = AO - AC
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

    return ray.origin + (ray.dir * dAP) #return the coordinates of the point of intersection


def cast_ray(ray):
    for s in sphere_list:
        point = compute_ray(ray, s)

        if point != None:
            diffuse_intensity = 0
            specular_intensity = 0

            for l in light_list:
                normal = (point - s.center).normalize() #vector from sphere center to point, which is the normal vector
                p2l = (l.pos - point).normalize() #vector from point of intersection with sphere to light l

                reflected = ((normal * 2 * (p2l * normal)) - p2l).normalize() #reflected light ray from light source along the normal vector
                dotted = reflected * ray.dir * (-1) #scalar product used in specular light calculation. The ray direction is multiplied by -1 because
                #we are taking the vector from the point of intersection to the viewer

                if (normal * p2l) >= 0:
                    diffuse_intensity += s.mat.idiffuse*(normal * p2l)*l.diffuse_intensity #diffuse intensity

                    if dotted >= 0:
                        specular_intensity += l.specular_intensity*s.mat.ispecular*(dotted**s.mat.alpha)


            return vec_to_list(s.mat.color * diffuse_intensity + Vec3(255, 255, 255) * specular_intensity) #color to render for that pixel

    return (114,255,138) #background


def render():
    for i in range(nbr_pixels_x):
        for j in range(nbr_pixels_y):
            x = ((i+0.5)/nbr_pixels_x-0.5)*2*tan(fov)*nbr_pixels_x/nbr_pixels_y #calculating the x coordinate in the world for the ith pixel
            y = ((j+0.5)/nbr_pixels_y-0.5)*2*tan(fov) #same for y
            z = -1 #looking in z=-1 direction
            img[i][j] = cast_ray(Ray(Vec3(0,0,0), Vec3(x, y, z).normalize())) #cast a ray to get the pixel color
            for c in range(3): #bring the values above 255 to 255 to avoid color breaking
                if img[i][j][c] > 255:
                    img[i][j][c] = 255


    cv2.imshow("render", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

render()
