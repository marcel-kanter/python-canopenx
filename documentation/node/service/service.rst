Service
=======

The CANopen standard defines several protocols and CAN messages used for these protocols. Each of the protocols has its own set of assigned CAN message IDs and an expected behaviour.

The class Service is the base class for implementing the protocols.

Attach/Detach
-------------

The base class implements the attach/detach pattern.

On attach, the service may read data from the node or register callbacks in the network.

On detach, the service shall clean up the changes made during attach, e.g. unregister all callbacks.
