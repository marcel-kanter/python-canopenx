CANopenX
========

This package is a Python implementation of the CANopen standard, as defined in DS301 and DS1301.

It uses python-can as backend.

Features
--------

This package has the following capabilities and features:

- Class/package structure eases the extension or adaption of the functionality.
- Communication to remote nodes on the can bus.
- Emulating of multiple local nodes in software is possible.
- The implemented object dictionary implements nearly all data types of the CANopen standard.

Concept
-------

The basic concept is:
- A network contains nodes.
- A node contains data objects.
- A service provides functionality to its parent.
