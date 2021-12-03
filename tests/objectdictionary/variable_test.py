import unittest
from hypothesis import given, example, strategies as st

from canopenx.objectdictionary import Variable
from canopenx.objectdictionary import BOOLEAN, UNSIGNED32


class VariableTestCase(unittest.TestCase):
	def test_equals(self):
		a = Variable("variable", 0x100, 0x00, UNSIGNED32, "rw")

		with self.subTest("Reflexivity"):
			self.assertTrue(a == a)

		with self.subTest("Transitivity"):
			test_data = [None, 3]
			for value in test_data:
				with self.subTest("value=" + str(value)):
					self.assertFalse(a == value)

		with self.subTest("Consistency"):
			b = Variable("variable", 0x100, 0x00, UNSIGNED32, "rw")
			for _ in range(3):
				self.assertTrue(a == b)

		with self.subTest("Symmetricality"):
			b = Variable("variable", 0x100, 0x00, UNSIGNED32, "rw")
			self.assertTrue(a == b)
			self.assertEqual(a == b, b == a)

			b = Variable("x", 0x100, 0x00, UNSIGNED32, "rw")
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)
		
			b = Variable("variable", 0x111, 0x00, UNSIGNED32, "rw")
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)
		
			b = Variable("variable", 0x100, 0x01, UNSIGNED32, "rw")
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)
		
			b = Variable("variable", 0x100, 0x00, BOOLEAN, "rw")
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)
		
			b = Variable("variable", 0x100, 0x00, UNSIGNED32, "ro")
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)

	@given(name = st.just("variable"), index = st.just(0x100), subindex = st.just(0x00), data_type = st.just(UNSIGNED32), access_type = st.just("rw"), test_outcome = st.just("pass"))
	@example(name = "variable", index = 0x100, subindex = 0x00, data_type = BOOLEAN, access_type = "rw", test_outcome = "pass")
	@example(name = "variable", index = -1, subindex = 0x00, data_type = UNSIGNED32, access_type = "rw", test_outcome = "fail")
	@example(name = "variable", index = 0x100, subindex = -1, data_type = UNSIGNED32, access_type = "rw", test_outcome = "fail")
	@example(name = "variable", index = 0x100, subindex = 0x00, data_type = -1, access_type = "rw", test_outcome = "fail")
	@example(name = "variable", index = 0x100, subindex = 0x00, data_type = BOOLEAN, access_type = "", test_outcome = "fail")
	def test_init(self, name, index, subindex, data_type, access_type, test_outcome):
		if test_outcome == "pass":
			Variable(name, index, subindex, data_type, access_type)
		else:
			with self.assertRaises(ValueError):
				Variable(name, index, subindex, data_type, access_type)	

	def test_properties(self):
		examinee = Variable("variable", 0x100, 0x00, UNSIGNED32, "rw")

		examinee.access_type = "const"
		examinee.access_type = "ro"
		examinee.access_type = "wo"
		examinee.access_type = "rw"

		with self.assertRaises(ValueError):
			examinee.access_type = "xx"
