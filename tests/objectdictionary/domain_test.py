import unittest
from hypothesis import given, example, strategies as st

from canopenx.objectdictionary import Domain
from canopenx.objectdictionary import BOOLEAN, UNSIGNED32


class DomainTestCase(unittest.TestCase):
	def test_equals(self):
		a = Domain("domain", 0x100, "rw")

		with self.subTest("Reflexivity"):
			self.assertTrue(a == a)

		with self.subTest("Transitivity"):
			test_data = [None, 3]
			for value in test_data:
				with self.subTest("value=" + str(value)):
					self.assertFalse(a == value)

		with self.subTest("Consistency"):
			b = Domain("domain", 0x100, "rw")
			for _ in range(3):
				self.assertTrue(a == b)

		with self.subTest("Symmetricality"):
			b = Domain("domain", 0x100, "rw")
			self.assertTrue(a == b)
			self.assertEqual(a == b, b == a)

			b = Domain("x", 0x100, "rw")
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)

			b = Domain("domain", 0x111, "rw")
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)

			b = Domain("domain", 0x100, "ro")
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)

	@given(name = st.just("domain"), index = st.just(0x100), access_type = st.just("rw"), test_outcome = st.just("pass"))
	@example(name = "domain", index = 0x100, access_type = "rw", test_outcome = "pass")
	@example(name = "domain", index = -1, access_type = "rw", test_outcome = "fail")
	@example(name = "domain", index = 0x100, access_type = "", test_outcome = "fail")
	def test_init(self, name, index, access_type, test_outcome):
		if test_outcome == "pass":
			dom = Domain(name, index, access_type)
			self.assertEqual(dom.object_type, 2)
		else:
			with self.assertRaises(ValueError):
				Domain(name, index, access_type)

	def test_properties(self):
		examinee = Domain("domain", 0x100, "rw")

		examinee.access_type = "const"
		examinee.access_type = "ro"
		examinee.access_type = "wo"
		examinee.access_type = "rw"

		with self.assertRaises(ValueError):
			examinee.access_type = "xx"
