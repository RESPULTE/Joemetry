from dataclasses import dataclass, field
from joemetry._type_hints import *
from .point import Point


# INTERSECT, STRETCHING(maybe?), translation?, CIRCLE
@dataclass
class Polygon:

    vertex: List[Union[tuple, Point]] = field(default_factory=list)


    def __post_init__(self):
        if len(self.vertex) < 3:
            raise TypeError(f'a polygon must consist of at least 3 points, dummy')
        self.vertex = [Point(*vertex) for vertex in self.vertex]


    @property
    def num_vertex(self) -> int: 
        return len(self.vertex)
    

    @property
    def area(self) -> float:
        '''returns the area of the polygon using the shoelacing equation'''
        area = 0
        for i in range(self.num_vertex):
            j = (i + 1) % self.num_vertex
            area += self.vertex[i].x * self.vertex[j].y
            area -= self.vertex[i].y * self.vertex[j].x
        return round(abs(area * 0.5), 2)


    @property
    def center(self) -> Point:
        '''returns the center of the polygon using the bounding box of it as reference'''
        bottomleft, topright = self.bounding_box
        center_x = bottomleft.x + ((topright.x - bottomleft.x) / 2)
        center_y = bottomleft.y + ((topright.y - bottomleft.y) / 2)
        return Point(center_x, center_y)


    @property
    def is_convex(self) -> bool:
        '''check whethr "this" polygon is a convex polygon'''
        if self.num_vertex == 3: 
            return True

        for ind, center_point in enumerate(self.vertex):
            center_to_right = self.vertex[(ind + 1) % self.num_vertex] 
            center_to_left  = self.vertex[(ind - 1) % self.num_vertex] 

            if center_to_left.cross(center_to_right, origin=center_point) < 0:
                return False 

        return True


    @property
    def bounding_box(self) -> Tuple[Point, Point]:
        x_coords   = [point.x for point in self.vertex]
        y_coords   = [point.y for point in self.vertex]
        topright   = max(x_coords), max(y_coords)
        bottomleft = min(x_coords), min(y_coords)
        return Point(*bottomleft), Point(*topright)


    @classmethod
    def convert(cls, polygons: List[List[Coor]]) -> List['Polygon']:
        '''convert a list of list of points into a list of polygons'''
        if not all(isinstance(c, (tuple, list)) for c in polygons):
            raise TypeError(f"the given data type must be tuples containing float/int")
        return [cls(poly) for poly in polygons]


    def add_vertex(self, point: Coor, index: Optional[int] = -1) -> None:
        '''adds a new vertex into the polygon with the given index'''
        self.vertex.insert(index, Point(*point)) 


    def pop_vertex(self, index: Optional[int] = -1) -> None:
        '''reomve a vertex from the polygon with the given index'''
        self.vertex.pop(index)


    def rotate(self, 
        angle: float, 
        origin: Optional[Coor] = (0,0),
        clockwise: Optional[bool] = True
        ) -> 'Polygon':
        '''
        returns a polygon that is rotated to the given angle
        angle: 0-360 degree
        origin: relative origin for the roatation
        clockwise: it's pretty self-explanatory, init?
        '''
        return Polygon([point.rotate(angle, origin, clockwise) for point in self.vertex])


    def rotate_ip(self, 
        angle: float, 
        origin: Optional[Coor] = (0,0),
        clockwise: Optional[bool] = True
        ) -> None:
        '''
        rotates this polygon to the given angle
        angle: 0-360 degree
        origin: relative origin for the roatation
        clockwise: it's pretty self-explanatory, init?
        '''
        [point.rotate_ip(angle, origin, clockwise) for point in self.vertex]


    def enlarge(self, scale_factor: Num):
        '''enlarge/shrink "this" polygon by the given scale factor'''
        self.vertex = [point * scale_factor for point in self.vertex]


    def enlarge_to(self, target_area: Num):
        '''enlarge/shrink "this" polygon to the given area'''
        ...

    def __mul__(self, scale_factor: Num):
        '''enlarge/shrink "this" polygon by the given scale factor'''
        if not isinstance(scale_factor, (float, int)):
            raise TypeError(f"cannot multiply {type(self).__name__} by '{type(scale_factor).__name__}'")
        return Polygon([point * scale_factor for point in self.vertex])


    def __truediv__(self, scale_factor: Num):
        '''enlarge/shrink "this" polygon by the given scale factor'''
        if not isinstance(scale_factor, (float, int)):
            raise TypeError(f"cannot divide {type(self).__name__} by '{type(scale_factor).__name__}'")
        return Polygon([point / scale_factor for point in self.vertex])


    def __floordiv__(self, scale_factor: Num):
        '''enlarge/shrink "this" polygon by the given scale factor'''
        if not isinstance(scale_factor, (float, int)):
            raise TypeError(f"cannot divide(floor) {type(self).__name__} by '{type(scale_factor).__name__}'")
        return Polygon([point // scale_factor for point in self.vertex])


    def __iter__(self):
        return iter((self.vertex))


    def __getitem__(self, index):
        return self.vertex[index]


    def __setitem__(self, index, value):
        self.vertex[index] = Point(*value)


