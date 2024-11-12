from py_pdf_parser.loaders import load_file
from py_pdf_parser.common import BoundingBox
import sys

def main(argv):
    for file in argv[1:]:
        parsePdf(file)

def parsePdf(file):
    pdf = None

    try:
        pdf = load_file(file)

    except:
        print(f"Could not load {file}")
        return -1

    try:
        pdf = load_file(file)
        font_size = 0
        bounding_box = BoundingBox(-1,-1,-1,-1)
        parsed = []
        paragraph = []

        for el in pdf.elements:
            if bounding_box.y0 - el.bounding_box.y1 > font_size: # New paragraph
                if len(paragraph) > 0:
                    parsed.append(paragraph)
                    paragraph = []

            paragraph.append({"text": el.text(),
                              "font_name": el.font_name,
                              "font_size": el.font_size,
                              "bounding_box": el.bounding_box})
            
            font_size = el.font_size
            bounding_box = el.bounding_box

        if len(paragraph) > 0:
             parsed.append(paragraph)   
            
        for par in parsed:
            print("*** PARAGRAPH START ***")
            print(par)
            print("*** PARAGRAPH END ***")

    except:
        print(f"Error parsing {file}")
        return -1

main(sys.argv)
