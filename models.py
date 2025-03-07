import datetime


class Transaction:
    # Define providers and sizes
    VALID_PROVIDERS = {'LP', 'MR'}
    VALID_SIZES = {'S', 'M', 'L'}

    # Define shipping prices
    PRICES = {
        'LP': {'S': 1.50, 'M': 4.90, 'L': 6.90},
        'MR': {'S': 2.00, 'M': 3.00, 'L': 4.00}
    }

    def __init__(self, date, size, provider):
        self.date = date
        self.size = size
        self.provider = provider
        self.price = self.shipping_price()

    def shipping_price(self):
        return self.PRICES.get(self.provider).get(self.size)

    # Create a class method to call it without creating an instance of class
    @classmethod
    def is_valid(cls, data):
        """Validate the transaction"""
        try:
            return (
                    len(data) == 3 and
                    datetime.date.fromisoformat(data[0]) and
                    data[1] in cls.VALID_SIZES and
                    data[2] in cls.VALID_PROVIDERS
            )
        except ValueError:
            return False


class Rules:
    def __init__(self):
        self.monthly_discount_amount = 0
        self.lp_large_shipment_amount = 0
        self.monthly_limit = 10

    def discount_rules(self, transaction):
        """Count discount based on rules"""
        discount = 0
        no_discount = '-'

        # 1st rule: The third L shipment via LP is free, but only once a month.
        if transaction.size == 'L' and transaction.provider == 'LP':
            self.lp_large_shipment_amount += 1
            if self.lp_large_shipment_amount == 3:
                discount = min(
                    transaction.price,
                    self.monthly_limit - self.monthly_discount_amount
                )
                self.monthly_discount_amount += discount

        # 2nd rule: S shipments should always match the lowest S package price.
        elif transaction.size == 'S':
            # get the lowest S price among all providers
            lowest_s_price = min(
                Transaction.PRICES[provider]['S']
                for provider in Transaction.VALID_PROVIDERS
            )
            # difference between current price and lowest price
            discount = max(0, transaction.price - lowest_s_price)
            discount = min(
                discount,
                self.monthly_limit - self.monthly_discount_amount
            )
            self.monthly_discount_amount += discount

        return discount if discount > 0 else no_discount
