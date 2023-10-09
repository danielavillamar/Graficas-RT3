import math


def normalize(vec):
    """Normalize a vector."""
    norm = math.sqrt(sum([x * x for x in vec]))
    return [x / norm for x in vec]


def dot(vec1, vec2):
    """Dot product of two vectors."""
    return sum([x * y for x, y in zip(vec1, vec2)])


def subtract(vec1, vec2):
    """Subtract two vectors."""
    return [x - y for x, y in zip(vec1, vec2)]


def linalg_norm(vec):
    """Get the norm of a vector."""
    return math.sqrt(sum([x * x for x in vec]))


def add(vec1, vec2):
    """Add two vectors."""
    return [x + y for x, y in zip(vec1, vec2)]


def multiplyVectorScalar(vec, scalar):
    """Multiply a vector by a scalar."""
    return [x * scalar for x in vec]


def multiplyVectorVector(vec1, vec2):
    """Multiply two vectors."""
    return [x * y for x, y in zip(vec1, vec2)]


def subtractVectorVector(vec1, vec2):
    """Subtract two vectors."""
    return [x - y for x, y in zip(vec1, vec2)]


def negateVector(vec):
    """Negate a vector."""
    return [-x for x in vec]


def divideVectorScalar(vec, scalar):
    """Divide a vector by a scalar."""
    return [x / scalar for x in vec]