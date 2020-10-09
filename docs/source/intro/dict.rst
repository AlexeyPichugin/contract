Dict template
=============

Simple dict template
--------------------

You can create dict tempalte. Dict template must be ``Dict[str, Template]``.

.. code-block:: python

    >>> from contract import Template, Contract
    >>> import trafaret as t

    >>> contract = Contract(Template(t.Int(), default=42))
    >>> print(contract('error'))
    42

    >>> contract = Contract({
    ...  'id': Template(t.Int()),
    ...  'value': Template(t.String()),
    ... })
    # Key 'key' not contains in template
    >>> print(contract({'id': 1, 'value': 'test', 'key': None}))
    {'id': 1, 'value': 'test'}

Contract check thet all template keys contains in input data. If one of them is missing, then frow ValueError.
If data contains more key they will be ignored.

Default value
-------------

If you set the default value, the invalid data will change to it. 
If the key is not set in the data, and the template has a default value, then the input contains this key with this value.

.. code-block:: python

    >>> from contract import Template, Contract
    >>> import trafaret as t

    >>> contract = Contract({
    ...  'id': Template(t.Int()),
    ...  'value': Template(t.String(), default='None'),  # 'None' is a string
    ... })
    >>> print(contract({'id': 1, 'key': None}))  # key 'value' is not set
    {'id': 1, 'value': 'None'}

Complex dict
------------

You can create a complex template for data validation like json

.. code-block:: python

    >>> contract = Contract({
    ...    'id': Template(t.Int(gt=0)),
    ...    'name': Template(t.String(min_length=5, max_length=20)),
    ...    'email': Template(t.Email),
    ...    'properties': [
    ...        Template(t.String())
    ...    ],
    ...    'urls': [{
    ...        'host': Template(t.String()),
    ...        'port': Template(t.Int(gt=0, lt=65535)),
    ...    }]
    ... })
    >>> print(contract({
    ...    'id': 10,
    ...    'name': 'Vasya',
    ...    'email': 'vasya@test.com',
    ...    'properties': ['dev', 'qa'],
    ...    'urls': [
    ...        {'host': '127.0.0.1', 'port': 80},
    ...        {'host': '127.0.0.1', 'port': 443},
    ...    ]
    ... }))
    {'id': 10, 'name': 'Vasya', 'email': 'vasya@test.com', 'properties': ['dev', 'qa'], 'urls': [{'host': '127.0.0.1', 'port': 80}, {'host': '127.0.0.1', 'port': 443}]}

