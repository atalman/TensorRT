from typing import Any, Callable, List, Optional

import torch
from torch.fx.passes.pass_manager import PassManager


class DynamoPassManager(PassManager):  # type: ignore[misc]
    def __init__(
        self,
        passes: Optional[
            List[Callable[[torch.fx.GraphModule], torch.fx.GraphModule]]
        ] = None,
    ):
        super().__init__(passes)

    @classmethod
    def build_from_passlist(
        cls,
        passes: Optional[List[Callable[[torch.fx.GraphModule], torch.fx.GraphModule]]],
    ) -> Any:
        pm = DynamoPassManager(passes)
        return pm

    def add_pass_with_index(
        self,
        lowering_pass: Callable[[torch.fx.GraphModule], torch.fx.GraphModule],
        index: Optional[int] = None,
    ) -> None:
        if index is None:
            self.passes.append(lowering_pass)
            index = -1
        else:
            self.passes.insert(index, lowering_pass)

    def remove_pass_with_index(self, index: int) -> None:
        del self.passes[index]

    def __call__(self, source: Any) -> Any:
        return super().__call__(source)

    def __str__(self) -> str:
        return str(self.passes)