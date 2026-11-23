import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import analyzer

ROWS = [
    {"date": "2025-01-05", "product": "A", "region": "N", "quantity": 2, "unit_price": 100.0},
    {"date": "2025-01-20", "product": "B", "region": "S", "quantity": 1, "unit_price": 50.0},
    {"date": "2025-02-02", "product": "A", "region": "N", "quantity": 1, "unit_price": 100.0},
]


class AnalyzerTests(unittest.TestCase):
    def test_total(self):
        self.assertEqual(analyzer.total_revenue(ROWS), 350)

    def test_group_sorted_desc(self):
        self.assertEqual(list(analyzer.group_revenue(ROWS, "product").items()), [("A", 300), ("B", 50)])

    def test_monthly(self):
        self.assertEqual(analyzer.monthly_revenue(ROWS), {"2025-01": 250, "2025-02": 100})

    def test_empty_stats(self):
        self.assertEqual(analyzer.order_stats([])["count"], 0)

    def test_load_skips_bad_rows(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
            f.write("date,product,region,quantity,unit_price\n2025-01-01,A,N,2,10\n2025-01-02,B,S,oops,5\n")
        rows = analyzer.load_sales(f.name)
        os.unlink(f.name)
        self.assertEqual(len(rows), 1)


if __name__ == "__main__":
    unittest.main()
