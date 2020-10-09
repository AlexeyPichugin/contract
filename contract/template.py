from trafaret import Trafaret, DataError
from typing import Any, Optional


class Template():
    """
    Template object to validate on contract class
    May contain a default value returned if the data is invalid

    Args:
        template trafarer.Trafaret objects or subclass:
            The template for checking value
        default Optional[Any] = None:
            The default value returned if the data is invalid
            The default value type mast be valid for the template object

    >>> from contract import Contract, Template
    >>> import trafaret as t
    >>> contract = Contract(Template(t.Int()))
    """
    def __init__(self, template: Trafaret, default: Optional[Any] = None):
        self._validate_template(template)
        self._template = template

        if default is not None:
            self._validate_default(default)
        self._default = default

    template = property()

    @template.getter
    def template(self) -> Trafaret:
        """
        Get current template

        Return:
            trafaret.Trafaret: current template
        """
        return self._template

    @template.setter
    def template(self, template: Trafaret) -> None:
        """
        Validate new trafaret object
        Args:
            template: trafarer.Trafaret objects or subclass
        """
        self._validate_template(template)
        self._template = template

    @template.deleter
    def template(self):
        """
        Delete old template
        """
        self._template = None

    def _validate_template(self, template: Trafaret) -> None:
        """
        Check if template is valid for work
        """
        if not isinstance(template, Trafaret):
            raise ValueError(f'Template type must be trafaret.Trafaret, not {type(template)}')

    default = property()

    @default.getter
    def default(self) -> Trafaret:
        """
        Get current default value
        """
        return self._default

    @default.setter
    def default(self, default: Any) -> None:
        """
        Validate and set new default value
        Args:
            default Any:
                The default value returned if the data is invalid
                The default value type mast be valid for the template object
        """
        self._validate_default(default)
        self._default = default

    @default.deleter
    def default(self):
        """
        Delete default value
        """
        self._default = None

    def _validate_default(self, default):
        """
        Check if default value is valid
        Raises:
            ValueError if template is not set
            trafaret.DataError if value is not valid
        """
        if self._template is not None:
            self._template.check(default)
            return
        raise ValueError("Template not set")

    def check(self, value: Any):
        """
        Check if value is valid by template
        Raises:
            ValueError if template is not set
            trafaret.DataError if value is not valid
        """
        if self._template is None:
            raise ValueError("Template not set")
        try:
            self._template.check(value)
        except DataError as e:
            raise e
