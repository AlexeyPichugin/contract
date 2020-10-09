Simple value
============


Check simple value
------------------

PyCont can validate simple value. 
All Template validators you can read in `Trafaret dock`_

.. code-block:: python

    >>> from pycont import Template, Contract
    >>> import trafaret as t
    >>> contract = Contract(Template(t.Int()))
    >>> print(contract(42))
    42
    >>> print(contract('test'))
    Traceback (most recent call last):
    ValueError: Invalid value: value can't be converted to int

.. _Trafaret dock: https://trafaret.readthedocs.io/en/latest/

Check value with default
------------------------
You can set a default value used ``Template.default``. This value will be returned if input data is invalid.

.. code-block:: python

    >>> from pycont import Template, Contract
    >>> import trafaret as t
    >>> contract = Contract(Template(t.Int(), default=0))
    >>> print(contract(42))
    42
    >>> print(contract('test'))
    0

