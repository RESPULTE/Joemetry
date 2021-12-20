from typing import List, Tuple, Union, Optional
from vector2D import Vector2D as vec
from math import sqrt, acos, sin, cos, radians

Point = Tuple[int, int]


# DOCCUMENTATION, LINEAR INTERPOLATION
def get_circumcircle_of_triangle(triangle: List[Point], radius: bool = True) -> Union[Tuple[vec, float], vec]:
    point_a, point_b, point_c = triangle

    angle_a = sin(2 * get_angle(point_b, point_c, point_a))
    angle_b = sin(2 * get_angle(point_c, point_a, point_b))
    angle_c = sin(2 * get_angle(point_a, point_b, point_c))

    circumcenter_x = (point_a[0] * angle_a + point_b[0] * angle_b + point_c[0] * angle_c) / (angle_a + angle_b + angle_c)
    circumcenter_y = (point_a[1] * angle_a + point_b[1] * angle_b + point_c[1] * angle_c) / (angle_a + angle_b + angle_c)
    circumcenter   = (circumcenter_x, circumcenter_y)
    
    if radius:
        circumradius = get_length(point_a - point_b) / angle_c
        return circumcenter, circumradius

    return circumcenter


def get_intersect(line1: List[vec], line2: List[vec]) -> Union[None, vec]:
    line1, line2 = vec.convert(line1), vec.convert(line2)
    start = line2[0] - line1[0]
    end_1, end_2 = line1[1] - line1[0], line2[1] - line2[0]

    determinant = end_1.cross(end_2)
    if determinant == 0: return None

    check_1 = (start).cross(end_2) / determinant
    check_2 = (start).cross(end_1) / determinant
    if (0 <= check_1 <= 1) and (0 <= check_2 <= 1):
        return round(line1[0] + (line1[1] - line1[0]) * check_1, 2)

    return None


def get_support(shape1: List[vec], shape2: List[vec], direction: vec) -> vec:
    s1_furthestpoint = max(shape1, key=lambda point: point.dot(direction))
    s2_furthestpoint = max(shape2, key=lambda point: point.dot(-direction))
    support_point = s1_furthestpoint - s2_furthestpoint
    return support_point 


def is_collinear(*points: List['Point']) -> bool:
    if not all(isinstance(p, Point) for p in points):
        raise TypeError(f"'{type(p).__name__}' is invalid")
    if len(points) < 2: return True 
    return all([point.cross(points[(ind + 1) % len(points)]) == 0 for ind, point in enumerate(points)]) 