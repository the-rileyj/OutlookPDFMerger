from PyPDF2 import PdfFileMerger

# writer = PdfFileWriter()

merger = PdfFileMerger()

for i in range(1,5):
    merger.append("d{}.pdf".format(i))

with open("RJassignment.pdf", "wb") as output_file:
    merger.write(output_file)
