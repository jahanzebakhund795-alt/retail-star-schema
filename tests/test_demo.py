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
        self.assertEqual(result['totals'], [['East','Tools',800],['West','Books',500],['West','Tools',1200]])
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        data['sales'] = []
        self.assertEqual(run(data)['totals'], [])
        data['sales'] = [{'id':'x','customer':'c','region':'R','product':'p','category':'C','cents':-1}]
        with self.assertRaises(Exception):
            run(data)


if __name__ == '__main__':
    unittest.main()
