from typing import Any, Union, List, Dict, TypeVar, Optional
from trafaret import DataError
from pycont.template import Template


T = TypeVar('Contract')


class Contract:
    """
    Contract class contains template to validate and generate object if data is valid

    Args:
    - template Union[Template, List[Template], Dict[str, Template]]:
        Template object or list of Templates or dict of Templates
    - optional_keys Optional[List[str]] = None
        Used only in dictionary contract
        The check function does not raise an error if the key is not set.

    Raises:
    - ValueError if template is not valid

    Simple value validation and generate
        >>> from pycont import Contract, Template
        >>> import trafaret as t
        >>> contract = Contract(Template(t.Int()))
        >>> print(contract(42))
        42
        >>> print(contract('test'))
        ValueError: invalid literal for int() with base 10: 'test'
    """
    def __init__(
        self,
        template: Union[Template, List[Template], Dict[str, Template]],
        optional_keys: Optional[List[str]] = None,
    ):
        self._validate(template)
        self._templates = [template]
        self.optional_keys = optional_keys or []

    def __or__(self, other: T) -> T:
        self._templates = self._templates + other._templates
        return self

    template = property()

    @template.getter
    def template(self) -> Union[Template, List[Template], Dict[str, Template]]:
        """
        Get current template value
        Return:
            Current template or list of tempalates
        """
        return self._templates[0] if len(self._templates) == 1 else self._templates[0]

    @template.setter
    def template(
        self,
        template: Union[Template, List[Template], Dict[str, Template]]
    ) -> None:
        """
        Set new template value

        Args:
            template Union[Template, List[Template], Dict[str, Template]]:
                new Template object or list of Template or Dict[str, Template]
        Raises:
            ValueError if template is not valid
        """
        self._validate(template)
        self._templates = [template]

    def _validate(
        self,
        template: Union[Template, List[Template], Dict[str, Template]]
    ):
        """
        Check what seted template is valid

        Raises:
            ValueError if template is not valid
        """
        if isinstance(template, list):
            for value in template:
                self._validate(value)
            return
        if isinstance(template, dict):
            for key, value in template.items():
                if not isinstance(key, str):
                    raise TypeError(f'Invalid key "{key}" type: key in template must be string')
                self._validate(value)
            return
        if not isinstance(template, Template):
            raise ValueError('Invalid value: value type must be Template')

    def _check(
        self,
        template: Union[Template, List[Template], Dict[str, Template]],
        data: Any
    ):
        """
        Recursive check if seted value is valid by template

        Args:
            template Union[Template, List[Template], Dict[str, Template]:
                Template object or list of Templates or dict of Templates
            data Any: data for checking

        Raises:
            trafaret.DataError if data cant checked
            ValueError or more Exepitons if cant read or validate data
        """
        if isinstance(template, list):
            result = []
            if len(template) == 1:
                sub_template = template[0]
                for value in data:
                    result.append(self._check(sub_template, value))
            else:
                if len(template) != len(data):
                    raise ValueError("Invalid value length")
                for inx, sub_template in enumerate(template):
                    next_data = data[inx]
                    result.append(self._check(sub_template, next_data))
            return result

        if isinstance(template, dict):
            result = {}
            for key, sub_template in template.items():
                if key in data.keys():
                    result[key] = self._check(sub_template, data[key])
                else:
                    if key not in self.optional_keys:
                        if isinstance(sub_template, Template):
                            if sub_template.default is not None:
                                result[key] = sub_template.default
                            else:
                                if not sub_template.optional:
                                    raise ValueError(f'Key "{key}" not set')
                        else:
                            raise ValueError(f'Key "{key}" not set')
            return result
        try:
            template.check(data)
        except DataError as e:
            if template.default is not None:
                data = template.default
            else:
                raise e
        return data

    def __call__(self, data: Any) -> Any:
        """
        Validate and generate object by template

        Args:
            data Any: data for validation

        Return:
            Any: data if data is valid

        Raises:
            ValueError if data is not valid
        """
        errors = []
        for template in self._templates:
            try:
                result = self._check(template, data)
                return result
            except Exception as e:
                errors.append(e)
        raise ValueError(f"Invalid value: {errors}")
