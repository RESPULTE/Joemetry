from typing import List, Tuple, Optional, Union
from dataclasses import dataclass, field
from vector2D import Vector2D as vec


@dataclass
class Point:

    sort_index: int 
    position: Tuple[int, int] 


    def __gt__(self, other):
        if self.sort_index == other.sort_index:

            if self.position == other.position:

                if isinstance(self, StartingPoint):
                    return self.line[1][1] > other.line[1][1]

                elif isinstance(self, EndingPoint):
                    return self.line[0][1] > other.line[0][1]

                else:
                    # if the point being compared is an intersecting point 
                    # always return True, i.e always make the point comes after the ending/starting type point
                    # make the operations a lil bit more efficient, since this can avoid evaluating the same point twice
                    return True


            # TO BE CHANGED AFTER THE VECTOR CLASS IS FIXED
            elif self.sort_index == self.position[0]:
                return self.position[1] > other.position[1]

            elif self.sort_index == self.position[1]:
                return self.position[0] > other.position[0]

        elif self.sort_index > other.sort_index:
            return True


    def __lt__(self, other):
        if self.sort_index == other.sort_index:

            if self.position == other.position:
                if isinstance(self, StartingPoint):
                    return self.line[1][1] < other.line[1][1]
                elif isinstance(self, EndingPoint):
                    return self.line[0][1] < other.line[0][1]
                else:
                    # if the point being compared is an intersecting point 
                    # always return True, i.e always make the point comes after the ending/starting type point
                    # make the operations a lil bit more efficient, since this can avoid evaluating the same point twice
                    return False

            elif self.sort_index == self.position[0]:
                return self.position[1] < other.position[1]

            elif self.sort_index == self.position[1]:
                return self.position[0] < other.position[0]

        elif self.sort_index < other.sort_index:
            return True


@dataclass
class StartingPoint(Point):

    line: Tuple[vec, vec] 


@dataclass
class EndingPoint(Point):

    line: Tuple[vec, vec]


@dataclass
class IntersectingPoint(Point): 

    points: Tuple[Tuple[vec, vec]] 
