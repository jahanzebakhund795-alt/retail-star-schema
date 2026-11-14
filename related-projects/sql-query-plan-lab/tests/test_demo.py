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
        self.assertTrue(result['results_equal'])
        self.assertIn('SCAN',str(result['before']['plan']))
        self.assertIn('INDEX',str(result['after']['plan']))
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        self.assertIsNone(run({'rows':10,'customer':999})['after']['total_cents'])
        with self.assertRaises(ValueError):
            run({'rows':0,'customer':1})


if __name__ == '__main__':
    unittest.main()
