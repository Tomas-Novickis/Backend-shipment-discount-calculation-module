import logging
from .models import Transaction


def read_transactions_from_file(file_path):
    transactions = []
    try:
        with file_path.open() as file:
            for line in file:
                separated_members = line.split()

                if Transaction.is_valid(separated_members):

                    transaction = Transaction(separated_members[0],
                                              separated_members[1],
                                              separated_members[2])
                    transactions.append(transaction)
                else:
                    transactions.append(separated_members)
    except OSError as error:
        logging.error("Reading from file %s failed due to: %s",
                      file_path, error)

    return transactions
