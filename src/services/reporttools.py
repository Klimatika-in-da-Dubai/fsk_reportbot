from typing import BinaryIO
from reportlab.pdfgen import canvas
from PIL import Image
import subprocess
import shutil
import os

PDF_HEIGHT, PDF_WIDTH = 1080, 1920
HEDING_FONT_SIZE = 60
INDENTS = (150, 80) # indents by x and y
REPORTS_PATH = "./reports"
LOGO_PATH = "./img/FSK_logo.jpg"
BACKGROUND = "./img/gradient_background.png"


class Indent:
    _x = INDENTS[0]
    _y = INDENTS[1]

    @staticmethod
    def get_x() -> int:
        return Indent._x
    @staticmethod
    def get_y() -> int:
        return Indent._y

class Fonts:
    regular = {
            "name" : 'TTNormsPro',
            "path" : '../fonts/TTNormsPro.ttf'
    }
    bold =    {
            "name" : 'TTNormsProBold',
            "path" : '../fonts/TTNormsProB.ttf'
    }
    italics = {
            "name" : 'TTNormsProItalics',
            "path" : '../fonts/TTNormsProI.ttf'
    }
    medium =  {
            "name" : 'TTNormsProMedium',
            "path" : '../fonts/TTNormsProM.ttf'
    }
    light =   {
            "name" : 'TTNormsProLight',
            "path" : '../fonts/TTNormsProL.ttf'
    }

class Formatter:
    IMAGE_WIDTH = 0
    X_POS = 0
    Y_POS = 0

    def __init__(self, img_width, hor_pos, vert_pos):
        self.IMAGE_WIDTH = img_width
        self.X_POS = hor_pos
        self.Y_POS = vert_pos

    def width(self) -> float:
        return self.IMAGE_WIDTH

    def center(self) -> tuple[int, int]:
        return (int((PDF_WIDTH - self.X_POS) / 2), int(self.Y_POS))

    def left(self) -> tuple[int, int]:
        return (0, int(self.Y_POS))

    def right(self) -> tuple[int, int]:
        return (int(PDF_WIDTH - self.X_POS), int(self.Y_POS))


def divide_by_len(text: str, line_len: int) -> list:
    text = text.replace("  ", " ")
    text_lines = []
    j = 1
    start = 0
    if line_len >= len(text):
        text_lines.append(text)
    else:
        while start < len(text):
            end_j = j * (line_len + 1)
            if end_j >= len(text):
                end_j = len(text) - 1
            for end in range(end_j, start, -1):
                if end + 1 == len(text) or text[end] == ' ':
                    end += 1
                    text_lines.append(text[start:end])
                    start = end
                    j += 1
                    break
    return text_lines


def image_crop(img_bin: BinaryIO, w_size=4, h_size=3) -> Image.Image:
    img = Image.open(img_bin)
    width, height = img.size

    relation = width/height
    left = 0
    top = 0
    right = width
    bottom = height

    if relation > w_size/h_size:
        to_crop = (width - (height * w_size)/h_size) / 2
        left = to_crop
        right = width - to_crop
        bottom = height
    elif relation < w_size/h_size:
        to_crop = (height - (width * h_size)/w_size) / 2
        top = to_crop
        right = width
        bottom = height - to_crop
    return img.crop((left, top, right, bottom))


def image_formatter(img, exp_width: int) -> canvas.ImageReader:
    img_w, img_h = img.size
    size_rel = img_h / img_w
    exp_height = int(exp_width * size_rel)
    exp_size = tuple([exp_width, exp_height])
    return canvas.ImageReader(img.resize(exp_size))


def add_image(canv, img: Image.Image, img_width: float, x: float, y: float):
    format_const = Formatter(img_width, INDENTS[0], y)
    img_f = image_formatter(img, int(format_const.width()))
    canv.drawImage(img_f, x=x, y=y, mask='auto')

def _get_ghostscript_path():
    gs_names = ['gs', 'gswin32', 'gswin64']
    for name in gs_names:
        if shutil.which(name):
            return shutil.which(name)
    raise FileNotFoundError(f'No GhostScript executable was found on path ({"/".join(gs_names)})')

def pdf_compression(filename: str):
    gs = _get_ghostscript_path()
    input_file_abs_path = os.path.abspath(f'reports/{filename}')
    output_file_abs_path = os.path.abspath(f'reports/{filename.strip(".pdf")}-compressed.pdf')
    # print(input_file_abs_path)
    # print(output_file_abs_path)
    # print("---------------")
    with open(f'{output_file_abs_path}', 'w') as _:
        pass
    subprocess.call([gs, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                    '-dPDFSETTINGS={}'.format('/default'),
                    '-dNOPAUSE', '-dQUIET', '-dBATCH',
                    '-sOutputFile={}'.format(output_file_abs_path),
                     input_file_abs_path]
    )

