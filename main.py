import cups
from PyPDF2 import PdfReader, PdfWriter
import os
from os.path import join
from tempfile import TemporaryDirectory
from pdf2image import convert_from_path
from img2pdf import convert 
import subprocess
def convert_to_grayscale(input_path, output_path):
    with TemporaryDirectory() as temp_dir: # Saves images temporarily in disk rather than RAM to speed up parsing
        # Converting pages to images
        print("Parsing pages to grayscale images. This may take a while")
        images = convert_from_path(
            input_path,
            output_folder=temp_dir,
            grayscale=True,
            fmt="jpeg",
            thread_count=4
        )

        image_list = list()
        for page_number in range(1, len(images) + 1):
            path = join(temp_dir, "page_" + str(page_number) + ".jpeg")
            image_list.append(path)
            images[page_number-1].save(path, "JPEG") # (page_number - 1) because index starts from 0

        with open(output_path, "bw") as gray_pdf:
            gray_pdf.write(convert(image_list))

        print("The new page is saved as Gray_PDF.pdf in the current directory.")

def print_pdf_page(pdf_path, page_number, printer_name,grayscale = False):
    if grayscale:
        grayscale_path = "/tmp/grayscale.pdf"
        convert_to_grayscale(pdf_path,grayscale_path)
        pdf_path = grayscale_path
    conn = cups.Connection()
    printers = conn.getPrinters()

    if printer_name not in printers:
        raise ValueError(f"Printer '{printer_name}' not found.")

    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        if 0 < page_number <= len(pdf_reader.pages):
            page = pdf_reader.pages[page_number - 1]
            output_path = "/tmp/temp_page.pdf"  # Temporary file path
            with open(output_path, 'wb') as output_file:
                writer = PdfWriter()
                writer.add_page(page)
                writer.write(output_file)

            print_options = {
                'media': 'A4',
                'scaling': '100',
                'fit-to-page': 'True',
                'cpi': '600',
                'lpi': '600',

            }
            print_job_id = conn.printFile(printer_name, output_path, f"Print Job - Page {page_number}", print_options)
            print(f"Print job sent. Job ID: {print_job_id}")
            #remove tmp file 
            os.remove(output_path)

        else:
            raise ValueError(f"Invalid page number. PDF has {len(pdf_reader.pages)} pages.")


# Example usage
pdf_path = "/Users/doganalisan/Downloads/12.sinif.pdf"  # Replace this with the path to your PDF file
page_number = 1  # Replace this with the desired page number
printer_name = "Canon_E410_series"  # Replace this with your printer's name

print_pdf_page(pdf_path, page_number, printer_name,True)
