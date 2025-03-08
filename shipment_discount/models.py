import datetime
from .config import (VALID_PROVIDERS,
                     VALID_SIZES,
                     MONTHLY_DISCOUNT_LIMIT, PRICES)


class Transaction:

    def __init__(self, date, size, provider):
        self.date = date
        self.size = size
        self.provider = provider
        self.price = self.shipping_price()

    def shipping_price(self):
        return PRICES.get(self.provider).get(self.size)

    @classmethod
    def is_valid(cls, data):
        """Validate the transaction"""
        try:
            return (
                    len(data) == 3 and
                    datetime.date.fromisoformat(data[0]) and
                    data[1] in VALID_SIZES and
                    data[2] in VALID_PROVIDERS
            )
        except ValueError:
            return False


class Rules:
    def __init__(self):
        # Track total discounts used in the month
        self.monthly_discount_used = 0
        # Track L shipments of LP provider
        self.lp_large_shipment_count = 0
        # Get the lowest S price among all providers
        self.lowest_s_price = min(
            PRICES[provider]['S']
            for provider in VALID_PROVIDERS
        )

    def apply_rules(self, transaction):
        """Apply all discount rules"""
        discount = 0
        no_discount = '-'

        # Rule 1: The third L shipment via LP is free, but only once a month.
        discount += self._rule_free_lp_shipment(transaction)

        # Rule 2: S shipments should always match the lowest S package price.
        discount += self._rule_lowest_s_price(transaction)

        # Ensure that the total discount doesn’t exceed the monthly limit.
        discount = min(discount,
                       MONTHLY_DISCOUNT_LIMIT - self.monthly_discount_used)
        self.monthly_discount_used += discount

        return discount if discount > 0 else no_discount

    def _rule_free_lp_shipment(self, transaction):
        """Rule: The third L shipment via LP is free, but only once a month."""
        if transaction.size == 'L' and transaction.provider == 'LP':
            self.lp_large_shipment_count += 1
            if self.lp_large_shipment_count == 3:
                # Ensure that this discount doesn’t exceed the monthly limit
                # to catch potential issues with the discount earlier
                return min(transaction.price,
                           MONTHLY_DISCOUNT_LIMIT - self.monthly_discount_used)
        return 0

    def _rule_lowest_s_price(self, transaction):
        """Rule: S shipments should always match the lowest S package price."""
        if transaction.size == 'S':
            return max(0, transaction.price - self.lowest_s_price)
        return 0
