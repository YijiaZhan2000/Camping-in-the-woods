"""CS 5001 - Yijia Zhan - Project 10
This module contains unit tests for the `str_to_int`
function in the `configui_wood` module
"""
import unittest
from configui_wood import str_to_int


class TestStrToIntFunction(unittest.TestCase):

    def test_valid_input(self):
        """Test str_to_int with valid integer input."""
        self.assertEqual(str_to_int("42"), 42)

    def test_invalid_input(self):
        """Test str_to_int with invalid input, raising ValueError."""
        with self.assertRaises(ValueError):
            # Test with a non-integer string
            str_to_int("abc")

        with self.assertRaises(ValueError):
            str_to_int("12.34")

    def test_empty_input(self):
        """Test str_to_int with an empty string input, raising ValueError."""
        with self.assertRaises(ValueError):
            # Test with a floating-point number
            str_to_int("")


if __name__ == '__main__':
    unittest.main()
