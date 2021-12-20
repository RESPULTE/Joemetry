from typing import List, Tuple, Union, Optional, TypeVar


Num  = Union[float, int]


Coor = TypeVar('Coor', Tuple[Num, Num], 'Point')


Seg  = TypeVar('Seg', Tuple[Coor, Coor], 'Segment')


Poly = TypeVar('Poly', List[Coor], 'Polygon')

