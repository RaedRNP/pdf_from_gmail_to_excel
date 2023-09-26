from pypdf import PdfReader
import os

os.chdir('./Download')
list_of_files = os.listdir()

for file in list_of_files:
    print(file)