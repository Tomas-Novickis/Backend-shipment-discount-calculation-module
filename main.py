import pathlib
from file_reader import read_transactions_from_file
from discount_calculation import apply_discount


def main():
    transactions = read_transactions_from_file(pathlib.Path("input.txt"))
    results = apply_discount(transactions)

    for result in results:
        print(result)


if __name__ == "__main__":
    main()
