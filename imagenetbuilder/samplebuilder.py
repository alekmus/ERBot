import PyPDF2
from pathlib import Path
import os
import pandas as pd

dir_location = Path('.') / 'samples'
labels = pd.read_csv(dir_location/'labels.csv')
print(labels)

