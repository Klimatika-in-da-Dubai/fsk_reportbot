from dataclasses import dataclass, field
from src.models.work import Work


@dataclass
class WorkPlace:
    name: str
    works: list[Work] = field(default_factory=list)

    def get_work(self, index: int) -> Work:
        return self.works[index]

    def add_work(self, work: Work) -> None:
        self.works.append(work)

    def remove_work(self, work: Work) -> None:
        self.works.remove(work)

    def pop_work(self, index: int) -> None:
        self.works.pop(index)

    def empty(self) -> bool:
        return len(self.works) == 0

    def filled(self) -> bool:
        if self.empty():
            return False

        return all(work.filled() for work in self.works)
