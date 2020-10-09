# PyCont
[![Travis](https://img.shields.io/travis/numpy/numpy/master.svg?label=Travis%20CI)](
    https://travis-ci.org/github/AlexeyPichugin/pycont)
[![codecov](https://codecov.io/gh/numpy/numpy/branch/master/graph/badge.svg)](
    https://codecov.io/gh/AlexeyPichugin/pycont)
[![Documentation Status](https://readthedocs.org/projects/pycont/badge/?version=latest)](
  https://pycont.readthedocs.io/en/latest/?badge=latest)

Validate and genereate pythpon objects from templates. 
Library is powered by [Trafaret](https://github.com/Deepwalker/trafaret) and helps to validate and genereate data from template.

# Documentation
https://pycont.readthedocs.io/en/latest/index.html

## Usage
```sh
pip install pycont
```


### Simple data template
```python
>>> from pycont import Template, Contract
>>> import trafaret as t
>>> contract = Contract(Template(t.Int()))
>>> print(contract(42))
42
>>> print(contract('test'))
Traceback (most recent call last):
  ...
ValueError: Invalid value: value can't be converted to int
```

### Simple list template
```python
>>> from pycont import Template, Contract
>>> import trafaret as t
>>> contract = Contract([
...  Template(t.Int())
...])
>>> print(contract([42]))
[42]
>>> print(contract([1, 2, 3, 4, 5]))
[1, 2, 3, 4, 5]
>>> print(contract([1, 2, 3, 'error']))
Traceback (most recent call last):
  ...
ValueError: Invalid value: value can't be converted to int
```

### Static list template
```python
>>> from pycont import Template, Contract
>>> import trafaret as t
>>> contract = Contract([
...  Template(t.Int()),
...  Template(t.String()),
...  Template(t.Float()),
...])
>>> print(contract([42, 'test', 12.5]))
[42, 'test', 12.5]
```

### Dict template
```python
>>> from pycont import Template, Contract
>>> import trafaret as t

>>> contract = Contract(Template(t.Int(), default=42))
>>> print(contract('error'))
42

>>> contract = Contract({
...  'id': Template(t.Int()),
...  'value': Template(t.String()),
...})
# Key 'key' not contains in template
>>> print(contract({'id': 1, 'value': 'test', 'key': None}))
{'id': 1, 'value': 'test'}
```

### Deafult value
`pycont.Template` contains an optional argument `default` (the default type must be valid to Tremplate checker). If the argument is set, then if the check fails, this value will be returned.

```python
>>> from pycont import Template, Contract
>>> import trafaret as t

>>> contract = Contract({
...  'id': Template(t.Int()),
...  'value': Template(t.String(), default='None'),  # 'None' is a string
...})
>>> print(contract({'id': 1, 'key': None}))  # key 'value' is not set
{'id': 1, 'value': 'None'}
```
