import unittest
from shipment_discount import Transaction, apply_discount


class TestOutOfOrderDates(unittest.TestCase):
    def test_out_of_order_dates(self):
        # Create transactions with out-of-order dates
        transactions = [
            Transaction("2024-12-29", "S", "MR"),
            Transaction("2024-12-30", "S", "LP"),
            Transaction("2025-01-01", "L", "LP"),
            Transaction("2024-12-31", "S", "MR"),
        ]

        results = apply_discount(transactions)

        # Verify the results
        expected_results = [
            "2024-12-29 S MR 1.50 0.50",
            "2024-12-30 S LP 1.50 -",
            "2025-01-01 L LP 6.90 -",
            "2024-12-31 S MR 1.50 0.50",
        ]
        self.assertEqual(results, expected_results)

    def test_apply_discount_invalid_transaction(self):
        transactions = [
            ["invalid transaction data", "0", "0"],
            Transaction("2024-12-01", "S", "LP"),
        ]

        results = apply_discount(transactions)

        self.assertEqual(results[0], "invalid transaction data 0 0 Ignored")
        self.assertEqual(results[1], "2024-12-01 S LP 1.50 -")


if __name__ == "__main__":
    unittest.main()
