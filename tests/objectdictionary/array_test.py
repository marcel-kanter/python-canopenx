import unittest
from hypothesis import given, example, strategies as st

from canopenx.objectdictionary import Array, DefStruct, Record, Variable
from canopenx.objectdictionary import BOOLEAN, UNSIGNED32


class ArrayTestCase(unittest.TestCase):
	def test_equals(self):
		a = Array("array", 0x100, UNSIGNED32)

		with self.subTest("Reflexivity"):
			self.assertTrue(a == a)

		with self.subTest("Transitivity"):
			test_data = [None, 3]
			for value in test_data:
				with self.subTest("value=" + str(value)):
					self.assertFalse(a == value)

		with self.subTest("Consistency"):
			b = Array("array", 0x100, UNSIGNED32)
			for _ in range(3):
				self.assertTrue(a == b)

		with self.subTest("Symmetricality"):
			b = Array("array", 0x100, UNSIGNED32)
			self.assertTrue(a == b)
			self.assertEqual(a == b, b == a)

			b = Array("x", 0x100, UNSIGNED32)
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)

			b = Array("array", 0x101, UNSIGNED32)
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)

			b = Array("array", 0x100, BOOLEAN)
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)

			b = Array("array", 0x100, UNSIGNED32)
			b.add(Variable("variable", 0x100, 0x00, UNSIGNED32))
			self.assertFalse(a == b)

			a.add(Variable("variable", 0x100, 0x00, UNSIGNED32))
			self.assertTrue(a == b)

			b = Array("array", 0x100, UNSIGNED32)
			b.add(Variable("x", 0x100, 0x00, UNSIGNED32))
			self.assertFalse(a == b)

	@given(name = st.just("array"), index = st.just(0x100), data_type = st.just(0), test_outcome = st.just("pass"))
	@example(name = "array", index = -1, data_type = 0, test_outcome = "fail")
	@example(name = "array", index = 0x100, data_type = -1, test_outcome = "fail")
	@example(name = "array", index = 0x100, data_type = 0x20, test_outcome = "fail")
	def test_init(self, name, index, data_type, test_outcome):
		if test_outcome == "pass":
			Array(name, index, data_type)
		else:
			with self.assertRaises(ValueError):
				Array(name, index, data_type)	

	def test_collection(self):
		examinee = Array("array", 0x100, UNSIGNED32)

		with self.assertRaises(TypeError):
			examinee.add(Array("x", 0x100, UNSIGNED32))

		with self.assertRaises(TypeError):
			examinee.add(DefStruct("x", 0x100))

		with self.assertRaises(TypeError):
			examinee.add(Record("x", 0x100))

		with self.assertRaises(ValueError):
			examinee.add(Variable("variable", 0x111, 0x00, UNSIGNED32))

		examinee.add(Variable("variable", 0x100, 0x00, UNSIGNED32))
		self.assertTrue("variable" in examinee)
		self.assertTrue(0x00 in examinee)

		with self.assertRaises(ValueError):
			examinee.add(Variable("x", 0x100, 0x00, UNSIGNED32))

		with self.assertRaises(ValueError):
			examinee.add(Variable("variable", 0x100, 0x01, UNSIGNED32))

		examinee.add(Variable("x", 0x100, 0x01, UNSIGNED32))
		self.assertTrue("x" in examinee)
		self.assertTrue(0x01 in examinee)

		self.assertEqual(len(examinee), 2)
