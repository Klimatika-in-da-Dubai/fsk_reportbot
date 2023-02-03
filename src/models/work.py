from dataclasses import dataclass, field
from aiogram import types
from src.models.work_node import WorkNode


@dataclass
class Work:
    name: str
    work_nodes: list[WorkNode] = field(default_factory=list)

    _index: int = field(default=0, init=False)

    def add_work_node(self, work_node: WorkNode) -> None:
        self.work_nodes.append(work_node)

    @property
    def last_work_node(self) -> WorkNode:
        return self.work_nodes[-1]

    @property
    def current_node(self) -> WorkNode | None:
        if self._index == len(self.work_nodes):
            return None
        return self.work_nodes[self._index]

    def empty(self) -> bool:
        return len(self.work_nodes) == 0

    def next(self) -> None:
        if self._index == len(self.work_nodes):
            return
        self._index += 1
