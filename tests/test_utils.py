import unittest

from service.if_empty import if_empty


class TestFunctionality(unittest.TestCase):
    def test_if_empty_1(self):
        assert if_empty(None, 1) == 1

    def test_if_empty_2(self):
        assert if_empty(1, None) == 1

    def test_if_empty_3(self):
        assert if_empty(None, None) is None


if __name__ == '__main__':
    unittest.main()
