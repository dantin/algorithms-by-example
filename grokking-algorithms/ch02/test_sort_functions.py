
import unittest

from sort_functions import selection_sort


class SortsTestCase(unittest.TestCase):
    """Tests for 'sort_functions.py'."""

    def setUp(self):
        """
        Create a sample list for all test methods.
        """
        self.my_list = [5, 3, 6, 2, 10]

    def test_selection_sort(self):
        """Test selection sort."""
        result = selection_sort(self.my_list)
        self.assertEqual(result, [2, 3, 5, 6, 10])


if __name__ == '__main__':
    unittest.main()
