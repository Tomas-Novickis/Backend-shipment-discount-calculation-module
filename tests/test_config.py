import unittest
from shipment_discount import (Transaction, VALID_PROVIDERS,
                               VALID_SIZES, PRICES)


class TestNewProvider(unittest.TestCase):
    def setUp(self):
        """Save the original state and temporarily modify it."""
        self.original_valid_providers = VALID_PROVIDERS.copy()
        self.original_prices = PRICES.copy()

        VALID_PROVIDERS.add("TEST")
        PRICES["TEST"] = {'S': 1.00, 'M': 2.00, 'L': 3.00}

    def tearDown(self):
        """Restore the original state to avoid side effects."""
        VALID_PROVIDERS.clear()
        VALID_PROVIDERS.update(self.original_valid_providers)

        PRICES.clear()
        PRICES.update(self.original_prices)

    def test_new_provider(self):
        self.assertTrue(Transaction.is_valid(["2024-12-01", "S", "TEST"]))

    def test_new_provider_price(self):
        transaction = Transaction("2024-12-01", "S", "TEST")
        self.assertEqual(transaction.price, 1.00)

    def test_new_provider_invalid_size(self):
        self.assertFalse(Transaction.is_valid(["2024-12-01", "XL", "TEST"]))


class TestNewSize(unittest.TestCase):
    def setUp(self):
        self.original_valid_sizes = VALID_SIZES.copy()

        VALID_SIZES.add('XS')

    def tearDown(self):
        VALID_SIZES.clear()
        VALID_SIZES.update(self.original_valid_sizes)

    def test_new_size(self):
        self.assertIn('XS', VALID_SIZES)

    def test_new_size_invalid_provider(self):
        self.assertFalse(Transaction.is_valid(["2024-12-01", "XL", "LP"]))


class TestNewPrice(unittest.TestCase):

    def setUp(self):
        self.original_prices = PRICES.copy()

        PRICES['LP']['XL'] = 9.99
        PRICES['MR']['M'] = 3.20

    def tearDown(self):
        PRICES.clear()
        PRICES.update(self.original_prices)

    def test_new_price(self):
        self.assertEqual(PRICES['LP']['XL'], 9.99)

    def test_modified_price(self):
        self.assertEqual(PRICES['MR']['M'], 3.20)


class TestDefaultState(unittest.TestCase):
    def test_default_state(self):
        self.assertNotIn('TEST', VALID_PROVIDERS)
        self.assertNotIn('XL', VALID_SIZES)
        self.assertNotIn(9.99, PRICES)
        self.assertEqual(PRICES['LP']['L'], 6.90)


if __name__ == '__main__':
    unittest.main()
