from dataclasses import dataclass, field
from aiogram import types
from src.models.work_node import WorkNode


@dataclass
class Work:
    name: str
    work_nodes: list[WorkNode] = field(default_factory=list)
    comment: str = ""

    def get_work_node(self, index: int) -> WorkNode:
        return self.work_nodes[index]

    def add_node(self, node: WorkNode) -> None:
        self.work_nodes.append(node)

    def remove_node(self, node: WorkNode) -> None:
        self.work_nodes.remove(node)

    def pop_node(self, index: int) -> None:
        self.work_nodes.pop(index)

    def empty(self) -> bool:
        return len(self.work_nodes) == 0

    def filled(self) -> bool:
        if self.empty():
            return False

        return all(node.filled() for node in self.work_nodes)
