from binarytree import AVL
from joemetry import Segment, Point
from joemetry._type_hints import *
from ._point_type import StartingPointType, EndingPointType, IntersectingPointType


class CheckSegmentIntersection:
    '''
        - a basic sweep line algorithm to detect intersection in n-number of lines

        [INPUT]: 

            lines -> a list of lines in the form like this:
                     [[(1, 1), (2, 1)], [(3, 3), (4, 1)]]
                     |    line 1    |  |    line 2     |
                 
            getLine -> will return all the intersecting lines if set to True

        [PROCESS]:
            
            1) convert all the lines given into 2D-vector for easier management

            2) populate the 'eventQueue' with the vectorized line, using the x-axis of point as the sort index
               -> this includes both the starting and ending point of the line

            3) enter and while loop and get the minimum value/point from the eventQueue
            
            4) check the type of the point

               i) if the point is a starting point:
                  - change the sort index of the point to be based on the y-axis

                  - get the closest point that is above and below the point

                  - check whether both the upper and lower point interscect with the point
                    -> add it to the 'eventQueue' if it does

                  - insert it into the 'activeQueue'

               ii) if the point is an ending point:
                  - get the closest point that is above and below the point

                  - check whether the upper point and the lower point intersect with each other
                    -> add it to the 'eventQueue' if it does

                  - delete the line from the 'activeQueue'

               iii) if the point is an intersecting point:
                  - determine which point is above and which point is down
                    -> using their starting point as comparison

                  - get the line that is above the upper point and the line that is below the lower point //
                    get the 'other neighbour' for both of those points

                  - swap the line/sort index of the upper and lower point

                  - check whether the original upper point's line and the lower point's neighbour's line intersects
                    -> add it to the 'eventQueue' if it does

                  - check whether the original lower point's line and the upper point's neighbour's line intersects
                    -> add it to the 'eventQueue' if it does

                  - record the intersecting point & intersecting lines

            5) repeat/loop until the 'eventQueue' is empty
    '''

    def __new__(cls,
        lines: S, 
        getLine: Optional[bool]=False
        ) -> Union[List[C], List[S], None]:
        return super().__new__(cls)(lines, getLine)


    def __call__(self, 
        lines: S, 
        getLine: Optional[bool]=False
        ) -> Union[List[C], List[S], None]:

        # data structure for storing all the points
        # activeQueue: y-axis sorted
        # eventQueue:  x-axis sorted
        self.eventQueue  = AVL()
        self.activeQueue = AVL()

        # store the intersected lines & points
        self.intersected_points = set()
        self.intersected_lines  = []

        # initialize the event queue with the x-axis as the sorting index
        for line in lines:
            vec_line = Segment(*line)
            self.eventQueue.insert(StartingPointType(line[0][0], line[0],vec_line))
            self.eventQueue.insert(EndingPointType(line[1][0], line[1], vec_line))

        return self.sweep(getLine)


    def sweep(self, getLine: Optional[bool]=False) -> Union[List[C], List[S], None]:
        while not self.eventQueue.isempty:

            current_point = self.eventQueue.pop(key='min')
            # change the sorting index to y-axis 
            # -> to get the correct set of points when it's passed into the activeQueue 
            current_point.sort_index = current_point.position[1]
        
            if not isinstance(current_point, IntersectingPointType):

                # get the point that is 'above' or 'below' the current point, based on the y-axis
                lower_point = self.activeQueue.find_lt(current_point)
                upper_point = self.activeQueue.find_gt(current_point)

                if isinstance(current_point, StartingPointType):
                    self.handle_starting_point(current_point, upper_point, lower_point)
                    continue

                self.handle_ending_point(current_point, upper_point, lower_point)
                continue

            self.handle_intersecting_point(current_point)
            continue

        if self.intersected_points != set():
            return (self.intersected_points, self.intersected_lines) if getLine else self.intersected_points

        return None
        

    def handle_starting_point(self, current_point, upper_point, lower_point):
        # if there's a segment below the current point, check if they intersect
        if upper_point:
            intersect_up = current_point.line.intersect_with(upper_point.line)
            if intersect_up:
                self.eventQueue.insert(IntersectingPointType(intersect_up[0], intersect_up.astuple(), (upper_point, current_point)))

        # if there's a segment above the current point, check if they intersect
        if lower_point:
            intersect_down = current_point.line.intersect_with(lower_point.line)
            if intersect_down:
                self.eventQueue.insert(IntersectingPointType(intersect_down[0], intersect_down.astuple(), (current_point, lower_point)))

        self.activeQueue.insert(current_point)


    def handle_ending_point(self, current_point, upper_point, lower_point):
        # check whather the line segment that's below and above it intersect
        if lower_point and upper_point:
            intersect_up_down = upper_point.line.intersect_with(lower_point.line)

            if intersect_up_down:
                self.eventQueue.insert(IntersectingPointType(intersect_up_down[0], intersect_up_down.astuple(), (upper_point, lower_point)))

        # remove the node with the line segment from the activeQueue 
        # doing it like this since the 'owner' of the line is swapped for each intersection point
        # ____________________________________________________________________________
        # might change this, add it as a feature or something in the delete method
        for node in self.activeQueue:
            if node.value.line == current_point.line:
                self.activeQueue.delete(node.value)


    def handle_intersecting_point(self, current_point):
        # get the upper and lower point of the intersection
        up_point   = max(current_point.points)
        down_point = min(current_point.points)

        self.intersected_points.add(current_point.position)
        self.intersected_lines.append((up_point.line, down_point.line))

        # get the neighbour of both of those points
        # -> the point that is even higher than the upper point
        # -> the point that is even lower thatn the upper point
        neigh_up   = self.activeQueue.find_gt(up_point)
        neigh_down = self.activeQueue.find_lt(down_point)

        # swap the line of the two intersecting points
        up_point.line, down_point.line = down_point.line, up_point.line
        
        # check whether lower point's line intersects with the line of neighbour of upper point 
        if neigh_up:
            intersect_up = neigh_up.line.intersect_with(up_point.line)
            if intersect_up:
                self.eventQueue.insert(IntersectingPointType(intersect_up[0], intersect_up.astuple(), (neigh_up, down_point)))
        
        # check whether upper point's line intersects with the line of neighbour of lower point 
        if neigh_down:
            intersect_down = neigh_down.line.intersect_with(down_point.line)
            if intersect_down:
                self.eventQueue.insert(IntersectingPointType(intersect_down[0], intersect_down.astuple(), (neigh_down, up_point)))
