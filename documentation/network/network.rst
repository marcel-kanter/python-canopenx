Network
=======

The Network class is the base class for a CANopen network.

Callbacks for CAN messages
--------------------------

The Network class provides the methods subscribe, subscribed and unsubscribe to register callbacks for CAN messages.
The implementation support more than one callback for each message identifier. Registering a callback twice for the same message identifier is not allowed.
If an exception occurs in the callback, it is silently ignored and the remaining callbacks get invoked.
