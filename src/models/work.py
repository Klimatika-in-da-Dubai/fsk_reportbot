from dataclasses import dataclass, field
from aiogram import types
from src.models.work_node import WorkNode


@dataclass
class Work:
    name: str
    work_nodes: list[WorkNode] = field(default_factory=list)

    def add_work_node(self, work_node: WorkNode) -> None:
        self.work_nodes.append(work_node)

    @property
    def last_work_node(self) -> WorkNode:
        return self.work_nodes[-1]

    def empty(self) -> bool:
        return len(self.work_nodes) == 0
