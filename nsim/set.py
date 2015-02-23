def unique(a):
    """ return the list with duplicate elements removed """
    return list(set(a))

def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

def exclusive(a, b):
    """ return the unique elements of two lists """
    return list(set(a) ^ set(b))

def subtract(a, b):
    """ return the elements of a not in b """
    return list(set(a) - set(b)) 

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))
