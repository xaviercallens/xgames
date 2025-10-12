"""
Mathematical utilities for game development.
Includes vector operations, collision detection, and common game math functions.
"""

import math
from typing import Tuple, List


class Vector2D:
    """2D Vector class for position, velocity, and direction calculations."""
    
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float):
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def magnitude(self) -> float:
        """Calculate the magnitude (length) of the vector."""
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self):
        """Return a normalized version of the vector."""
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)
    
    def distance_to(self, other) -> float:
        """Calculate distance to another vector."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def dot_product(self, other) -> float:
        """Calculate dot product with another vector."""
        return self.x * other.x + self.y * other.y
    
    def to_tuple(self) -> Tuple[float, float]:
        """Convert to tuple for use with pygame."""
        return (self.x, self.y)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(value, max_val))


def lerp(start: float, end: float, t: float) -> float:
    """Linear interpolation between start and end."""
    return start + (end - start) * t


def circle_collision(pos1: Tuple[float, float], radius1: float, 
                    pos2: Tuple[float, float], radius2: float) -> bool:
    """Check collision between two circles."""
    distance = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    return distance < (radius1 + radius2)


def rect_collision(rect1: Tuple[float, float, float, float], 
                  rect2: Tuple[float, float, float, float]) -> bool:
    """Check collision between two rectangles (x, y, width, height)."""
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    
    return (x1 < x2 + w2 and x1 + w1 > x2 and 
            y1 < y2 + h2 and y1 + h1 > y2)


def angle_between_points(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate angle between two points in radians."""
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


def rotate_point(point: Tuple[float, float], angle: float, 
                center: Tuple[float, float] = (0, 0)) -> Tuple[float, float]:
    """Rotate a point around a center by given angle (radians)."""
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    
    # Translate to origin
    x = point[0] - center[0]
    y = point[1] - center[1]
    
    # Rotate
    new_x = x * cos_angle - y * sin_angle
    new_y = x * sin_angle + y * cos_angle
    
    # Translate back
    return (new_x + center[0], new_y + center[1])
