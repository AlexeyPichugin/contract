List template
=============

One element list template
-------------------------

If you set in ``Contract`` list of one ``Template`` you can validate all types in dinamic lengths list.

.. code-block:: python

    >>> from contract import Template, Contract
    >>> import trafaret as t
    >>> contract = Contract([Template(t.Int())])
    >>> print(contract([42]))
    [42]
    >>> print(contract([1, 2, 3, 4, 5]))
    [1, 2, 3, 4, 5]
    >>> print(contract([1, 2, 3, 'error']))
    Traceback (most recent call last):
    ValueError: Invalid value: value can't be converted to int

One element list template with default
--------------------------------------

If set default value you can change all invalid element to this

.. code-block:: python

    >>> from contract import Template, Contract
    >>> import trafaret as t

    >>> template = Template(t.Int(), default=0)
    >>> contract = Contract([template])
    >>> print(contract([1, 'a', 2, 'b', 3]))
    [1, 0, 2, 0, 3]

Static lengths list
-------------------

If Contract list contains 2 or more element, the data is checked for length.
If one of the elements is invalid or the length does not match, throw a ValueError exceptionю

.. code-block:: python

    >>> from contract import Template, Contract
    >>> import trafaret as t
    >>> contract = Contract([
    ...  Template(t.Int()),
    ...  Template(t.String()),
    ...  Template(t.Float()),
    ... ])
    >>> print(contract([42, 'test', 12.5]))
    [42, 'test', 12.5]

    >>> print(contract(['error', 'test', 12.5]))
    Traceback (most recent call last):
    ValueError: Invalid value: value can't be converted to int

    >>> print(contract([1', 'test', 12.5, 'error']))
    Traceback (most recent call last):
    ValueError: Invalid value: Invalid value length
