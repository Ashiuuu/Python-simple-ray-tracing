from classes import *

def norm(v):
    return sqrt(v*v)

def vec_to_list(vector):
    return (vector.x, vector.y, vector.z)

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


def cast_ray(ray, sphere_list, light_list):
    for s in sphere_list:
        point = compute_ray(ray, s)

        if point != None:
            diffuse_intensity = 0
            specular_intensity = 0

            for l in light_list:
                temp = 1
                normal = (point - s.center).normalize() #vector from sphere center to point, which is the normal vector
                p2l = (l.pos - point).normalize() #vector from point of intersection with sphere to light l

                occlu = s.center + (normal*1.15) #point a little outside the sphere to compensate float precision
                dir_occlu = (l.pos - occlu).normalize()

                for sp in sphere_list:
                    pointp = compute_ray(Ray(occlu, dir_occlu), sp)

                    if pointp != None:
                        temp = 0

                reflected = ((normal * 2 * (p2l * normal)) - p2l).normalize() #reflected light ray from light source along the normal vector
                dotted = reflected * ray.dir * (-1) #scalar product used in specular light calculation. The ray direction is multiplied by -1 because
                #we are taking the vector from the point of intersection to the viewer

                if (normal * p2l) >= 0:
                    diffuse_intensity += s.mat.idiffuse*(normal * p2l)*l.diffuse_intensity #diffuse intensity
                    diffuse_intensity *= temp

                    if dotted >= 0:
                        specular_intensity += l.specular_intensity*s.mat.ispecular*(dotted**s.mat.alpha)
                        specular_intensity *= temp


            return vec_to_list(s.mat.color * diffuse_intensity + Vec3(255, 255, 255) * specular_intensity)

    return (150,200,125) #background
