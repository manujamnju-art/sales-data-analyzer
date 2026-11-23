"""Sales Data Analyzer: loads a CSV and produces summary statistics."""
import csv
import statistics
from collections import defaultdict


def load_sales(path):
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            try:
                rows.append({
                    "date": r["date"],
                    "product": r["product"],
                    "region": r["region"],
                    "quantity": int(r["quantity"]),
                    "unit_price": float(r["unit_price"]),
                })
            except (KeyError, ValueError):
                continue  # skip malformed rows
    return rows


def revenue(row):
    return row["quantity"] * row["unit_price"]


def total_revenue(rows):
    return sum(revenue(r) for r in rows)


def group_revenue(rows, key):
    totals = defaultdict(float)
    for r in rows:
        totals[r[key]] += revenue(r)
    return dict(sorted(totals.items(), key=lambda kv: -kv[1]))


def monthly_revenue(rows):
    totals = defaultdict(float)
    for r in rows:
        totals[r["date"][:7]] += revenue(r)
    return dict(sorted(totals.items()))


def order_stats(rows):
    values = [revenue(r) for r in rows]
    if not values:
        return {"count": 0, "mean": 0, "median": 0, "max": 0}
    return {
        "count": len(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "max": max(values),
    }


def bar(value, maximum, width=30):
    return "#" * int(width * value / maximum) if maximum else ""


def print_report(rows):
    print("=" * 52)
    print(f"SALES REPORT  |  total revenue: {total_revenue(rows):,.0f}")
    print("=" * 52)
    s = order_stats(rows)
    print(f"Orders: {s['count']}  Mean: {s['mean']:,.0f}  Median: {s['median']:,.0f}  Max: {s['max']:,.0f}")
    for title, key in (("By product", "product"), ("By region", "region")):
        print(f"\n{title}")
        data = group_revenue(rows, key)
        top = max(data.values())
        for name, val in data.items():
            print(f"  {name:<11}{val:>12,.0f}  {bar(val, top)}")
    print("\nMonthly trend")
    monthly = monthly_revenue(rows)
    top = max(monthly.values())
    for month, val in monthly.items():
        print(f"  {month}  {val:>12,.0f}  {bar(val, top)}")


if __name__ == "__main__":
    import sys
    print_report(load_sales(sys.argv[1] if len(sys.argv) > 1 else "sales.csv"))
