import unittest
from hypothesis import given, example, strategies as st

from canopenx.objectdictionary import Array, DefStruct, Record, Variable
from canopenx.objectdictionary import BOOLEAN, UNSIGNED8, UNSIGNED16, UNSIGNED32


class DefStructTestCase(unittest.TestCase):
	def test_equals(self):
		a = DefStruct("defstruct", 0x100)

		with self.subTest("Reflexivity"):
			self.assertTrue(a == a)

		with self.subTest("Transitivity"):
			test_data = [None, 3]
			for value in test_data:
				with self.subTest("value=" + str(value)):
					self.assertFalse(a == value)

		with self.subTest("Consistency"):
			b = DefStruct("defstruct", 0x100)
			for _ in range(3):
				self.assertTrue(a == b)

		with self.subTest("Symmetricality"):
			b = DefStruct("defstruct", 0x100)
			self.assertTrue(a == b)
			self.assertEqual(a == b, b == a)

			b = DefStruct("x", 0x100)
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)

			b = DefStruct("defstruct", 0x101)
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)

			b = DefStruct("defstruct", 0x100)
			b.add(Variable("variable", 0x100, 0x00, UNSIGNED8, "ro"))
			self.assertFalse(a == b)

			a.add(Variable("variable", 0x100, 0x00, UNSIGNED8, "ro"))
			self.assertTrue(a == b)

			b = DefStruct("defstruct", 0x100)
			b.add(Variable("x", 0x100, 0x00, UNSIGNED8, "ro"))
			self.assertFalse(a == b)

	@given(name = st.just("defstruct"), index = st.just(0x100), test_outcome = st.just("pass"))
	@example(name = "defstruct", index = -1, test_outcome = "fail")
	def test_init(self, name, index, test_outcome):
		if test_outcome == "pass":
			DefStruct(name, index)
		else:
			with self.assertRaises(ValueError):
				DefStruct(name, index)

	def test_collection(self):
		examinee = DefStruct("defstruct", 0x100)

		with self.assertRaises(TypeError):
			examinee.add(Array("x", 0x100, UNSIGNED32))

		with self.assertRaises(TypeError):
			examinee.add(Record("x", 0x100))

		with self.assertRaises(ValueError):
			examinee.add(Variable("variable", 0x111, 0x00, UNSIGNED32))

		with self.assertRaises(ValueError):
			examinee.add(Variable("variable", 0x100, 0x00, UNSIGNED32))

		with self.assertRaises(ValueError):
			examinee.add(Variable("variable", 0x100, 0x01, UNSIGNED8))

		with self.assertRaises(ValueError):
			examinee.add(Variable("variable", 0x100, 0xFF, UNSIGNED8))

		examinee.add(Variable("variable", 0x100, 0x00, UNSIGNED8, "ro"))
		self.assertTrue("variable" in examinee)
		self.assertTrue(0x00 in examinee)

		with self.assertRaises(ValueError):
			examinee.add(Variable("x", 0x100, 0x00, UNSIGNED32))

		with self.assertRaises(ValueError):
			examinee.add(Variable("variable", 0x100, 0x01, UNSIGNED32))

		examinee.add(Variable("x", 0x100, 0x01, UNSIGNED16, "ro"))
		self.assertTrue("x" in examinee)
		self.assertTrue(0x01 in examinee)

		self.assertEqual(len(examinee), 2)
