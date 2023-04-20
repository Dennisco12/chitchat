import unittest
from chitchatcli.utilis.storage import PersistentDataStorage


class TestPersistentDataStorage(unittest.TestCase):
    def setUp(self):
        self.storage = PersistentDataStorage()

    def test_store(self):
        self.storage.store('key', 'value')
        self.assertEqual(self.storage.retrieve('key'), 'value')

    def test_delete(self):
        self.storage.store('key', 'value')
        self.storage.delete('key')
        self.assertIsNone(self.storage.retrieve('key'))


if __name__ == '__main__':
    unittest.main()
