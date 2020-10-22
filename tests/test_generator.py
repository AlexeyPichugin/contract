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

    def test_binary_template(self):
        # Simple values
        template_1 = Template(t.Int())
        template_2 = Template(t.String())
        contract = Contract(template_1 | template_2)
        result = contract(42)
        self.assertEqual(result, 42)
        result = contract('test')
        self.assertEqual(result, 'test')
        with self.assertRaises(ValueError):
            result = contract(['list'])

        # Simple list values
        template_1 = Template(t.Int())
        template_2 = Template(t.String())
        contract = Contract([template_1 | template_2])
        result = contract([1, 2, 3])
        self.assertEqual(result, [1, 2, 3])
        result = contract(['test_1', 'test_2'])
        self.assertEqual(result, ['test_1', 'test_2'])
        result = contract([1, 'test', 3])
        self.assertEqual(result, [1, 'test', 3])

        # Combinated list values
        template_1 = Template(t.Int())
        template_2 = Template(t.String())
        contract = Contract([
            template_1 | template_2,
            template_1,
            template_2
        ])
        result = contract([1, 1, 'test'])
        self.assertEqual(result, [1, 1, 'test'])
        result = contract(['test', 1, 'test'])
        self.assertEqual(result, ['test', 1, 'test'])

        # Dict values
        template = {
            'key': Template(t.String()) | Template(t.Int()),
            'value': Template(t.String()),
        }
        contract = Contract(template)
        result = contract({'key': 'key', 'value': 'test'})
        self.assertEqual(result, {'key': 'key', 'value': 'test'})
        result = contract({'key': 12, 'value': 'test'})
        self.assertEqual(result, {'key': 12, 'value': 'test'})

        template_1 = {
            'key': Template(t.String()),
            'value': Template(t.String()),
        }
        template_2 = {
            'id': Template(t.Int()),
            'value': Template(t.String()),
        }
        contract_1 = Contract(template_1)
        contract_2 = Contract(template_2)
        contract = contract_1 | contract_2
        result = contract({'key': 'key', 'value': 'test'})
        self.assertEqual(result, {'key': 'key', 'value': 'test'})
        result = contract({'id': 42, 'value': 'test'})
        self.assertEqual(result, {'id': 42, 'value': 'test'})

    def test_optional(self):
        contract = Contract({
            'key': Template(t.Int()),
            'value': Template(t.String()),
            'optional': Template(t.String(), optional=True)
        })
        data = {
            'key': 1,
            'value': 'test',
            'optional': 'test',
        }
        result = contract(data)
        self.assertEqual(result, data)
        del data['optional']
        result = contract(data)
        self.assertEqual(result, data)

    def test_complex_dict_value(self):
        contract = Contract({
            'key': Template(t.Int()),
            'value': Template(t.String()),
            'optional': Template(t.String(), optional=True),
            'property': [Template(t.String())],
            'optional_property': [Template(t.String(), optional=True)],
            'objects': [{'id': Template(t.Int()), 'val': Template(t.String())}],
        }, optional_keys=['optional_property'])
        data = {
            'key': 1,
            'value': 'test',
            'optional': 'test',
            'property': ['A', 'B', 'C'],
            'optional_property': ['A', 'B', 'C'],
            'objects': [{'id': 1, 'val': 'test'}, {'id': 2, 'val': 'test'}],
        }
        result = contract(data)
        self.assertEqual(result, data)
        del data['optional_property']
        del data['optional']
        result = contract(data)
        self.assertEqual(result, data)

        del data['objects']
        with self.assertRaises(ValueError):
            result = contract(data)
