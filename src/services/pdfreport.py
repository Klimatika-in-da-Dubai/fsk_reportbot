import io
from PIL import Image

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfdoc import Destination
from reportlab.pdfbase.ttfonts import TTFont, TTFontParser

from src.services.reporttools import *


class pdfGenerator:
    canv = canvas.Canvas("./report.pdf", pagesize=(PDF_WIDTH, PDF_HEIGHT))

    def __init__(self, report_name: str = "report"):
        self.report_name = report_name
        self.canv = canvas.Canvas(
            f"{REPORTS_PATH}/{self.report_name}.pdf", pagesize=(PDF_WIDTH, PDF_HEIGHT)
        )
        # set up fonts
        pdfmetrics.registerFont(TTFont(Fonts.regular["name"], Fonts.regular["path"]))
        pdfmetrics.registerFont(TTFont(Fonts.italics["name"], Fonts.italics["path"]))
        pdfmetrics.registerFont(TTFont(Fonts.medium["name"], Fonts.medium["path"]))
        pdfmetrics.registerFont(TTFont(Fonts.light["name"], Fonts.light["path"]))
        pdfmetrics.registerFont(TTFont(Fonts.bold["name"], Fonts.bold["path"]))

    def first_slide(self):
        canv = self.canv
        background = Image.open(BACKGROUND)
        logo = Image.open(LOGO_PATH)

        add_image(canv, background, PDF_WIDTH, 0, 0)
        add_image(canv, logo, 400, PDF_WIDTH - 435, PDF_HEIGHT - 235)

        textobject = canv.beginText()
        textobject.setTextOrigin(Indent.get_x(), PDF_HEIGHT - Indent.get_y() * 6.5)
        textobject.setFillColor("#FFFFFF")
        textobject.setFont(Fonts.medium["name"], 130)
        textobject.setLeading(140)

        textobject.textLine(text="Отчёт выполненных")
        textobject.textLine(text="работ")

        canv.drawText(textobject)

        canv.showPage()

    def bef_aft_slide(
        self, work_name: str, node_name: str, before: BinaryIO, after: BinaryIO
    ):
        # , before: BinaryIO = 0, after: BinaryIO = 0
        canv = self.canv

        background = Image.open(BACKGROUND)
        add_image(canv, background, PDF_WIDTH, 0, 0)

        img_before = image_crop(before)
        img_after = image_crop(after)
        add_image(canv, img_before, 780, Indent.get_x(), Indent.get_y())
        add_image(
            canv, img_after, 780, PDF_WIDTH - 760 - Indent.get_x(), Indent.get_y()
        )

        textobject = canv.beginText()
        textobject.setTextOrigin(
            Indent.get_x(), PDF_HEIGHT - Indent.get_y() - HEDING_FONT_SIZE
        )

        textobject.setFont(Fonts.medium["name"], HEDING_FONT_SIZE)
        textobject.setFillColor("#000000")
        textobject.setLeading(HEDING_FONT_SIZE - 10)
        textobject.textLine(text=work_name)

        textobject.setFont(Fonts.light["name"], HEDING_FONT_SIZE - 25)
        textobject.setLeading(HEDING_FONT_SIZE * 2)
        textobject.textLine(text=node_name)

        textobject.setFont(Fonts.italics["name"], HEDING_FONT_SIZE)
        textobject.setFillColor("#FFFFFF")
        textobject.setTextOrigin(
            Indent.get_x(), PDF_HEIGHT - Indent.get_y() - HEDING_FONT_SIZE * 4
        )
        textobject.textLine(text="до")
        textobject.setTextOrigin(
            860 + Indent.get_x(), PDF_HEIGHT - Indent.get_y() - HEDING_FONT_SIZE * 4
        )
        textobject.textLine(text="после")

        canv.drawText(textobject)

        canv.showPage()

    def comment_slide(self, work_name: str, node_name: str, comment: str):
        canv = self.canv

        background = Image.open(BACKGROUND)
        add_image(canv, background, PDF_WIDTH, 0, 0)

        textobject = canv.beginText()
        textobject.setTextOrigin(
            Indent.get_x(), PDF_HEIGHT - Indent.get_y() - HEDING_FONT_SIZE
        )

        textobject.setFont(Fonts.medium["name"], HEDING_FONT_SIZE)
        textobject.setFillColor("#000000")
        textobject.setLeading(HEDING_FONT_SIZE - 10)
        textobject.textLine(text=work_name)

        textobject.setFont(Fonts.light["name"], HEDING_FONT_SIZE - 25)
        textobject.setLeading(HEDING_FONT_SIZE * 2)
        textobject.textLine(text=node_name)

        textobject.setFont(Fonts.italics["name"], HEDING_FONT_SIZE - 10)
        textobject.setFillColor("#FFFFFF")
        textobject.textLine(text="комментарий")

        textobject.setFont(Fonts.regular["name"], 31)
        textobject.setFillColor("#000000")
        textobject.setLeading(36)
        for i in divide_by_len(comment, 67):
            textobject.textLine(text=i)

        canv.drawText(textobject)

        canv.showPage()

    def last_slide(self):
        canv = self.canv

        background = Image.open(BACKGROUND)
        add_image(canv, background, PDF_WIDTH, 0, 0)

        textobject = canv.beginText()
        textobject.setTextOrigin(
            Indent.get_x(), PDF_HEIGHT - Indent.get_y() - HEDING_FONT_SIZE
        )

        textobject.setFont(Fonts.medium["name"], HEDING_FONT_SIZE)
        textobject.setFillColor("#000000")
        textobject.textLine(text="Контакты")

        textobject.setTextOrigin(Indent.get_x(), PDF_HEIGHT - 300)
        textobject.setFillColor("#FFFFFF")

        textobject.setFont(Fonts.regular["name"], 35)
        textobject.setCharSpace(-1)
        textobject.setLeading(40)
        textobject.textLine(text="г. Н. Новгород, ул. Белинского 32, БЦ «Две")
        textobject.setLeading(90)
        textobject.textLine(text="Башни», Круглая башня, оф. 205")
        textobject.textLine(text="+7 800 444-44-01")
        textobject.textLine(text="info@fedscom.ru")

        canv.drawText(textobject)
        canv.showPage()

    def generate(self, work_list: dict):
        self.first_slide()

        for work_place in work_list["work_places"]:
            for work in work_place["works"]:
                for node in work["work_nodes"]:
                    self.bef_aft_slide(
                        work_place["name"] + " " + work["name"],
                        node["name"],
                        node["photo_before"],
                        node["photo_after"],
                    )
                if work["comment"] != "":
                    self.comment_slide(
                        work_place["name"] + " " + work["name"],
                        "",
                        work["comment"],
                    )
        self.last_slide()
        self.canv.save()

        pdf_compression(f"{self.report_name}.pdf")
