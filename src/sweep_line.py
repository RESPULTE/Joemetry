from typing import List, Tuple, Optional
from dataclasses import dataclass, field
from functools import total_ordering
from binarytree import AVL
from vector2D import Vector2D as vec
from utility import get_intersect


Coordinate = Tuple[int, int]

@total_ordering
@dataclass
class Event:

    sort_index: int 
    position: Tuple[int, int]

    def __gt__(self, other):
        if self.sort_index > other.sort_index:
            return True
        elif self.sort_index == other.sort_index:
            if self.sort_index == self.position[0]:
                return self.position[1] > other.position[1]
            elif self.sort_index == self.position[1]:
                return self.position[0] < other.position[0]

@dataclass
class StartingEvent(Event):

    line: Tuple[vec, vec] = field(compare=False)


@dataclass
class EndingEvent(Event):

    line: Tuple[vec, vec] = field(compare=False)


@dataclass
class IntersectingEvent(Event): 

    segment: Tuple[Tuple[vec, vec]] = field(compare=False)


def sweep_line(
    lines:   List[Tuple[Coordinate, Coordinate]], 
    getLine: Optional[bool]=False
    ) -> List[Coordinate]:
    
    # data structure for storing all the points
    activeQueue, eventQueue = AVL(), AVL()

    # store the intersected lines & points
    intersected_points   = set()
    intersected_segments = []

    # initialize the event queue with the x-axis as the key
    for line in lines:
        vec_line   = vec.convert(line)
        eventQueue.insert(StartingEvent(line[0][0], line[0],vec_line))
        eventQueue.insert(EndingEvent(line[1][0], line[1], vec_line))

    while not eventQueue.isempty:

        # get the minimum line_segment from the event queue 
        # change the sort index of the line segment to be based on y-axis
        curr_event = eventQueue.pop(key='min')

        # get the line segment that is 'above' or 'below' the current segment, based on the y-axis
        below_segment = activeQueue.find_lt(curr_event)
        above_segment = activeQueue.find_gt(curr_event)

        # if the current segemnt hasn't been added to the active queue
        if isinstance(curr_event, StartingEvent):

            curr_event.sort_index = curr_event.position[1]
            
            activeQueue.insert(curr_event)

            # if there's a segment below the current segemnt, check if they intersect
            if above_segment:
                above_intersection = get_intersect(curr_event.line, above_segment.line)
                if above_intersection:
                    eventQueue.insert(IntersectingEvent(above_intersection[0], above_intersection.astuple, (above_segment, curr_event)))

            # if there's a segment above the current segemnt, check if they intersect
            if below_segment:
                below_intersection = get_intersect(curr_event.line, below_segment.line)
                if below_intersection:
                    eventQueue.insert(IntersectingEvent(below_intersection[0], below_intersection.astuple, (curr_event, below_segment)))

        # if the sweep line has reached the end of a line segment
        elif isinstance(curr_event, EndingEvent):

            # check whather the line segment that's below and above it intersect
            if below_segment and above_segment:
                above_below_intersection = get_intersect(above_segment.line, below_segment.line)

                if above_below_intersection:
                    eventQueue.insert(IntersectingEvent(above_below_intersection[0], above_below_intersection.astuple, (above_segment, below_segment)))

            for node in activeQueue:
                if node.value.line == curr_event.line:
                    activeQueue.delete(node.value)

        elif isinstance(curr_event, IntersectingEvent):

            upper_intersected_segment = max(curr_event.segment)
            lower_intersected_segment = min(curr_event.segment)
            
            above_above_segment = activeQueue.find_gt(upper_intersected_segment)
            below_below_segment = activeQueue.find_lt(lower_intersected_segment)

            upper_intersected_segment.line, lower_intersected_segment.line = lower_intersected_segment.line, upper_intersected_segment.line
            
            if above_above_segment:
                upper_intersection = get_intersect(above_above_segment.line, upper_intersected_segment.line)
                if upper_intersection:
                    eventQueue.insert(IntersectingEvent(upper_intersection[0], upper_intersection.astuple, (above_above_segment, lower_intersected_segment)))

            if below_below_segment:
                lower_intersection = get_intersect(below_below_segment.line, lower_intersected_segment.line)
                if lower_intersection:
                    eventQueue.insert(IntersectingEvent(lower_intersection[0], lower_intersection.astuple, (below_below_segment, upper_intersected_segment)))

            intersected_points.add(curr_event.position)

    return (intersected_points, intersected_segments) if getLine else intersected_points


a = [[(1, 5), (4, 5)], [(2, 5), (10, 1)], [(3, 2), (10, 3)], [(6, 4), (9, 4)], [(7, 1), (8, 1)], [(5, 0), (7, 10)]]
a, b = sweep_line(a, getLine=True)
print(a)
