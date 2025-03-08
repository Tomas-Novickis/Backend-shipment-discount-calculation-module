from shipment_discount import (read_transactions_from_file,
                               apply_discount)
import pathlib


def main():
    file_path = pathlib.Path("input.txt")
    transactions = read_transactions_from_file(file_path)
    results = apply_discount(transactions)

    for result in results:
        print(result)


if __name__ == "__main__":
    main()
