import numpy as np
import cv2

from classes import *
from render import *


#global variables
nbr_pixels_y, nbr_pixels_x = 1024, 720
fov = radians(45) #real fov / 2
#img = np.zeros((nbr_pixels_x, nbr_pixels_y, 3))
img = np.zeros((nbr_pixels_x, nbr_pixels_y, 3), dtype=np.int32) #int32 to avoid uint8 overflow when computing specular light


mat_list = dict() #material dictionnary
#mat_list["Test"] = Material('Test', Vec3(1.0, 0.5, 0.5), 1.0, 0.25, 1.0) #BGR and not RGB !!
mat_list["Test"] = Material('Test', Vec3(255, 128, 128), 1.0, 0.25, 1.0)


light_list = list() #all lights in the scene
light_list.append(Light(Vec3(0,5, -5), 1.0, 1.0))


sphere_list = list() #all spheres in the scene
sphere_list.append(Sphere(Vec3(0,-5, -9), 1.0, mat_list["Test"]))
sphere_list.append(Sphere(Vec3(0, 0, -7), 0.5, mat_list["Test"]))
#sphere_list.append(Sphere(Vec3(-3, 3, -7), 0.75, mat_list["Test"]))

def render():
    for i in range(nbr_pixels_x):
        for j in range(nbr_pixels_y):
            x = ((i+0.5)/nbr_pixels_x-0.5)*2*tan(fov)*nbr_pixels_x/nbr_pixels_y #calculating the x coordinate in the world for the ith pixel
            y = ((j+0.5)/nbr_pixels_y-0.5)*2*tan(fov) #same for y
            z = -1 #looking in z=-1 direction
            img[i][j] = cast_ray(Ray(Vec3(0,0,0), Vec3(x, y, z).normalize()), sphere_list, light_list) #cast a ray to get the pixel color

            for n in range(len(img[i][j])): #assure everything is between 0 and 255 for the uint8 cast
                img[i][j][n] = min(255, max(0, img[i][j][n]))

    cv2.imshow("render", img.astype(np.uint8)) #uint8 because opencv can't handle anything else
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    render()
