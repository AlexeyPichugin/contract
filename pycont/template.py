from trafaret import Trafaret, DataError
from typing import Any, Optional, Union, List, TypeVar


T = TypeVar('Template')


class TemplateError(Exception):
    pass


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
        optional Optional[bool] = False:
            Used only in dictionary contract
            If True, the check function does not raise an error if the key is not set.

        >>> from pycont import Contract, Template
        >>> import trafaret as t
        >>> contract = Contract(Template(t.Int()))
    """
    def __init__(
        self,
        template: Union[Trafaret, List[Trafaret]],
        default: Optional[Any] = None,
        optional: Optional[bool] = False,
    ):
        self._validate_template(template)
        self._template = [template] if isinstance(template, Trafaret) else template
        self.optional = optional

        if default is not None:
            self._validate_default(default)
        self._default = default

    def __or__(self, other: T):
        if self.default is not None and other.default is not None:
            raise TemplateError('Both templates cannot have default values')
        self.template = self.template + other.template
        self.default = self.default or other.default
        return self

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
    def template(self, template: Union[Trafaret, List[Trafaret]]) -> None:
        """
        Validate new trafaret object
        Args:
            template: trafarer.Trafaret objects or subclass
        """
        self._validate_template(template)
        self._template = [template] if isinstance(template, Trafaret) else template

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
            try:
                for tmp in template:
                    if not isinstance(tmp, Trafaret):
                        raise ValueError(f'Template type must be trafaret.Trafaret, not {type(template)}')
            except Exception:
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
        if default is None:
            return
        if self._template is not None:
            for template in self._template:
                try:
                    template.check(default)
                except DataError:
                    pass
                else:
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
        errors = []
        for template in self._template:
            try:
                template.check(value)
            except DataError as e:
                errors.append(e.error)
            else:
                return
        raise DataError(error='\n'.join(errors))
