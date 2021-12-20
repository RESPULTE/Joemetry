from dataclasses import dataclass, field
from joemetry import Segment
from joemetry._type_hints import *


@dataclass
class PointType:

    sort_index: int 
    position: Tuple[int, int] 


    def __gt__(self, other):
        if self.sort_index == other.sort_index:

            if self.position == other.position:

                if isinstance(self, StartingPointType):
                    return self.line[1][1] > other.line[1][1]

                elif isinstance(self, EndingPointType):
                    return self.line[0][1] > other.line[0][1]

                else:
                    # if the point being compared is an intersecting point 
                    # always return True, i.e always make the point comes after the ending/starting type point
                    # make the operations a lil bit more efficient, since this can avoid evaluating the same point twice
                    return True

            return self.position > other.position

        elif self.sort_index > other.sort_index:
            return True


    def __lt__(self, other):
        if self.sort_index == other.sort_index:

            if self.position == other.position:
                if isinstance(self, StartingPointType):
                    return self.line[1][1] < other.line[1][1]
                elif isinstance(self, EndingPointType):
                    return self.line[0][1] < other.line[0][1]
                else:
                    # if the point being compared is an intersecting point 
                    # always return True, i.e always make the point comes after the ending/starting type point
                    # make the operations a lil bit more efficient, since this can avoid evaluating the same point twice
                    return False

            return self.position < other.position

        elif self.sort_index < other.sort_index:
            return True


@dataclass
class StartingPointType(PointType):

    line: Segment


@dataclass
class EndingPointType(PointType):

    line: Segment


@dataclass
class IntersectingPointType(PointType): 

    points: Tuple[PointType, PointType]
