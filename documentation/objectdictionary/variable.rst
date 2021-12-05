Variable
========

The class Variable represents an item in the object dictionary with the type VARIABLE.

To encode/decode a value into/from the CANopen representation, the method encode/decode can be used.
The data type TIME_DIFFERENCE does not allow negative values. If a negative value is passed to encode, the absolute of this value is encoded.
The decode method accepts more bytes than needed, only the lowest/first bytes are used. Decoding an INTEGER8 from a python variable x with 3 bytes will use only use x[0].
