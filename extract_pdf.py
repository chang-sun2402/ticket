import PyPDF2

pdf_file = open('ACC102_2025-26_S2_MiniAssignment_Individual(1).pdf', 'rb')
reader = PyPDF2.PdfReader(pdf_file)
text = ''
for page in range(len(reader.pages)):
    text += reader.pages[page].extract_text()
pdf_file.close()
print(text)
