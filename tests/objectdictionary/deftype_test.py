import unittest
from canopenx.objectdictionary import DefType, UNSIGNED32


class DefTypeTestCase(unittest.TestCase):
	def test_init(self):
		with self.assertRaises(ValueError):
			DefType("deftype", -1)
		with self.assertRaises(ValueError):
			DefType("deftype", 65536)

		name = "deftype"
		index = 0x100
		deftype = DefType(name, index)

		self.assertEqual(deftype.name, name)
		self.assertEqual(deftype.index, index)
		self.assertEqual(deftype.subindex, 0)
		self.assertEqual(deftype.data_type, UNSIGNED32)
		self.assertEqual(deftype.access_type, "ro")

		with self.assertRaises(AttributeError):
			deftype.name = name
		with self.assertRaises(AttributeError):
			deftype.index = index
		with self.assertRaises(AttributeError):
			deftype.subindex = 0
		with self.assertRaises(AttributeError):
			deftype.data_type = UNSIGNED32
		with self.assertRaises(AttributeError):
			deftype.access_type = "ro"
