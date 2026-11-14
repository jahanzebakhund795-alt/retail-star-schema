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
        self.assertFalse(result['matched'])
        self.assertEqual(result['missing'],['3'])
        self.assertEqual(result['changed'],[{'id':'2','fields':['cents']}])
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        data['target'] = copy.deepcopy(data['source'])
        self.assertTrue(run(data)['matched'])
        data['target'].append(copy.deepcopy(data['target'][0]))
        with self.assertRaises(ValueError):
            run(data)


if __name__ == '__main__':
    unittest.main()
