import canopenx
import unittest


class Item(object):
	def __eq__(self, other):
		if type(self) != type(other):
			return False
		return self is other or (self.name == other.name and self.index == other.index)

	def __init__(self, name, index):
		self.name = name
		self.index = index


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

			b.add(Item("variable", 0x100))
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)

			a.add(Item("variable", 0x100))
			self.assertTrue(a == b)
			self.assertEqual(a == b, b == a)

			b = canopenx.ObjectDictionary()
			b.add(Item("x", 0x100))
			self.assertFalse(a == b)
			self.assertEqual(a == b, b == a)

	def test_init(self):
		canopenx.ObjectDictionary()

	def test_collection(self):
		examinee = canopenx.ObjectDictionary()

		examinee.add(Item("variable", 0x100))
		self.assertTrue("variable" in examinee)
		self.assertTrue(0x100 in examinee)
