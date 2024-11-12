from py_pdf_parser.loaders import load_file
import sys

def main(argv):
    for file in argv[1:]:
        parsePdf(file)

def parsePdf(file):
    try:
        pdf = load_file(file)

        for el in pdf.elements:
            print(f"{el.font_name} {el.font_size}")
            print(el.text())

    except:
        print(f"Could not load {file}")

main(sys.argv)
