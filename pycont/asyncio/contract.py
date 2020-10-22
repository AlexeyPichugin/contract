from typing import Any, Union, List, Dict
from trafaret import DataError

from pycont import Contract
from pycont.asyncio.template import AsyncTemplate as Template


class AsyncContract(Contract):
    """
    Contract class contains template to validate and generate object if data is valid

    Args:
    - template Union[Template, List[Template], Dict[str, Template]]:
        Template object or list of Templates or dict of Templates

    Raises:
    - ValueError if template is not valid

    Simple value validation and generate
        >>> from pycont import AsyncContract as Contract
        >>> from pycont import AsyncTemplate as Tempalte
        >>> import trafaret as t
        >>> contract = Contract(Template(t.Int()))
        >>> await contract(42)
    """
    async def _check(
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
                    result.append(await self._check(sub_template, value))
            else:
                if len(template) != len(data):
                    raise ValueError("Invalid value length")
                for inx, sub_template in enumerate(template):
                    next_data = data[inx]
                    result.append(await self._check(sub_template, next_data))
            return result

        if isinstance(template, dict):
            result = {}
            for key, sub_template in template.items():
                if key in data.keys():
                    result[key] = await self._check(sub_template, data[key])
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
            await template.check(data)
        except DataError as e:
            if template.default is not None:
                data = template.default
            else:
                raise e
        return data

    async def __call__(self, data: Any) -> Any:
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
                result = await self._check(template, data)
                return result
            except Exception as e:
                errors.append(e)
        raise ValueError(f"Invalid value: {errors}")
