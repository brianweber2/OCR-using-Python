'''
Author: Brian Weber
Date: September 28, 2016
Revision: 1

Description: A sample script for reading in a PDF document and running Opitical 
Character Recognition (OCR) on the document. OCR makes the scanned PDF searchable.

Source: https://pythontips.com/2016/02/25/ocr-on-pdf-files-using-python/
'''


# Import the required libraries
from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io, sys


# Get the handle of the OCR library (in this case, tesseract)
tools = pyocr.get_available_tools()
if len(tools) == 0:
	print("No OCR tool found!")
	sys.exit(1)
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))

# Get the language
langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs)) 
lang = langs[1] # For English
print("Will use language '%s'" % (lang))

# Setup two lists which will be used to hold our images and final_text
req_image = []
final_text = []

# Open the PDF file using wand and convert it to jpeg
image_pdf = Image(filename="pdf_example.pdf", resolution=300)
image_jpeg = image_pdf.convert('pdf')

# wand has converted all the separate pages in the PDF into separate image
# blobs. We can loop over them and append them as a blob into the req_image
# list.
for img in image_jpeg.sequence:
	img_page = Image(image=img)
	req_image.append(img_page.make_blob('jpeg'))

# Now we just need to run OCR over the image blobs and store all of the 
# recognized text in final_text.
for img in req_image:
	txt = tool.image_to_string(
		PI.open(io.BytesIO(img)),
		lang=lang,
		builder=pyocr.builders.TextBuilder()
	)
	final_text.append(txt)

print("\nThe final text is: \n")
print final_text