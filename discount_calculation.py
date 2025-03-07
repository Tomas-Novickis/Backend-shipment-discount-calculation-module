from models import Rules, Transaction


def apply_discount(transactions):
    """Apply discount based on rules"""
    discount_rules = None
    current_month = None
    results = []
    for transaction in transactions:
        if not isinstance(transaction, Transaction):
            # Convert invalid lines to a string and append 'Ignored'
            invalid_lines = " ".join(transaction)
            results.append(f"{invalid_lines} Ignored")
            continue
    # Get year and month (for example '2024-12')
        month = transaction.date[:7]
        if month != current_month:
            # Rules() object is created when we are in the next month,
            # to ensure that discount is updated
            discount_rules = Rules()
            current_month = month

        discount = discount_rules.discount_rules(transaction)
        if discount != '-':
            final_price = transaction.price - discount
        else:
            final_price = transaction.price
        # round() in Python does not always produce exactly two decimal places
        # so im converting it to string to format it properly
        final_price_str = f"{final_price:.2f}"
        discount_str = f"{discount:.2f}" if discount != '-' else '-'
        results.append(
            f"{transaction.date} "
            f"{transaction.size} "
            f"{transaction.provider} "
            f"{final_price_str} {discount_str}"
        )
    return results
