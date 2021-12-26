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
		dt = DefType(name, index)

		self.assertEqual(dt.name, name)
		self.assertEqual(dt.index, index)
		self.assertEqual(dt.subindex, 0)
		self.assertEqual(dt.data_type, UNSIGNED32)
		self.assertEqual(dt.access_type, "ro")

		self.assertEqual(dt.object_type, 5)

		with self.assertRaises(AttributeError):
			dt.name = name
		with self.assertRaises(AttributeError):
			dt.index = index
		with self.assertRaises(AttributeError):
			dt.subindex = 0
		with self.assertRaises(AttributeError):
			dt.data_type = UNSIGNED32
		with self.assertRaises(AttributeError):
			dt.access_type = "ro"
