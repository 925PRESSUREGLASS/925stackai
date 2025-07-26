from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class Tool:
    func: Callable[..., Any]
    name: str = ""
    description: str = ""

    @classmethod
    def from_function(
        cls, func: Callable[..., Any], name: str = "", description: str = ""
    ) -> "Tool":
        return cls(func=func, name=name, description=description)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)
