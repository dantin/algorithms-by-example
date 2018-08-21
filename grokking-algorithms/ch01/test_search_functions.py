
import unittest

from search_functions import binary_search


class SearchesTestCase(unittest.TestCase):
    """Tests for 'search_functions.py'."""

    def setUp(self):
        """
        Create a sample list for all test methods.
        """
        self.my_list = [1, 3, 5, 7, 9]

    def test_found_binary_search(self):
        """Test that target is found by binary search."""
        pos = binary_search(self.my_list, 3)
        self.assertEqual(pos, 1)

    def test_not_found_binary_search(self):
        """Test that target is NOT found by binary search."""
        pos = binary_search(self.my_list, -1)
        self.assertTrue(pos == None)


if __name__ == '__main__':
    unittest.main()
