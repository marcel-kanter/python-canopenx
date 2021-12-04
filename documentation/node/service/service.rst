Service
=======

The CANopen standard defines several protocols and CAN messages used for these protocols. Each of the protocols has its own set of assigned CAN message IDs and an expected behaviour.

The class Service is the base class for implementing the protocols.

Attach/Detach
-------------

The base class implements the attach/detach pattern.

On attach, the service may read data from the node or register callbacks in the network.

On detach, the service shall clean up the changes made during attach, e.g. unregister all callbacks.

Callbacks
---------

The class Service implements a callback system.

Each callback should be as short as possible.

Use the methods add_event and remove_event to add or remove event names to the service.
Use the methods add_callback and remove_callback to add or remove callback to an event.
Use the method notify to call the callbacks for an event. Currently notify calls the callbacks directly.
