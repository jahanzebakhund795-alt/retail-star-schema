"""Warehouse Migration Reconciler. Synthetic portfolio demonstration."""
import hashlib
import json

def keyed(rows):
    output = {}
    for row in rows:
        if row['id'] in output:
            raise ValueError('Duplicate primary key')
        output[row['id']] = row
    return output

def digest(row):
    return hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def run(data):
    source,target = keyed(data['source']),keyed(data['target'])
    changed = []
    for key in sorted(source.keys() & target.keys()):
        if digest(source[key]) != digest(target[key]):
            fields = sorted(k for k in source[key].keys() | target[key].keys()
                            if (k in source[key]) != (k in target[key]) or source[key].get(k) != target[key].get(k))
            changed.append({'id':key,'fields':fields})
    missing,extra = sorted(source.keys()-target.keys()),sorted(target.keys()-source.keys())
    return {'matched':not (missing or extra or changed),'missing':missing,'extra':extra,'changed':changed}



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
