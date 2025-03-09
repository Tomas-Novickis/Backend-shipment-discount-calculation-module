import unittest
from unittest.mock import mock_open, patch
import pathlib
from shipment_discount import read_transactions_from_file, Transaction


class TestFileReader(unittest.TestCase):

    def test_read_valid_transactions(self):
        data = ("2024-12-01 S MR\n"
                "2024-12-01 L LP\n"
                "2024-12-01 M MR\n")
        with patch("pathlib.Path.open", mock_open(read_data=data)):
            transactions = read_transactions_from_file(
                pathlib.Path("fake_path"))

        self.assertEqual(len(transactions), 3)

        self.assertIsInstance(transactions[0], Transaction)
        self.assertEqual(transactions[0].provider, 'MR')

    def test_read_invalid_transactions(self):
        mock_file_content = ("invalid data\n"
                             "2024-12-01 S MR\n"
                             "invalid transaction\n")

        with patch("pathlib.Path.open", mock_open(
                read_data=mock_file_content)):
            transactions = read_transactions_from_file(
                pathlib.Path("fake_path"))

        self.assertEqual(len(transactions), 3)
        self.assertEqual(transactions[0], ["invalid", "data"])
        self.assertIsInstance(transactions[1], Transaction)

    def test_file_reading_error(self):
        with patch("pathlib.Path.open", side_effect=OSError("File not found")):
            with self.assertLogs(level="ERROR") as log:
                read_transactions_from_file(
                    pathlib.Path("fake_path"))

                self.assertIn("ERROR:root:"
                              "Reading from file fake_path failed due to: "
                              "File not found",
                              log.output)

    def test_empty_file(self):
        data = ""

        with patch("pathlib.Path.open", mock_open(read_data=data)):
            transactions = read_transactions_from_file(
                pathlib.Path("fake_path"))

        self.assertEqual(len(transactions), 0)


if __name__ == '__main__':
    unittest.main()
