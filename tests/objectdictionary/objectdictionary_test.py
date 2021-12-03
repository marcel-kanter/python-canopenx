import canopenx
import unittest

from canopenx.objectdictionary import Variable
from canopenx.objectdictionary import UNSIGNED32


class ObjectDictionaryTestCase(unittest.TestCase):
	def test_equals(self):
		a = canopenx.ObjectDictionary()

		with self.subTest("Reflexivity"):
			self.assertTrue(a == a)

		with self.subTest("Transitivity"):
			test_data = [None, 3]
			for value in test_data:
				with self.subTest("value=" + str(value)):
					self.assertFalse(a == value)

		with self.subTest("Consistency"):
			b = canopenx.ObjectDictionary()
			for _ in range(3):
				self.assertTrue(a == b)

		with self.subTest("Symmetricality"):
			b = canopenx.ObjectDictionary()
			self.assertTrue(a == b)
			self.assertEqual(a == b, b == a)

			b.add(Variable("variable", 0x100, 0x00, UNSIGNED32))
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)

			a.add(Variable("variable", 0x100, 0x00, UNSIGNED32))
			self.assertTrue(a == b)
			self.assertEqual(a == b, b == a)

			b = canopenx.ObjectDictionary()
			b.add(Variable("x", 0x100, 0x00, UNSIGNED32))
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)

	def test_init(self):
		canopenx.ObjectDictionary()

	def test_collection(self):
		examinee = canopenx.ObjectDictionary()

		with self.assertRaises(TypeError):
			examinee.add(canopenx.ObjectDictionary())

		examinee.add(Variable("variable", 0x100, 0x00, UNSIGNED32))
		self.assertTrue("variable" in examinee)
		self.assertTrue(0x100 in examinee)
