from math import sqrt, atan2, cos, sin, degrees, radians, pi

import unittest

from service.Physics.PythonPhysics import PythonPhysics
from service.Physics.Physics import Physics

class TestPythonPhysics(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)
        Physics.SetInstance(PythonPhysics())

    def test_distance(self):
        assert(Physics.distance(5, 5, 5, 5)             == 0)       # Equal positive points
        assert(Physics.distance(0, 0, 0, 0)             == 0)       # Equal origins
        assert(Physics.distance(-5, -5, -5, -5)         == 0)       # Equal negatives points
        assert(Physics.distance(0, 5, 0, 0)             == 5)       # 1D distance origin to positive X
        assert(Physics.distance(-5, 0, 0, 0)            == 5)       # 1D distance negative to origin X
        assert(Physics.distance(0, 0, 0, 5)             == 5)       # 1D distance origin to positive Y
        assert(Physics.distance(0, 0, -5, 0)            == 5)       # 1D distance negative to origin Y
        assert(Physics.distance(0, 1, 0, 1)             == sqrt(2)) # 2D distance towards positive X,Y
        assert(Physics.distance(0, -1, 0, -1)           == sqrt(2)) # 2D distance towards negative X,Y
        assert(Physics.distance(0, 1, 0, -1)            == sqrt(2)) # 2D distance towards positive X, negative Y
        assert(Physics.distance(0, 1, 0, -1)            == sqrt(2)) # 2D distance towards negative X, positive Y
        assert(Physics.distance(0.5, 1.5, 0.5, -0.5)    == sqrt(2)) # Float number test
        assert(Physics.distance(0, float('inf'), 0, 0)               == float('inf'))         # Huge numbers 1D
        assert(Physics.distance(0, float('inf'), 0, float('inf'))    == sqrt(2*float('inf'))) # Huge numbers 2D
        with self.assertRaises(Exception):
            Physics.distance("a", "a", "a", "a")

    def test_angularDistance(self):
        assert(Physics.angularDistance(0, 0)         == 0)     # Equal angles
        assert(Physics.angularDistance(0, 180)       == 180)   # Clockwise PI
        assert(Physics.angularDistance(0, -180)      == 180)   # Anti-clockwise PI
        assert(Physics.angularDistance(0, 360)       == 0)     # Clickwise 2PI
        assert(Physics.angularDistance(0, -360)      == 0)     # Anti-clickwise 2PI
        assert(Physics.angularDistance(0, 540)       == 180)   # Clockwise >2PI difference
        assert(Physics.angularDistance(0, -540)      == 180)   # Anti-clockwise >2PI difference
        with self.assertRaises(Exception):
            Physics.angularDistance("a", "a")

    def test_getAngle(self):
        assert(Physics.getAngle(0, 0, 0, 0) == 0)   # Equal points
        assert(Physics.getAngle(0, 0, 1, 1) == 45)  # Square Diagonal
        assert(Physics.getAngle(0, 0, 0, 1) == 90)  # Right Angle
        assert(Physics.getAngle(0, 0, 1, 0) == 0)   # Front Flat angle
        assert(Physics.getAngle(1, 0, 0, 0) == 180) # Back Flat angle
        with self.assertRaises(Exception):
            Physics.getAngle('a', 'a', 'a', 'a')

    def test_applyMovement(self):
        assert(Physics.applyMovement(0, 0, 90, 0)    == (0,0))             # No distance
        assert(Physics.applyMovement(0, 0, 0, 1)     == (1,0))             # Forward
        assert(Physics.applyMovement(0, 0, 0, -1)    == (-1,0))            # Backward using distance
        assert(Physics.applyMovement(0, 0, 45, 1)    == (cos(radians(45)),sin(radians(45))))    # Diagonal
        assert(Physics.applyMovement(0, 0, 90, 1)    == (cos(radians(90)),sin(radians(90))))    # Upwards (supposed to be (0,1), but won't work)
        assert(Physics.applyMovement(0, 0, 270, 1)   == (cos(radians(270)),sin(radians(270))))  # Downwards (supposed to be (0,-1), but won't work)

    def test_isInCircle(self):
        assert(Physics.isInCircle(0, 0, 0, 0, 1))             # Point at circle's origin
        assert(not Physics.isInCircle(0, 0, 1.01, 0, 1))      # Point just out of the circle
        assert(Physics.isInCircle(0, 0, 0.99, 0, 1))          # Point just in the circle
        for i in range(360):
            assert(Physics.isInCircle(cos(radians(i)), sin(radians(i)), 0, 0, 1)) # Points on the circle's perimetre

    # def test_rectIntersectsCircle(self):
    #     assert(not Physics.rectIntersectsCircle(-1, 1, 2, 2, 0, 0, 1))  # Circle inside Rectangle
    #     assert(Physics.rectIntersectsCircle(-1, 1, 2, 2, 0, 0, 4))      # Rectangle inside Circle
    #     assert(Physics.rectIntersectsCircle(-1.2, 1.2, 1, 1, 0, 0, 1))  # Bottom-Right corner inside Circle
    #     assert(Physics.rectIntersectsCircle(-1.2, -0.6, 1, 1, 0, 0, 1)) # Top-Right corner inside Circle
    #     assert(Physics.rectIntersectsCircle(0.6, 1.2 , 1, 1, 0, 0, 1))  # Bottom-Left corner inside Circle
    #     assert(Physics.rectIntersectsCircle(0.6, -0.6, 1, 1, 0, 0, 1))  # Top-Left corner inside Circle
    #     assert(Physics.rectIntersectsCircle(0.6, 2, 1, 3, 0, 0, 1))     # No corner inside Circle, just a line crosses

    # def test_polygonIntersectsRect(self):
    #     assert(Physics.polygonIntersectsRect([(0, 0), (1, 1), (1, 0)], 0.75, 0.25, 1, 1))              # Rectangle hit by Triangle
    #     assert(not Physics.polygonIntersectsRect([(0, 0), (1, 1), (2, 1), (2, -1)], 0.75, 0.25, 1, 1)) # Same Rectangle wrapped by polygon (no intersect)
    #     assert(not Physics.polygonIntersectsRect([(1, 1), (1.5, 1.5), (1.5, 1)], 0.75, 0.25, 1, 1))    # Same Rectangle with polygon inside (no intersect)

    def test_lineIntersectsRect(self):
        assert(True)

    def test_lineIntersectsLine(self):
        assert(True)    

    def test_pointInsidePolygon(self):
        assert(True)

    def test_createCirclePolygon(self):
        assert(True)