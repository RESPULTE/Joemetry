from joemetry._type_hints import *
from joemetry.utils import get_support
from joemetry import Polygon, Point


def GJK(shape1: Poly = None, shape2: Poly = None) -> bool:

	def handle_simplex(simplex: List[Point], direction: Point) -> bool:
		if len(simplex) == 2:
			return line_case(simplex, direction)
		return triangle_case(simplex, direction)

	def line_case(simplex: List[Point], direction: Point) -> bool:
		B, A = simplex
		AB, AO = (B - A), (-A)
		ABperp = AB.get_perpendicular(AO)
		direction.update(ABperp)
		return False

	def triangle_case(simplex: List[Point], direction: Point) -> bool:
		A, B, C = simplex
		AB, AC, AO = (B - A), (C - A), (-A)
		ABperp = AB.get_perpendicular(-AC)
		ACperp = AC.get_perpendicular(-AB)

		if ABperp.dot(AO) > 0: 	
			simplex.remove(C)
			direction.update(ABperp)
			return False

		elif ACperp.dot(AO) > 0: 
			simplex.remove(B)
			direction.update(ACperp)
			return False
			
		return True

	shape1, shape2 = Polygon(shape1), Polygon(shape2)
	direction = shape2.center - shape1.center
	simplex = [get_support(shape1, shape2, direction)]
	direction = -simplex[0]

	while True:

		support_point = get_support(shape1, shape2, direction)

		if direction.dot(support_point) < 0:
			return False

		simplex.append(support_point)

		if handle_simplex(simplex, direction):
			return True


