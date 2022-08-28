from PIL import ImageGrab
from pyautogui import press
import pytesseract
import time
from PyPDF2 import PdfMerger

# Mandatory Configs
top_left_x = 500
top_left_y = 90
bottom_right_x = 1180
bottom_right_y = 990
bounding_box = (
    top_left_x,
    top_left_y,
    bottom_right_x,
    bottom_right_y,
)  # Can use Command+Shift+4 in MacOS to get the coordinates.
total_pages = 134

# Optional Configs
delay_next_page = 1
save_png = False
use_ocr = True
merge_outputs = True
tmp_path = f"/tmp/screen-grabber"


def next_page(delay=None):
    if delay:
        time.sleep(delay)
    press("right")


def merge(input_dir, output_file):
    merger = PdfMerger()
    for x in range(total_pages):
        merger.append(f"{input_dir}/{x}.pdf")
    merger.write(output_file)
    merger.close()


def print_page(page_num):
    im = ImageGrab.grab(bbox=bounding_box).convert("RGB")
    print(f"Page {page_num + 1}/{total_pages}\r", end="")

    if save_png:
        im.save(f"{tmp_path}/{page_num}.png")

    if use_ocr:
        pdf = pytesseract.image_to_pdf_or_hocr(im, extension="pdf")
        with open(f"/{tmp_path}/{page_num}.pdf", "w+b") as f:
            f.write(pdf)
    else:
        im.save(f"{tmp_path}/{page_num}.pdf")


def main():
    for i in range(5):
        print("Recording will start in %d\r" % (5 - i), end="")
        time.sleep(1)
    print()

    for i in range(total_pages):
        print_page(i)
        next_page(delay=delay_next_page)
    print()

    if merge_outputs:
        merge(tmp_path, f"{tmp_path}/output.pdf")


if __name__ == "__main__":
    main()
