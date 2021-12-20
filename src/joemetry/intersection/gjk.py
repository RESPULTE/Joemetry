from vector2D import Vector2D as vec
from typing import List, Tuple, Optional
from utility import get_center, get_support


Polygon = List[Tuple[int, int]]



def GJK(shape1: Polygon = None, shape2: Polygon = None) -> bool:
	shape1, shape2 = vec.convert(shape1), vec.convert(shape2)
	center1, center2 = get_center(shape1), get_center(shape2)
	direction = center2 - center1

	simplex = [get_support(shape1, shape2, direction)]
	direction = -simplex[0]

	while True:

		support_point = get_support(shape1, shape2, direction)

		if direction.dot(support_point) < 0:
			return False

		simplex.append(support_point)

		if handle_simplex(simplex, direction):
			return True


def handle_simplex(simplex: List[vec], direction: vec) -> bool:
	if len(simplex) == 2:
		return line_case(simplex, direction)
	return triangle_case(simplex, direction)


def line_case(simplex: List[vec], direction: vec) -> bool:
	point_b, point_a    = simplex
	a_to_b, a_to_origin = (point_b - point_a), (-point_a)
	abperp = a_to_b.get_perpendicular(a_to_origin)
	direction.update(abperp)
	return False


def triangle_case(simplex: List[vec], direction: vec) -> bool:
	point_a, point_b, point_c   = simplex
	a_to_b, a_to_c, a_to_origin = (point_b - point_a), (point_c - point_a), (-point_a)
	abperp = a_to_b.get_perpendicular(a_to_c)
	acperp = a_to_c.get_perpendicular(a_to_b)

	if abperp.dot(a_to_origin) > 0: 
		simplex.remove(point_c)
		direction.update(abperp)
		return False

	elif acperp.dot(a_to_origin) > 0: 
		simplex.remove(point_b)
		direction.update(acperp)
		return False
		
	return True