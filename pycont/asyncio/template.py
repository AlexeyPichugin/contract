from trafaret import DataError
from typing import Any

from pycont import Template


class AsyncTemplate(Template):
    """
    Template object to validate on contract class
    May contain a default value returned if the data is invalid

    Args:
        template trafarer.Trafaret objects or subclass:
            The template for checking value
        default Optional[Any] = None:
            The default value returned if the data is invalid
            The default value type mast be valid for the template object

        >>> from pycont import Contract, Template
        >>> import trafaret as t
        >>> contract = Contract(Template(t.Int()))
    """
    async def check(self, value: Any):
        """
        Check if value is valid by template

        Raises:
            ValueError if template is not set
            trafaret.DataError if value is not valid
        """
        if self._template is None:
            raise ValueError("Template not set")
        errors = []
        for template in self._template:
            try:
                await template.async_check(value)
            except DataError as e:
                errors.append(e.error)
            else:
                return
        raise DataError(error='\n'.join(errors))
