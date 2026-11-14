"""SQL Query Plan Lab. Synthetic portfolio demonstration."""
import sqlite3
import time

def run(data):
    if type(data['rows']) is not int or not 1 <= data['rows'] <= 1000000:
        raise ValueError('rows must be between 1 and 1000000')
    with sqlite3.connect(':memory:') as db:
        db.execute('CREATE TABLE sales(customer INTEGER, cents INTEGER)')
        db.executemany('INSERT INTO sales VALUES(?,?)',((i%100,i%1000) for i in range(data['rows'])))
        query = 'SELECT SUM(cents) FROM sales WHERE customer=?'
        def measure():
            plan = [r[3] for r in db.execute('EXPLAIN QUERY PLAN '+query,(data['customer'],))]
            start = time.perf_counter()
            total = db.execute(query,(data['customer'],)).fetchone()[0]
            return {'plan':plan,'total_cents':total,'seconds':time.perf_counter()-start}
        before = measure()
        db.execute('CREATE INDEX sales_customer_cents ON sales(customer,cents)')
        after = measure()
        return {'before':before,'after':after,'results_equal':before['total_cents']==after['total_cents']}



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
