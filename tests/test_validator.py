from pycont import Contract, Template, TemplateError

import unittest
import trafaret as t


class TestValidator(unittest.TestCase):
    def test_template(self):
        with self.assertRaises(ValueError):
            template = Template('error')

        trafaret = t.String()
        template = Template(trafaret)
        self.assertEqual(template.template, [trafaret])
        template.check('test')
        with self.assertRaises(ValueError):
            template.check(42)

        template.template = t.Int()
        template.check(42)

        del template.template
        with self.assertRaises(ValueError):
            template.check('test')

    def test_default(self):
        trafaret = t.String()
        template = Template(trafaret, 'null')
        self.assertEqual(template.default, 'null')
        template.default = 'new'
        self.assertEqual(template.default, 'new')

        with self.assertRaises(ValueError):
            template.default = 42

        del template.template
        with self.assertRaises(ValueError):
            template.default = 42

        del template.default
        self.assertIsNone(template.default)

    def test_simple_validator(self):
        # Create contract
        trafaret = t.Trafaret()
        template = Template(trafaret)
        contract = Contract(template)
        self.assertEqual(contract.template, template)
        new_template = Template(trafaret)
        contract.template = new_template
        self.assertEqual(contract.template, new_template)

        # Int
        int_t = Template(t.Int())
        contract = Contract(int_t)

        # String
        string_t = Template(t.String())
        contract = Contract(string_t)

        # Dict
        dict_t = Template(t.Dict({
            'id': t.Int,
            'email': t.Email
        }))
        contract.template = dict_t

        # List
        list_t = Template(t.List(t.Int))
        contract.template = list_t

    def test_list_validator(self):
        list_t = [
            Template(t.Int()),
            Template(t.List(t.Int)),
            Template(t.Dict({'id': t.Int, 'val': t.String})),
        ]
        contract = Contract(list_t)

        list_t = [
            Template(t.Int()),
            'error',
            Template(t.Dict({'id': t.Int, 'val': t.String})),
        ]
        with self.assertRaises(ValueError):
            contract.template = list_t
        with self.assertRaises(ValueError):
            contract = Contract(list_t)

    def test_dict_validator(self):
        dict_t = {
            'id': Template(t.Int(gt=0)),
            'val': Template(t.String()),
        }
        contract = Contract(dict_t)

        dict_t = {
            'id': Template(t.Int(gt=0)),
            'val': 'error',
        }
        with self.assertRaises(ValueError):
            contract.template = dict_t
        with self.assertRaises(ValueError):
            contract = Contract(dict_t)

        dict_t = {
            12: Template(t.Int(gt=0)),
            'val': 'error',
        }
        with self.assertRaises(TypeError):
            contract = Contract(dict_t)

    def test_binary_templates(self):
        tempalte_1 = Template(t.Int())
        tempalte_2 = Template(t.String())
        contract = Contract(tempalte_1 | tempalte_2)
        result = contract(42)
        self.assertEqual(result, 42)
        result = contract('test')
        self.assertEqual(result, 'test')
        with self.assertRaises(ValueError):
            result = contract([123])

        tempalte_1 = Template(t.Int(), default=42)
        tempalte_2 = Template(t.String(), default='Test')
        with self.assertRaises(TemplateError):
            tempalte = tempalte_1 | tempalte_2

        tempalte_1 = Template(t.Int(), default=42)
        tempalte_2 = Template(t.String())
        tempalte = tempalte_1 | tempalte_2  # noqa

        tempalte_1 = Template(t.Int())
        tempalte_2 = Template(t.String(), default='Test')
        tempalte = tempalte_1 | tempalte_2  # noqa
