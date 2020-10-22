from pycont import AsyncTemplate, AsyncContract
import unittest
import asyncio
import trafaret as t


class TestGenerators(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.get_event_loop()

    @classmethod
    def tearDownClass(cls):
        cls.loop.close()

    def test_simple_value(self):
        template = AsyncTemplate(t.Int())
        contract = AsyncContract(template)
        result = self.loop.run_until_complete(contract.__call__(42))
        self.assertEqual(result, 42)

        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract.__call__('error'))

        del template.template
        with self.assertRaises(ValueError):
            self.loop.run_until_complete(template.check('test'))

    def test_simple_value_with_default(self):
        template = AsyncTemplate(t.Int(), default=7)
        contract = AsyncContract(template)
        result = self.loop.run_until_complete(contract(42))
        self.assertEqual(result, 42)

        result = self.loop.run_until_complete(contract('error'))
        self.assertEqual(result, 7)

    def test_list_single_value(self):
        template = AsyncTemplate(t.Int())
        contract = AsyncContract([template])
        result = self.loop.run_until_complete(contract([42]))
        self.assertEqual(result, [42])

        result = self.loop.run_until_complete(contract([8, 800, 555, 35, 35]))
        self.assertEqual(result, [8, 800, 555, 35, 35])

        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract([8, 800, 555, 'error', 35]))
        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract(42))

    def test_list_single_value_with_default(self):
        template = AsyncTemplate(t.Int(), 42)
        contract = AsyncContract([template])

        result = self.loop.run_until_complete(contract([8, 800, 555, 35, 35]))
        self.assertEqual(result, [8, 800, 555, 35, 35])

        result = self.loop.run_until_complete(contract([8, 800, 555, 'error', 35]))
        self.assertEqual(result, [8, 800, 555, 42, 35])

    def test_list_many_values(self):
        contract = AsyncContract([
            AsyncTemplate(t.Int()),
            AsyncTemplate(t.String()),
            AsyncTemplate(t.Float())
        ])
        result = self.loop.run_until_complete(contract([1, 'Test', 12.5]))
        self.assertEqual(result, [1, 'Test', 12.5])

        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract(['error', 'Test', 12.5]))
        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract([1, 666, 12.5]))
        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract([1, 'Test', 'error']))
        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract([1, 'Test']))
        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract([1, 'Test', 12.5, 'error']))
        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract(42))

    def test_list_many_values_with_default(self):
        contract = AsyncContract([
            AsyncTemplate(t.Int(), 42),
            AsyncTemplate(t.String(), 'null'),
            AsyncTemplate(t.Float(), 1.5)
        ])
        result = self.loop.run_until_complete(contract([1, 'Test', 12.5]))
        self.assertEqual(result, [1, 'Test', 12.5])

        result = self.loop.run_until_complete(contract(['error', 'Test', 12.5]))
        self.assertEqual(result, [42, 'Test', 12.5])
        result = self.loop.run_until_complete(contract([1, 666, 12.5]))
        self.assertEqual(result, [1, 'null', 12.5])
        result = self.loop.run_until_complete(contract([1, 'Test', 'error']))
        self.assertEqual(result, [1, 'Test', 1.5])
        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract([1, 'Test']))
        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract([1, 'Test', 12.5, 'error']))
        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract(42))

    def test_dict_value(self):
        contract = AsyncContract({
            'id': AsyncTemplate(t.Int()),
            'value': AsyncTemplate(t.String()),
        })
        result = self.loop.run_until_complete(contract({'id': 42, 'value': 'test'}))
        self.assertEqual(result, {'id': 42, 'value': 'test'})
        result = self.loop.run_until_complete(contract({'id': 42, 'value': 'test', 'key': 666}))
        self.assertEqual(result, {'id': 42, 'value': 'test'})

        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract({'id': 'error', 'value': 'test'}))
        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract({'id': 42, 'value': 666}))
        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract({'id': 1}))
        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract(666))

    def test_dict_value_with_default(self):
        contract = AsyncContract({
            'id': AsyncTemplate(t.Int(), 99),
            'value': AsyncTemplate(t.String(), 'null'),
        })
        result = self.loop.run_until_complete(contract({'id': 42, 'value': 'test'}))
        self.assertEqual(result, {'id': 42, 'value': 'test'})
        result = self.loop.run_until_complete(contract({'id': 42, 'value': 'test', 'key': 666}))
        self.assertEqual(result, {'id': 42, 'value': 'test'})

        result = self.loop.run_until_complete(contract({'id': 'error', 'value': 'test'}))
        self.assertEqual(result, {'id': 99, 'value': 'test'})
        result = self.loop.run_until_complete(contract({'id': 42, 'value': 666}))
        self.assertEqual(result, {'id': 42, 'value': 'null'})
        result = self.loop.run_until_complete(contract({'id': 99}))
        self.assertEqual(result, {'id': 99, 'value': 'null'})
        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract(666))

    def test_binary_template(self):
        # Simple values
        template_1 = AsyncTemplate(t.Int())
        template_2 = AsyncTemplate(t.String())
        contract = AsyncContract(template_1 | template_2)
        result = self.loop.run_until_complete(contract(42))
        self.assertEqual(result, 42)
        result = self.loop.run_until_complete(contract('test'))
        self.assertEqual(result, 'test')
        with self.assertRaises(ValueError):
            result = self.loop.run_until_complete(contract(['list']))

        # Simple list values
        template_1 = AsyncTemplate(t.Int())
        template_2 = AsyncTemplate(t.String())
        contract = AsyncContract([template_1 | template_2])
        result = self.loop.run_until_complete(contract([1, 2, 3]))
        self.assertEqual(result, [1, 2, 3])
        result = self.loop.run_until_complete(contract(['test_1', 'test_2']))
        self.assertEqual(result, ['test_1', 'test_2'])
        result = self.loop.run_until_complete(contract([1, 'test', 3]))
        self.assertEqual(result, [1, 'test', 3])

        # Combinated list values
        template_1 = AsyncTemplate(t.Int())
        template_2 = AsyncTemplate(t.String())
        contract = AsyncContract([
            template_1 | template_2,
            template_1,
            template_2
        ])
        result = self.loop.run_until_complete(contract([1, 1, 'test']))
        self.assertEqual(result, [1, 1, 'test'])
        result = self.loop.run_until_complete(contract(['test', 1, 'test']))
        self.assertEqual(result, ['test', 1, 'test'])

        # Dict values
        template = {
            'key': AsyncTemplate(t.String()) | AsyncTemplate(t.Int()),
            'value': AsyncTemplate(t.String()),
        }
        contract = AsyncContract(template)
        result = self.loop.run_until_complete(contract({'key': 'key', 'value': 'test'}))
        self.assertEqual(result, {'key': 'key', 'value': 'test'})
        result = self.loop.run_until_complete(contract({'key': 12, 'value': 'test'}))
        self.assertEqual(result, {'key': 12, 'value': 'test'})

        template_1 = {
            'key': AsyncTemplate(t.String()),
            'value': AsyncTemplate(t.String()),
        }
        template_2 = {
            'id': AsyncTemplate(t.Int()),
            'value': AsyncTemplate(t.String()),
        }
        contract_1 = AsyncContract(template_1)
        contract_2 = AsyncContract(template_2)
        contract = contract_1 | contract_2
        result = self.loop.run_until_complete(contract({'key': 'key', 'value': 'test'}))
        self.assertEqual(result, {'key': 'key', 'value': 'test'})
        result = self.loop.run_until_complete(contract({'id': 42, 'value': 'test'}))
        self.assertEqual(result, {'id': 42, 'value': 'test'})

    def test_optional(self):
        contract = AsyncContract({
            'key': AsyncTemplate(t.Int()),
            'value': AsyncTemplate(t.String()),
            'optional': AsyncTemplate(t.String(), optional=True)
        })
        data = {
            'key': 1,
            'value': 'test',
            'optional': 'test',
        }
        result = self.loop.run_until_complete(contract(data))
        self.assertEqual(result, data)
        del data['optional']
        result = self.loop.run_until_complete(contract(data))
        self.assertEqual(result, data)
