from boersebot import pdf_reader

if __name__ == '__main__':
    sample = pdf_reader.pdf_to_string("samples/0.pdf", 17)
    lines = sample.split('\n')

    for line in lines:
        if 'tulos' in line.lower():
            print(line.strip())
