"""
Sample tests
"""
from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    """Test the calc model"""

    def test_add_numbers(self):
        """Test adding number together"""
        res = calc.add(5, 6)

        self.assertEqual(res, 11)

    # We make this test before we make the code, then make our code so \
    # that it passes the test (TDD)
    def test_subtract_numbers(self):
        """Test subtracting numbers"""
        res = calc.subtract(10, 15)

        self.assertEqual(res, 5)
