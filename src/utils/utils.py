from aiogram import Bot
from src.models.report import Report
from src.models.work import Work
from src.models.work_node import WorkNode


async def create_report_dict(report: Report, bot: Bot) -> dict:
    report_dict = {"work_places": []}
    for work_place in report.work_places:
        work_place_dict = {"name": work_place.name, "works": []}

        for work in work_place.works:
            work_dict = {"name": work.name, "work_nodes": [], "comment": work.comment}

            for work_node in work.work_nodes:
                work_node_dict = {
                    "name": work_node.name,
                    "photo_before": await bot.download(work_node.photo_before.file_id),
                    "photo_after": await bot.download(work_node.photo_after.file_id),
                }

                work_dict["work_nodes"].append(work_node_dict)
            work_place_dict["works"].append(work_dict)
        report_dict["work_places"].append(work_place_dict)
    print(report_dict)
    return report_dict
