"""Retail Star Schema Warehouse. Synthetic portfolio demonstration."""
import sqlite3

def run(data):
    with sqlite3.connect(':memory:') as db:
        db.execute('PRAGMA foreign_keys=ON')
        db.executescript("""CREATE TABLE customer(id TEXT PRIMARY KEY,region TEXT);
          CREATE TABLE product(id TEXT PRIMARY KEY,category TEXT);
          CREATE TABLE sales(id TEXT PRIMARY KEY,customer_id TEXT REFERENCES customer(id),
          product_id TEXT REFERENCES product(id),cents INTEGER CHECK(cents>=0));""")
        for row in data['sales']:
            db.execute('INSERT OR IGNORE INTO customer VALUES(?,?)',(row['customer'],row['region']))
            db.execute('INSERT OR IGNORE INTO product VALUES(?,?)',(row['product'],row['category']))
            db.execute('INSERT INTO sales VALUES(?,?,?,?)',(row['id'],row['customer'],row['product'],row['cents']))
        totals = db.execute("""SELECT c.region,p.category,SUM(f.cents) FROM sales f
          JOIN customer c ON c.id=f.customer_id JOIN product p ON p.id=f.product_id
          GROUP BY c.region,p.category ORDER BY c.region,p.category""").fetchall()
        return {'grain':'one row per sale', 'totals':[list(r) for r in totals]}



if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path(__file__).with_name('sample.json'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run(json.loads(args.input.read_text()))
    serialized = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    if args.output:
        args.output.write_text(serialized + '\n')
    else:
        print(serialized)
