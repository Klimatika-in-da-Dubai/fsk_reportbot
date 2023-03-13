from dataclasses import dataclass, field
from .report import Report
from .work_place import WorkPlace
from .work import Work
from .work_node import WorkNode


@dataclass
class User:
    report: Report = field(default_factory=Report)
    selected_work_place: WorkPlace | None = None
    selected_work: Work | None = None
    selected_work_node: WorkNode | None = None

    def select_work_place(self, index: int) -> None:
        self.selected_work_place = self.report.get_work_place(index)

    def select_work(self, index: int) -> None:
        self.selected_work = self.selected_work_place.get_work(index)

    def select_work_node(self, index: int) -> None:
        self.selected_work_node = self.selected_work.get_work_node(index)
