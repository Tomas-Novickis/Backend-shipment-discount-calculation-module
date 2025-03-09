import unittest
from shipment_discount import (Transaction,
                               Rules, VALID_PROVIDERS,
                               VALID_SIZES, PRICES)


class TestTransaction(unittest.TestCase):
    def test_valid_transaction(self):
        self.assertTrue(Transaction.is_valid(["2024-12-01", "L", "MR"]))
        self.assertTrue(Transaction.is_valid(["2024-12-01", "S", "LP"]))
        self.assertTrue(Transaction.is_valid(["2024-12-03", "L", "MR"]))

    def test_invalid_transaction(self):
        self.assertFalse(Transaction.is_valid(["2024-12-01", "XLL", "MR"]))
        self.assertFalse(Transaction.is_valid(["2025-12-01", "L", "TEST"]))
        self.assertFalse(Transaction.is_valid(["0", "L", "MR"]))
        self.assertFalse(Transaction.is_valid([]))

    def test_shipping_price(self):
        transaction = Transaction("2024-12-01", "L", "LP")
        self.assertEqual(transaction.price, PRICES['LP']['L'])
        self.assertNotEqual(transaction.price, PRICES['LP']['S'])
        self.assertNotEqual(transaction.price, PRICES['MR']['L'])

    def test_shipping_price_valid_combinations(self):
        for provider in VALID_PROVIDERS:
            for size in VALID_SIZES:
                transaction = Transaction("2024-12-01", size, provider)
                expected_price = PRICES[provider][size]
                self.assertEqual(transaction.price, expected_price)


class TestRules(unittest.TestCase):
    def setUp(self):
        self.rules = Rules()

    def test_apply_discount(self):
        transaction = Transaction("2024-12-01", "S", "MR")
        discount = self.rules.apply_rules(transaction)
        self.assertEqual(discount, 0.5)

    def test_no_discount(self):
        transaction = Transaction("2024-12-01", "S", "LP")
        discount = self.rules.apply_rules(transaction)
        self.assertEqual(discount, '-')

    def test_third_lp_large_shipment_free(self):
        for i in range(2):
            transaction = Transaction(f"2024-12-{i+1}", "L", "LP")
            discount = self.rules.apply_rules(transaction)
            self.assertEqual(discount, '-')

        transaction = Transaction("2024-12-03", "L", "LP")
        discount = self.rules.apply_rules(transaction)
        self.assertEqual(discount, transaction.price)

    def test_max_discounts_per_month(self):
        for i in range(20):
            transaction = Transaction(f"2024-12-0{i + 1}", "S", "MR")
            self.rules.apply_rules(transaction)

        # transaction should not get a discount as monthly limit is 10
        transaction = Transaction("2024-12-04", "S", "MR")
        discount = self.rules.apply_rules(transaction)
        self.assertEqual(discount, '-')

    def test_lowest_s_price(self):
        transaction = Transaction("2024-12-01", "S", "MR")
        discount = self.rules.apply_rules(transaction)
        self.assertEqual(transaction.price - discount,
                         self.rules.lowest_s_price)


if __name__ == '__main__':
    unittest.main()
