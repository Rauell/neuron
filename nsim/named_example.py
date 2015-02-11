from collections import namedtuple
from nsim import *


a = Stimulus(1, 2, 3, 4, 5, 6)
print a
b = Stimulus(1,2,3,4,5)
print b
c = Stimulus(1,2,3,4)
print c
d = Stimulus(1,2,3)
print d
e = Stimulus(1,2)
print e
f = Stimulus(1)
print f
g = Stimulus()
print g
'''
namedtuple('Ex', 'age height weight')

class Node(namedtuple('Node', ['value', 'left', 'right'])):
    def __new__(cls, valuee, left=None, right=14):
        return super(Node, cls).__new__(cls, value, left, right)

Node1 = Node(1, 2)
Node2 = Node(3)
Node4 = Node()

print Node1.right
print Node2.left
'''
