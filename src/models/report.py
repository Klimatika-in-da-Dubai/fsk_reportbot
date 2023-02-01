from dataclasses import dataclass, field
from src.models.work import Work, WorkNode


@dataclass
class Report:
    works: list[Work] = field(default_factory=list)

    @property
    def last_work(self) -> Work:
        return self.work_nodes[-1]

    @property
    def last_work_node(self) -> WorkNode:
        return self.last_work.last_work_node

    def add_work(self, work: Work) -> None:
        self.works.append(work)

    def empty(self) -> bool:
        return len(self.works) == 0
