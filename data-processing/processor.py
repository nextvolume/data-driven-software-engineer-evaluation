from py_pdf_parser.loaders import load_file
from py_pdf_parser.common import BoundingBox
from xml.etree import cElementTree as et

import sys

def main(argv) -> int:
    """ Main program function """
    if len(argv) == 1:
        print(f"{argv[0]} [PDF files...]")

        return 0

    try:
        parsePdfFiles(argv[1:])

    except Exception as ex:
        print(ex)
# Error
        return 1

# Success
    return 0

def parsePdfFiles(fileNames):
    """ 
This will parse PDF files specified with filenames specified by fileNames
and for each then save an XML having the filename suffixed by an XML extension
"""
    for file in fileNames:
        parsed = parsePdf(file)

        writeXml(f"{file}.xml", parsed)

# PDF parsing function
def parsePdf(file) -> dict:
    """ PDF parsing function

Returns dictionary-based structure with parsed PDF.
"""
    pdf = None

# Load file
    try:
        pdf = load_file(file)

    except:
        raise Exception(f"Could not load {file}")

    try:
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

        return parsed

    except:
        raise Exception(f"Error parsing {file}")

def writeXml(outName, parsed):
    """XML writing function from pasrsed PDF data
"""
    try:
# Create document structure        
       doc = et.Element("Document")

       for paragraph in parsed:
          par = et.SubElement(doc, "Paragraph")

          for element in paragraph:
            et.SubElement(par, "Part", font_name=element['font_name'],
                font_size=str(element['font_size'])).text = element['text']

# The tree node is the Document element
       tree = et.ElementTree(doc)

# Write XML to file
       tree.write(outName)

    except:
        raise Exception(f"Problem during writing of {outName}")

# Run main function
sys.exit(main(sys.argv))
