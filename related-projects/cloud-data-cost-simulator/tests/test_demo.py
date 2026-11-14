import copy
import json
from pathlib import Path
import unittest
from main import run


class DemoTests(unittest.TestCase):
    def test_business_result(self):
        data = json.loads(Path('sample.json').read_text())
        original = copy.deepcopy(data)
        result = run(data)
        self.assertEqual(result['scenarios'][0]['monthly_total'],'430.00')
        self.assertEqual(result['scenarios'][1]['monthly_total'],'269.50')
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        data['assumptions']['scan_tb'] = 0
        self.assertEqual(run(data)['scenarios'][0]['monthly_total'], '280.00')
        data['assumptions']['scan_tb'] = -1
        with self.assertRaises(ValueError):
            run(data)


if __name__ == '__main__':
    unittest.main()
