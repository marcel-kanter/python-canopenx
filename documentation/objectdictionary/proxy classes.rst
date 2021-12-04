Proxy classes
=============

The object dictionary is a template which contains a description of all objects of a node. One object dictionary may be used by many nodes.
Each node has its own instances of these objects, which mirror the structure of the object dictionary. The behavior of the instances depends on their root (or parent).

Each class of the object dictionary implements a method `proxy`. This method creates a representation of the class which is bound to a node.
