Network
=======

The Network class is the base class for a CANopen network.

Callbacks for CAN messages
--------------------------

The Network class provides the methods subscribe, subscribed and unsubscribe to register callbacks for CAN messages.
The implementation support more than one callback for each message identifier. Registering a callback twice for the same message identifier is not allowed.
If an exception occurs in the callback, it is silently ignored and the remaining callbacks get invoked.

Dictionary of Nodes
-------------------

The Network is basically a dictionary of nodes. It is possbile to add nodes to a network, get a node by id or name, iterate over all nodes and remove nodes from a network.
