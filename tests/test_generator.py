from pycont import Template, Contract
import unittest
import trafaret as t


class TestGenerators(unittest.TestCase):
    def test_simple_value(self):
        template = Template(t.Int())
        contract = Contract(template)
        result = contract.__call__(42)
        self.assertEqual(result, 42)

        with self.assertRaises(ValueError):
            result = contract('error')

    def test_simple_value_with_default(self):
        template = Template(t.Int(), default=7)
        contract = Contract(template)
        result = contract(42)
        self.assertEqual(result, 42)

        result = contract('error')
        self.assertEqual(result, 7)

    def test_list_single_value(self):
        template = Template(t.Int())
        contract = Contract([template])
        result = contract([42])
        self.assertEqual(result, [42])

        result = contract([8, 800, 555, 35, 35])
        self.assertEqual(result, [8, 800, 555, 35, 35])

        with self.assertRaises(ValueError):
            result = contract([8, 800, 555, 'error', 35])
        with self.assertRaises(ValueError):
            result = contract(42)

    def test_list_single_value_with_default(self):
        template = Template(t.Int(), 42)
        contract = Contract([template])

        result = contract([8, 800, 555, 35, 35])
        self.assertEqual(result, [8, 800, 555, 35, 35])

        result = contract([8, 800, 555, 'error', 35])
        self.assertEqual(result, [8, 800, 555, 42, 35])

    def test_list_many_values(self):
        contract = Contract([
            Template(t.Int()),
            Template(t.String()),
            Template(t.Float())
        ])
        result = contract([1, 'Test', 12.5])
        self.assertEqual(result, [1, 'Test', 12.5])

        with self.assertRaises(ValueError):
            result = contract(['error', 'Test', 12.5])
        with self.assertRaises(ValueError):
            result = contract([1, 666, 12.5])
        with self.assertRaises(ValueError):
            result = contract([1, 'Test', 'error'])
        with self.assertRaises(ValueError):
            result = contract([1, 'Test'])
        with self.assertRaises(ValueError):
            result = contract([1, 'Test', 12.5, 'error'])
        with self.assertRaises(ValueError):
            result = contract(42)

    def test_list_many_values_with_default(self):
        contract = Contract([
            Template(t.Int(), 42),
            Template(t.String(), 'null'),
            Template(t.Float(), 1.5)
        ])
        result = contract([1, 'Test', 12.5])
        self.assertEqual(result, [1, 'Test', 12.5])

        result = contract(['error', 'Test', 12.5])
        self.assertEqual(result, [42, 'Test', 12.5])
        result = contract([1, 666, 12.5])
        self.assertEqual(result, [1, 'null', 12.5])
        result = contract([1, 'Test', 'error'])
        self.assertEqual(result, [1, 'Test', 1.5])
        with self.assertRaises(ValueError):
            result = contract([1, 'Test'])
        with self.assertRaises(ValueError):
            result = contract([1, 'Test', 12.5, 'error'])
        with self.assertRaises(ValueError):
            result = contract(42)

    def test_dict_value(self):
        contract = Contract({
            'id': Template(t.Int()),
            'value': Template(t.String()),
        })
        result = contract({'id': 42, 'value': 'test'})
        self.assertEqual(result, {'id': 42, 'value': 'test'})
        result = contract({'id': 42, 'value': 'test', 'key': 666})
        self.assertEqual(result, {'id': 42, 'value': 'test'})

        with self.assertRaises(ValueError):
            result = contract({'id': 'error', 'value': 'test'})
        with self.assertRaises(ValueError):
            result = contract({'id': 42, 'value': 666})
        with self.assertRaises(ValueError):
            result = contract({'id': 1})
        with self.assertRaises(ValueError):
            result = contract(666)

    def test_dict_value_with_default(self):
        contract = Contract({
            'id': Template(t.Int(), 99),
            'value': Template(t.String(), 'null'),
        })
        result = contract({'id': 42, 'value': 'test'})
        self.assertEqual(result, {'id': 42, 'value': 'test'})
        result = contract({'id': 42, 'value': 'test', 'key': 666})
        self.assertEqual(result, {'id': 42, 'value': 'test'})

        result = contract({'id': 'error', 'value': 'test'})
        self.assertEqual(result, {'id': 99, 'value': 'test'})
        result = contract({'id': 42, 'value': 666})
        self.assertEqual(result, {'id': 42, 'value': 'null'})
        result = contract({'id': 99})
        self.assertEqual(result, {'id': 99, 'value': 'null'})
        with self.assertRaises(ValueError):
            result = contract(666)
