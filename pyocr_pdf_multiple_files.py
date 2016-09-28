'''
Author: Brian Weber
Date: September 28, 2016
Revision: 1

Description: A sample script for reading in multiple PDF documents and running 
Opitical Character Recognition (OCR) on the documents. OCR makes the scanned PDF 
searchable by storing the text in a dictionary related to the name of the 
document and the page number.

Source: https://pythontips.com/2016/02/25/ocr-on-pdf-files-using-python/
'''


# Import the required libraries
from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io
import sys, os


# Find all documents with .pdf extension in current directory
pdf_files = []

dir_path = os.getcwd()
for file in os.listdir(dir_path):
	if file.endswith(".pdf"):
		pdf_files.append(file)

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

# Setup a list and a dictionary which will be used to hold our images and 
# final_text. final_text will be organized by a key referring to the document
# name and page number.
req_image = []
final_text = {}


for pdf_file in pdf_files:
	# Open the PDF file using wand and convert it to jpeg
	image_pdf = Image(filename=pdf_file, resolution=300)
	image_jpeg = image_pdf.convert('pdf')

	# wand has converted all the separate pages in the PDF into separate image
	# blobs. We can loop over them and append them as a blob into the req_image
	# list.
	for img in image_jpeg.sequence:
		img_page = Image(image=img)
		req_image.append(img_page.make_blob('jpeg'))

	# Now we just need to run OCR over the image blobs and store all of the 
	# recognized text in final_text.
	i = 1
	for img in req_image:
		txt = tool.image_to_string(
			PI.open(io.BytesIO(img)),
			lang=lang,
			builder=pyocr.builders.TextBuilder()
		)
		final_text[pdf_file + ' Page ' + str(i)] = txt
		i += 1

# Print the document name with page number and the text found by OCR.
for key, value in final_text.iteritems():
	print("\nDocument: {}".format(key))
	print("\nThe final text is: \n")
	print(value)