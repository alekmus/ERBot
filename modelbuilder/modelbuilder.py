import PyPDF2
from pathlib import Path
import os
import pandas as pd

dir_location = Path('.') / 'samples'
data = []

with open(dir_location/'labels.csv') as f:
    labels = [int(line) for line in f]

for file in os.scandir(dir_location):
    if file.name != 'labels.csv':
        with open(file, 'rb') as f:
            file_index = int(Path(file.path).stem)
            reader = PyPDF2.PdfFileReader(f)
            for i in range(reader.getNumPages()):
                page = reader.getPage(i).extractText()
                data.append((page, i == labels[file_index]))


for i in data:
    print(i)
    input('.')

