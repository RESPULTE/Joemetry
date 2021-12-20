from math import sin, cos, radians, sqrt, ceil, floor, acos
from dataclasses import dataclass
from joemetry._type_hints import *


@dataclass
class Point:

    __slots__ = ['x', 'y']

    x: float 
    y: float 


    def __post_init__(self):
        # using the built-in float as a type checker
        self.x = float(self.x)
        self.y = float(self.y)


    @property
    def _length(self):
        # this is the 'real' length of the point, used for computation in order to maximize accuracy
        return sqrt((self.x * self.x) + (self.y * self.y))


    @property
    def length(self):
        # this is the 'fake' length of the point, displayed when printed
        return round(self._length, 2)
    

    @classmethod
    def convert(cls, coordinates: List[Coor]) -> List['Point']:
        '''convert a list of tuple into Points'''
        if not all(isinstance(c, tuple) for c in coordinates):
            raise TypeError(f"the given data type must be tuples containing float/int")
        return [cls(*point) for point in coordinates]


    def astuple(self) -> tuple:
        return (self.x, self.y)


    def update(self, other: Coor) -> None:
        self.x, self.y = other[0], other[1]


    def scale_to_length(self, length: float) -> None:
        '''reposition the point to match the given length'''
        if self.x == 0 and self.y == 0: return 
        ratio = length / self._length
        self.x *= ratio
        self.y *= ratio


    def normalize(self) -> 'Point':
        '''return a point that's converted to unit vector'''
        if self.x != 0 and self.y != 0:
            return Point(self.x / self._length, self.y / self._length)
        return Point(0,0)


    def normalize_ip(self) -> None:
        '''convert the point in-use into unit vectors'''
        if self.x == 0 and self.y == 0: return 
        self.x /= self._length
        self.y /= self._length


    def cross(self, other: Coor, origin: Optional[Coor] = (0, 0)) -> float:
        '''
        returns the cross product of betweeen 'this' point and another point
        origin: use this tuple/point object as the relative origin of both point
        '''
        x1, y1 = (self.x - origin[0]), (self.y - origin[1])
        x2, y2 = (other[0] - origin[0]), (other[1] - origin[1])  
        return (x1 * y2) - (y1 * x2)


    def dot(self, other: Coor, origin: Optional[Coor] = (0, 0)) -> float:
        '''
        returns the dot product of betweeen 'this' point and another point
        origin: use this tuple/point object as the relative origin of both point
        '''
        x1, y1 = (self.x - origin[0]), (self.y - origin[1])
        x2, y2 = (other[0] - origin[0]), (other[1] - origin[1])     
        return (x1 * x2) + (y1 * y2)


    # TO BE FIXED
    def get_perpendicular(self, ref_point: Coor) -> 'Point':
        '''
        get the point that is perpendicular to "this" point
        ref_point: use this to get the desired perpendicular point ('up' or 'down')
        '''
        perpendicular_line = Point(self.y, -self.x)
        if perpendicular_line.dot(ref_point) < 0:
            perpendicular_line *= -1
        return perpendicular_line


    def rotate(self, 
        angle    : Num, 
        origin   : Optional[Coor] = (0,0),
        clockwise: Optional[bool] = True
        ) -> 'Point':
        '''
        returns a point that is rotated to the given angle
        angle: 0-360 degree
        origin: relative origin for the roatation
        clockwise: it's pretty self-explanatory, init?
        '''
        # formula:
        #  let r = length of the vector
        #  rotated_x = r[cos(original_angle + new_angle)]
        #            = r * [cos(original_angle)cos(new_angle) - sin(original_angle)sin(new_angle)]
        #            = (original_x)(cos(new_angle)) - (original_y)(sin(new_angle))
        #
        #  rotated_y = r[sin(original_angle + new_angle)]
        #            = r * [sin(original_angle)cos(new_angle) + cos(originl_angle)sin(new_angle)]
        #            = (original_y)(cos(new_angle)) + (original_x)(sin(new_angle))
        #
        # translated -> original (in this case)
        angle  = radians(angle)
        cosine, sine = cos(angle), sin(angle)
        translated_x = self.x - origin[0]
        translated_y = self.y - origin[1]

        dx = origin[0] + (translated_x * cosine - translated_y * sine)
        dy = origin[1] + (translated_y * cosine + translated_x * sine)

        return Point(dx, dy) * -1 if clockwise else Point(dx, dy)


    def rotate_ip(self, 
        angle    : Num, 
        origin   : Optional[Coor] = (0,0),
        clockwise: Optional[bool] = True
        ) -> None:
        '''
        rotates 'this' point to the given degree
        angle: 0-360 degree
        origin: relative origin for the roatation
        clockwise: it's pretty self-explanatory, init?
        '''
        # formula:
        #  let r = length of the vector
        #  rotated_x = r[cos(original_angle + new_angle)]
        #            = r * [cos(original_angle)cos(new_angle) - sin(original_angle)sin(new_angle)]
        #            = (original_x)(cos(new_angle)) - (original_y)(sin(new_angle))
        #
        #  rotated_y = r[sin(original_angle + new_angle)]
        #            = r * [sin(original_angle)cos(new_angle) + cos(originl_angle)sin(new_angle)]
        #            = (original_y)(cos(new_angle)) + (original_x)(sin(new_angle))
        #
        # translated -> original (in this case)
        angle        = radians(angle) * -1 if clockwise else radians(angle)
        cosine, sine = cos(angle), sin(angle)
        translated_x = self.x - origin[0]
        translated_y = self.y - origin[1]

        dx = origin[0] + (translated_x * cosine - translated_y * sine)
        dy = origin[1] + (translated_y * cosine + translated_x * sine)

        self.x, self.y = dx, dy


    def angle_to(self, 
        other    : Coor, 
        origin   : Optional[Coor] = (0,0), 
        clockwise: Optional[bool] = False,
        ) -> float:
        '''
        returns the angle that is formed between "this" point and the given point
        other: a point object/ a tuple of 2 float
        origin: relative origin for computation
        clockwise: it's pretty self-explanatory, init?
        '''
        origin_to_point1 = self  - origin
        origin_to_other  = other - origin

        scalar  = origin_to_point1.dot(origin_to_other)
        length1 = origin_to_point1.length
        length2 = origin_to_other.length

        angle = round(acos(scalar / (length1 * length2)) * 180 / 3.142, 2)   

        return angle * -1 if clockwise else angle


    def in_polygon(self, polygon: List[Coor]) -> bool:
        '''
        returns a True if "this" point is inside of a polygon and vice versa
        uses the cross product to determine the whereabouts of the point
        '''
        if self in polygon: 
            return True
        total_vertex = len(polygon)
        cross_check  = [(polygon[(ind + 1) % total_vertex]).cross(self, origin=point) for ind, point in enumerate(polygon)]
        return all(map(lambda cross_product: cross_product <= 0, cross_check))


    def in_circle(self, center: Coor, radius: float) -> bool:
        '''
        returns a True if "this" point is inside of a circle and vice versa
        '''
        dx, dy = abs(self - center)

        if dy <= radius and dx <= radius:  return True
        if dy + dx <= radius:              return True
        if dx*dx + dy*dy <= radius*radius: return True

        return False


    def __add__(self, other: Coor):
        if isinstance(other, (type(self), tuple)):
            return Point(self.x + other[0], self.y + other[1])
        raise TypeError(f'addition with an invalid type: {type(other)}!')


    def __sub__(self, other: Coor):
        if isinstance(other, (type(self), tuple)):
            return Point(self.x - other[0], self.y - other[1])
        raise TypeError(f'subtraction with an invalid type: {type(other)}!')


    def __mul__(self, val: Num):
        '''contract/extend the point's position by the given scale factor'''
        if not isinstance(val, (float, int)):
            raise TypeError(f"cannot multiply {type(self).__name__} by '{type(val).__name__}'")
        return Point(self.x * val, self.y * val)


    def __truediv__(self, val: Num):
        '''contract/extend the point's position by the given scale factor'''
        if not isinstance(val, (float, int)):
            raise TypeError(f"cannot divide {type(self).__name__} by '{type(val).__name__}'")
        return Point(self.x / val, self.y / val)


    def __floordiv__(self, val: Num):
        '''contract/extend the point's position by the given scale factor'''
        if not isinstance(val, (float, int)):
            raise TypeError(f"cannot divide(floor) {type(self).__name__} by '{type(val).__name__}'")
        return Point(self.x // val, self.y // val)


    def __round__(self, ndigits: int) -> 'Point':
        return Point(round(self.x, ndigits), round(self.y, ndigits))


    def __invert__(self) -> 'Point':
        return Point(self.y, self.x)


    def __abs__(self) -> 'Point':
        return Point(abs(self.x), abs(self.y))


    def __neg__(self) -> 'Point':
        return Point(self.x * -1, self.y * -1)


    def __pos__(self):
        return Point(self.x, self.y)


    def __iter__(self):
        return iter((self.x, self.y))


    def __ceil__(self) -> 'Point':
        return Point(ceil(self.x), ceil(self.y))


    def __floor__(self) -> 'Point':
        return Point(int(floor(self.x)), int(floor(self.y)))


    def __getitem__(self, index: int) -> Num:
        if index == 0: return self.x
        if index == 1: return self.y


    def __setitem__(self, index: int, val: Num) -> None:
        if index == 0: self.x = val
        if index == 1: self.y = val


    def __copy__(self):
        point = type(self)(self.x, self.y)
        point.__dict__.update(self.__dict__)
        return point


    def __repr__(self):
        return f"Point(x={round(self.x, 2)}, y={round(self.y, 2)})"

