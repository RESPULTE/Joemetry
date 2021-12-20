from vector2D import Vector2D as vec
from typing import List, Tuple


Point = Tuple[int, int]


def ear_clipping(polygon: List[Point]) -> List[List[Point]]:
    if len(polygon) > 3:
        polygon = vec.convert(polygon)
        total_triangles = len(polygon) - 2

        triangles = []
        while len(triangles) < total_triangles:
            for ind, center_point in enumerate(polygon):
                right_point = polygon[(ind + 1) % len(polygon)]
                left_point  = polygon[(ind - 1) % len(polygon)] 

                if left_point.cross(right_point, origin=center_point) > 0: 
                    temp_triangle = (left_point, center_point, right_point)
                    check_triangle_validity = lambda point: point not in temp_triangle and point.in_polygon(temp_triangle)
    
                    if not any(filter(check_triangle_validity, polygon)):
                        triangles.append(temp_triangle)
                        polygon.pop(ind)

        return triangles

    return polygon

         

