# Backend shipment discount calculation module.

Program description
----------------------------
The module processes shipment transactions from an input file, calculates discounts, and outputs the results to the screen.

Features
----------------------------

* Supports shipments via **`Mondial Relay` (MR)** and **`La Poste` (LP)**.
* Processes shipment sizes: **S (Small), M (Medium), L (Large)**.
* Implements discount rules:
  - All **S** shipments match the lowest available **S** package price.
  - The **third L shipment via LP** in a calendar month is free (once per month).
  - Discounts cannot exceed **10€ per calendar month**.
* Ignores invalid or unrecognized input lines.
* Designed for flexibility to allow adding or modifying rules easily.

Input format
----------------------------
The program reads transactions from a file named `input.txt`. Each line contains:
```
YYYY-MM-DD <Package Size> <Carrier Code>
```
Example:

```
2015-02-01 S MR
2015-02-02 S MR
2015-02-03 L LP
2015-02-05 S LP
2015-02-06 S MR
2015-02-06 L LP
2015-02-09 L LP
2015-02-29 CUSPS
2015-03-01 S MR
```

Output format
----------------------------
The output is printed to the console in the following format:

```
YYYY-MM-DD <Package Size> <Carrier Code> <Final Price> <Discount Applied>
```

If the input line is invalid, it is marked as `Ignored`.

Example Output:

```
2015-02-01 S MR 1.50 0.50
2015-02-02 S MR 1.50 0.50
2015-02-03 L LP 6.90 -
2015-02-05 S LP 1.50 -
2015-02-06 S MR 1.50 0.50
2015-02-06 L LP 6.90 -
2015-02-09 L LP 0.00 6.90
2015-02-29 CUSPS Ignored
2015-03-01 S MR 1.50 0.50
```

Setup & Usage
----------------------------

### Prerequisites

Ensure that Python is installed on your system, as it is required to run this project.

### Running the Program

1. Clone this repository.
2. Run the program:
     ```sh
     python main.py
     ```
3. The output will be displayed on the screen.