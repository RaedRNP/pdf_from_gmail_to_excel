from pypdf import PdfReader
import os

os.chdir('./Download')
list_of_files = os.listdir()

for file in list_of_files:
    reader = PdfReader(file)
    page = reader.pages[0]
    print(page.extract_text(0))
    break