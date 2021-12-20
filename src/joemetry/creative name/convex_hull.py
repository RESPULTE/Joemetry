from joemetry.intersection import *

from vector2D import Vector2D as vec
from typing import List, Tuple


Point = Tuple[int, int]


def monotone_chain(points: List[Point]) -> List[Point]:
    points = vec.convert(sorted(points))
    if len(points) > 3:

        # Build lower hull 
        lower_hull = []
        for point in points:
            # get the cross product between the current point that's being loop through 
            # with the last point that has been added 
            # with the second last point as the origin for the two points
            # if the cross product has value lower than or equal to 0 
            # the point that we're currently looking at is 'above' the last point that was added
            # keep popping the points in the list until the point in the list and the current point 
            # makes an anti-clockwise turn // the point in the list is higher/'above' the current point
            while len(lower_hull) >= 2 and lower_hull[-1].cross(point, origin=lower_hull[-2]) <= 0:
                lower_hull.pop()
            lower_hull.append(point)

        # Build upper hull
        upper_hull = []
        for point in reversed(points):
            while len(upper_hull) >= 2 and upper_hull[-1].cross(point, origin=upper_hull[-2]) <= 0:
                upper_hull.pop()
            upper_hull.append(point)

        # Concatenation of the lower and upper hulls gives the convex hull.
        # Last point of each list is omitted because it is repeated at the beginning of the other list. 
        return lower_hull[:-1] + upper_hull[:-1]

    return points


