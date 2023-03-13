from dataclasses import dataclass, field
from src.models.work_place import WorkPlace


@dataclass
class Report:
    work_places: list[WorkPlace] = field(default_factory=list)

    def get_work_place(self, index: int) -> WorkPlace:
        return self.work_places[index]

    def add_work_place(self, work_place: WorkPlace) -> None:
        self.work_places.append(work_place)

    def remove_work_place(self, work_place: WorkPlace) -> None:
        self.work_places.remove(work_place)

    def pop_work_place(self, index: int) -> None:
        self.work_places.pop(index)

    def empty(self) -> bool:
        return len(self.work_places) == 0

    def filled(self) -> bool:
        if self.empty():
            return False

        return all(work_place.filled() for work_place in self.work_places)


