import unittest
import mock

from canopenx import ObjectDictionary
from canopenx.node import Node
from canopenx.node.service import Service


class EventTestService(Service):
	def __init__(self):
		Service.__init__(self)

	def add_event_a(self):
		self._add_event("A")

	def remove_event_a(self):
		self._remove_event("A")

	def add_event_b(self):
		self._add_event("B")

	def remove_event_b(self):
		self._remove_event("B")


class ServiceTestCase(unittest.TestCase):
	def test_attach(self):
		dictionary = ObjectDictionary()
		node = Node(1, dictionary)

		examinee = Service()
		self.assertFalse(examinee.is_attached())
		self.assertEqual(examinee.node, None)

		examinee.attach(node)
		self.assertTrue(examinee.is_attached())
		self.assertEqual(examinee.node, node)

		examinee.detach()
		self.assertFalse(examinee.is_attached())
		self.assertEqual(examinee.node, None)

	def test_events(self):
		examinee = EventTestService()

		cb1 = mock.Mock(side_effect = Exception)
		cb2 = mock.Mock(side_effect = Exception)

		# The class does not contain events by default and the test implementation too
		self.assertFalse(examinee.has_event("A"))
		self.assertFalse(examinee.has_event("B"))

		# Add wrong types
		with self.assertRaises(TypeError):
			examinee.add_callback("A", None)

		with self.assertRaises(KeyError):
			examinee.add_callback("A", cb1)

		# Remove an event which not belongs to the service - not ok
		with self.assertRaises(KeyError):
			examinee.remove_event_a()

		# Successfully add event
		examinee.add_event_a()
		self.assertTrue(examinee.has_event("A"))
		self.assertFalse(examinee.has_event("B"))
		self.assertFalse(examinee.has_callback("A", cb1))
		with self.assertRaises(KeyError):
			self.assertFalse(examinee.has_callback("B", cb1))

		# Adding an event twice - not ok
		with self.assertRaises(KeyError):
			examinee.add_event_a()

		# Adding a callback
		examinee.add_callback("A", cb1)
		self.assertTrue(examinee.has_callback("A", cb1))
		with self.assertRaises(KeyError):
			self.assertFalse(examinee.has_callback("B", cb1))

		# Notifiy only event A
		cb1.reset_mock()
		cb2.reset_mock()
		examinee.notify("A")
		cb1.assert_called_once()
		cb2.assert_not_called()

		cb1.reset_mock()
		cb2.reset_mock()
		with self.assertRaises(KeyError):
			examinee.notify("B")
		cb1.assert_not_called()
		cb2.assert_not_called()

		# Adding a second event
		examinee.add_event_b()
		examinee.add_callback("B", cb2)
		self.assertTrue(examinee.has_event("A"))
		self.assertTrue(examinee.has_event("B"))
		self.assertTrue(examinee.has_callback("A", cb1))
		self.assertFalse(examinee.has_callback("A", cb2))
		self.assertFalse(examinee.has_callback("B", cb1))
		self.assertTrue(examinee.has_callback("B", cb2))

		# Notifying should call only the callbacks for the events, which should be notified
		cb1.reset_mock()
		cb2.reset_mock()
		examinee.notify("A")
		cb1.assert_called_once()
		cb2.assert_not_called()

		cb1.reset_mock()
		cb2.reset_mock()
		examinee.notify("B")
		cb1.assert_not_called()
		cb2.assert_called_once()

		# Removing an callback that is not in the list - not ok
		with self.assertRaises(ValueError):
			examinee.remove_callback("A", cb2)

		with self.assertRaises(ValueError):
			examinee.remove_callback("A", None)

		examinee.remove_callback("A", cb1)
		self.assertFalse(examinee.has_callback("A", cb1))

		# Removing twice - not ok
		with self.assertRaises(ValueError):
			examinee.remove_callback("A", cb1)

		# Check whether the callback is removed correctly and only from the specified event
		cb1.reset_mock()
		cb2.reset_mock()
		examinee.notify("A")
		cb1.assert_not_called()
		cb2.assert_not_called()

		cb1.reset_mock()
		cb2.reset_mock()
		examinee.notify("B")
		cb1.assert_not_called()
		cb2.assert_called_once()

		# Remove the event
		examinee.remove_event_a()
		self.assertFalse(examinee.has_event("A"))
		self.assertTrue(examinee.has_event("B"))

		cb1.reset_mock()
		cb2.reset_mock()
		with self.assertRaises(KeyError):
			examinee.notify("A")
		cb1.assert_not_called()
		cb2.assert_not_called()

		cb1.reset_mock()
		cb2.reset_mock()
		examinee.notify("B")
		cb1.assert_not_called()
		cb2.assert_called_once()

		examinee.remove_event_b()
		self.assertFalse(examinee.has_event("A"))
		self.assertFalse(examinee.has_event("B"))

		# Check whether the event is removed correctly and only from the specified event
		cb1.reset_mock()
		cb2.reset_mock()
		with self.assertRaises(KeyError):
			examinee.notify("A")
		cb1.assert_not_called()
		cb2.assert_not_called()

		cb1.reset_mock()
		cb2.reset_mock()
		with self.assertRaises(KeyError):
			examinee.notify("B")
		cb1.assert_not_called()
		cb2.assert_not_called()
