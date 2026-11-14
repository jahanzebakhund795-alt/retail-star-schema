"""Cloud Data Cost Simulator. Synthetic portfolio demonstration."""
from decimal import Decimal, ROUND_HALF_UP

def number(value):
    result = Decimal(str(value))
    if not result.is_finite() or result < 0:
        raise ValueError('Assumptions and rates must be finite and nonnegative')
    return result

def money(value):
    return str(value.quantize(Decimal('0.01'),rounding=ROUND_HALF_UP))

def run(data):
    usage = data['assumptions']
    output = []
    for scenario in data['scenarios']:
        storage = number(usage['storage_gb'])*number(scenario['storage_per_gb'])
        compute = number(usage['compute_hours'])*number(scenario['compute_per_hour'])*number(scenario.get('compute_multiplier',1))
        scan = number(usage['scan_tb'])*number(scenario['scan_per_tb'])*number(scenario.get('scan_multiplier',1))
        output.append({'name':scenario['name'],'storage':money(storage),'compute':money(compute),
                       'scan':money(scan),'monthly_total':money(storage+compute+scan)})
    return {'pricing':'invented user-editable assumptions; not provider quotes','scenarios':output}



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
