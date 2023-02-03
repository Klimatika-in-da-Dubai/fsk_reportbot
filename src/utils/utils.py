from aiogram import Bot
from src.models.report import Report
from src.models.work import Work
from src.models.work_node import WorkNode


async def create_report_dict(report: Report, bot: Bot) -> dict:
    report_dict = {}
    for work_ind, work in enumerate(report.works):
        work_node_dict = {}
        for work_node_ind, work_node in enumerate(work.work_nodes):
            work_node_dict[work_node_ind] = {
                "name": work_node.name,
                "photo_before": await bot.download(work_node.photo_before.file_id),
                "photo_after": await bot.download(work_node.photo_after.file_id),
                "comment": work_node.comment,
            }
        report_dict[work_ind] = {"name": work.name, "nodes": work_node_dict}
    print(report_dict)
    return report_dict
