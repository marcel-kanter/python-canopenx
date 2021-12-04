import canopenx
import unittest

from canopenx.node import Node
from canopenx.objectdictionary.array import Array
from canopenx.objectdictionary.datatypes import UNSIGNED8, UNSIGNED32
from canopenx.objectdictionary.defstruct import DefStruct
from canopenx.objectdictionary.record import Record
from canopenx.objectdictionary.variable import Variable


class CollectionProxyTestCase(unittest.TestCase):
	def test_access(self):
		dictionary = canopenx.ObjectDictionary()

		node = Node(1, dictionary)

		# Array
		dictionary.add(Array("array", 0x1000, UNSIGNED32))

		arr = node["array"]

		with self.assertRaises(KeyError):
			arr_var = arr["variable"]

		dictionary["array"].add(Variable("variable", 0x1000, 0x00, UNSIGNED8))

		self.assertTrue("variable" in node["array"])
		arr_var = arr["variable"]
		self.assertEqual(len(dictionary["array"]), len(node["array"]))

		self.assertEqual(dictionary["array"].data_type, node["array"].data_type)
		self.assertEqual(dictionary["array"].index, node["array"].index)
		self.assertEqual(dictionary["array"].name, node["array"].name)

		# DefStruct
		dictionary.add(DefStruct("defstruct", 0x2000))

		defstr = node["defstruct"]

		with self.assertRaises(KeyError):
			defstr_var = defstr["variable"]	

		dictionary["defstruct"].add(Variable("variable", 0x2000, 0x00, UNSIGNED8))

		self.assertTrue("variable" in node["defstruct"])
		defstr_var = defstr["variable"]	
		self.assertEqual(len(dictionary["defstruct"]), len(node["defstruct"]))

		self.assertEqual(dictionary["defstruct"].data_type, node["defstruct"].data_type)
		self.assertEqual(dictionary["defstruct"].index, node["defstruct"].index)
		self.assertEqual(dictionary["defstruct"].name, node["defstruct"].name)

		# Record
		dictionary.add(Record("record", 0x5000))

		rec = node["record"]

		with self.assertRaises(KeyError):
			rec_var = rec["variable"]

		dictionary["record"].add(Variable("variable", 0x5000, 0x00, UNSIGNED8))

		self.assertTrue("variable" in node["record"])
		rec_var = rec["variable"]	
		self.assertEqual(len(dictionary["record"]), len(node["record"]))

		self.assertEqual(dictionary["record"].data_type, node["record"].data_type)
		self.assertEqual(dictionary["record"].index, node["record"].index)
		self.assertEqual(dictionary["record"].name, node["record"].name)
