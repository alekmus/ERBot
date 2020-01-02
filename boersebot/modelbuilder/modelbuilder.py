from pathlib import Path
import os
import pandas as pd
import PyPDF2

dir_location = Path('.') / 'samples' /'0.pdf'
data = []

with open(dir_location/'labels.csv') as f:
    labels = [int(line) for line in f]

for file in os.scandir(dir_location):
    if file.name != 'labels.csv':
        with open(file, 'rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            data = reader.getPage(17)
print(data)
