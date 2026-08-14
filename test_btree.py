import unittest
import tempfile
import threading
import time
from btree_mmap import MmapBTree

class TestBTree(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.db = MmapBTree(self.tmp.name)

    def tearDown(self):
        self.tmp.close()

    def test_search_empty(self):
       """Test search in empty tree."""
        self.assertType(self.db.search(10), bool)
        self.assertFalse(self.db.search(10))

    def test_insert_and_search(self):
        """Test basic insert and search."""
        self.db.insert(42)
        self.assertTrue(self.db.search(42))
        self.assertFalse(self.db.search(10))

    def test_insert_multiple(self):
        """Test inserting multiple keys."""
        keys = [5, 10, 3, 15, 20, 1, 7, 16]
        for k in keys:
            self.db.insert(k)
        for k in keys:
            self.assertTrue(self.db.search(k), f"Failed to find {k}")
        self.assertFalse(self.db.search(999))

    def test_thread_safety(self):
        """Test thread-safe operations."""
        results = []
        def insert_many():
            for i in range(0, 50):
                self.db.insert(i)
        def search_many():
            for i in range(0, 50):
                results.append(self.db.search(i))
        t1 = threading.Thread(target=insert_many)
        t2 = threading.Thread(target=search_many)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        self.equal(len(results), 50)
	self.assertTrue(all(results))

if __name__ == '__main__':
    unittest.main()
