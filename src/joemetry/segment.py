from dataclasses import dataclass
from joemetry._type_hints import *
from .point import *


@dataclass
class Segment:

    __slots__ = ['start', 'end']

    start: Point
    end: Point


    def __post_init__(self):
        self.start = Point(*self.start)
        self.end   = Point(*self.end)


    @property
    def slant(self) -> float:
        '''
        Y = mX + C
        pretty sure that you're familiar with this equation
        this returns the "m" inside of the equation
        '''
        return round((self.start.y - self.end.y) / (self.start.x - self.end.x), 2)
    

    @property
    def _length(self) -> float:
        # this is the 'real' length of the point, used for computation in order to maximize accuracy
        return sqrt((self.start.x - self.end.x)**2 + (self.start.y - self.end.y)**2)


    @property
    def length(self) -> float:
        # this is the 'fake' length of the point, displayed when printed
        return round(self._length, 2)


    @property
    def midpoint(self) -> 'Point':
        '''returns the midpoint of "this" segment'''
        return Point((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2)


    @property
    def unit_vector(self) -> 'Point':
        '''returns a normalized segment'''
        return (self.end - self.start) / self._length
    

    @classmethod
    def convert(cls, segments: List[Tuple[Coor, Coor]]) -> List['Segment']:
        '''converts either a list of tuple of point objects or a list of tuple of tuple of 2 float into segment objects'''
        if not all(isinstance(c, (tuple, list)) for c in segments):
            raise TypeError(f"the given data type must be tuples containing float/int")
        return [cls(*seg) for seg in segments]


    def perpendicular_with(self, other: 'Segment') -> bool:
        '''
        check whether "this" segment is perpendicular with the other segment
        uses the [m1 x m2 = -1] equation
        '''
        return (self.slant * other.slant) == -1 


    def parallel_with(self, other: 'Segment') -> bool:
        '''
        check whether "this" segment is parallel with the other segment
        '''
        return self.slant == other.slant


    def collinear_with(self, other: 'Segment') -> bool:
        '''
        check whether "this" segment is collinear with the other segment
        uses the cross-product of both ends of the segments
        '''
        return self.start.cross(other.start) == self.end.cross(other.end) == 0


    def scale_to_length(self, length: Num, direction='mid') -> None:
        '''
        extend or contract "this" segment to the given length
        direction: valid options -> "start", "mid", "end"
                   "start": extend/contract the segment at the starting point only
                   "end": extend/contract the segment at the ending point only
                   "mid": extend/contract the segment at the starting point and ending point equally

        '''
        if direction not in ['start', 'mid', 'end']:
            raise ValueError(f"{direction} is not a valid direction")
        scale_factor  = self.unit_vector * (length - self._length)
        plus_start = plus_end = scale_factor
        if direction == 'mid':
            plus_start = plus_end = scale_factor * 0.5
        elif direction == 'start':
            plus_end = (0, 0)
        elif direction == 'end':
            plus_start = (0, 0)

        self.start -= plus_start
        self.end   += plus_end


    def rotate(self, 
        angle: Num, 
        origin: Optional[Coor] = (0,0),
        clockwise: Optional[bool] = True
        ) -> 'Segment':
        '''
        returns a segment that is rotated to the given angle
        angle: 0-360 degree
        origin: relative origin for the roatation
        clockwise: it's pretty self-explanatory, init?
        '''
        return Segment(self.start.rotate(angle, origin, clockwise), self.end.rotate(angle, origin, clockwise))


    def rotate_ip(self, 
        angle: Num, 
        origin: Optional[Coor] = (0,0),
        clockwise: Optional[bool] = True
        ) -> None:
        '''
        rotates this segment to the given angle
        angle: 0-360 degree
        origin: relative origin for the roatation
        clockwise: it's pretty self-explanatory, init?
        '''
        self.start.rotate_ip(angle, origin, clockwise)
        self.end.rotate_ip(angle, origin, clockwise)


    def intersect_with(self, other: 'Segment') -> Coor:
        '''
        returns either None or an intersecting point of both segment 
        '''
        start = other.start - self.start
        end_1, end_2 = self.end - self.start, other.end - other.start

        determinant = end_1.cross(end_2)
        if determinant == 0: return None

        check_1 = (start).cross(end_2) / determinant
        check_2 = (start).cross(end_1) / determinant

        if (0 <= check_1 <= 1) and (0 <= check_2 <= 1):
            return round(self.start + (self.end - self.start) * check_1, 2)

        return None


    def __mul__(self, scale_factor: Num):
        '''contract/extend the segment's length by the given scale factor'''
        if not isinstance(scale_factor, (float, int)):
            raise TypeError(f"cannot multiply {type(self).__name__} by '{type(scale_factor).__name__}'")
        return Segment(self.start * scale_factor, self.end * scale_factor)


    def __truediv__(self, scale_factor: Num):
        '''contract/extend the segment's length by the given scale factor'''
        if not isinstance(scale_factor, (float, int)):
            raise TypeError(f"cannot divide {type(self).__name__} by '{type(scale_factor).__name__}'")
        return Segment(self.start / scale_factor, self.end / scale_factor)


    def __floordiv__(self, scale_factor: Num):
        '''contract/extend the segment's length by the given scale factor'''
        if not isinstance(scale_factor, (float, int)):
            raise TypeError(f"cannot divide(floor) {type(self).__name__} by '{type(scale_factor).__name__}'")
        return Segment(self.start // scale_factor, self.end // scale_factor)


    def __getitem__(self, index: int) -> 'Point':
        if index == 0: return self.start
        if index == 1: return self.end


    def __setitem__(self, index: int, val: Coor) -> Num:
        if index == 0: self.start = Point(*val)
        if index == 1: self.end = Point(*val)

