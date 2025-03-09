from .models import Rules, Transaction
from collections import defaultdict


def apply_discount(transactions):
    """Apply discount based on rules"""

    # Using this dictionary wouldn't lead to any incorrect behavior
    # for example, when transactions are out of order.
    monthly_transactions = defaultdict(list)
    results = []

    # Using indexing to preserve order of original input
    for index, transaction in enumerate(transactions):
        if not isinstance(transaction, Transaction):
            # Convert invalid lines to a string and append 'Ignored'
            invalid_lines = " ".join(transaction)
            results.append(f"{invalid_lines} Ignored")
            continue

        # Get year and month (for example '2024-12')
        month = transaction.date[:7]
        monthly_transactions[month].append((index, transaction))

    for month, transactions_in_month in monthly_transactions.items():
        # Create a new Rules object for the month
        discount_rules = Rules()

        for index, transaction in transactions_in_month:
            discount = discount_rules.apply_rules(transaction)

            if discount != '-':
                final_price = transaction.price - discount
            else:
                final_price = transaction.price

            # round() does not always produce exactly two decimal places
            # So im converting it to string to format it properly
            final_price_str = f"{final_price:.2f}"
            discount_str = f"{discount:.2f}" if discount != '-' else '-'
            result = (
                f"{transaction.date} "
                f"{transaction.size} "
                f"{transaction.provider} "
                f"{final_price_str} {discount_str}"
            )

            results.insert(index, result)

    return results
