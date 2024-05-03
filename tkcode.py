import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.ttk import Style
import cups
from PyPDF2 import PdfReader, PdfWriter
import os
from os.path import join
from tempfile import TemporaryDirectory
from pdf2image import convert_from_path
from img2pdf import convert


def browse_file_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return file_path


def convert_to_grayscale(input_path, output_path):
    with TemporaryDirectory() as temp_dir:
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
            images[page_number - 1].save(path, "JPEG")

        with open(output_path, "bw") as gray_pdf:
            gray_pdf.write(convert(image_list))

        print("The new page is saved as Gray_PDF.pdf in the current directory.")


def print_pdf_page(pdf_path, page_number, printer_name, duplex=False, grayscale=False):
    if grayscale:
        grayscale_path = "/tmp/grayscale.pdf"
        convert_to_grayscale(pdf_path, grayscale_path)
        pdf_path = grayscale_path

    conn = cups.Connection()
    printers = conn.getPrinters()

    if printer_name not in printers:
        raise ValueError(f"Printer '{printer_name}' not found.")

    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        if 0 < page_number <= len(pdf_reader.pages):
            page = pdf_reader.pages[page_number - 1]
            output_path = "/tmp/temp_page.pdf"
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
                'sides': 'two-sided-long-edge' if duplex else 'one-sided',
            }
            print_job_id = conn.printFile(printer_name, output_path, f"Print Job - Page {page_number}", print_options)
            print(f"Print job sent. Job ID: {print_job_id}")
            os.remove(output_path)
        else:
            raise ValueError(f"Invalid page number. PDF has {len(pdf_reader.pages)} pages.")


def main():
    file_path = browse_file_path()
    if file_path:
        root = tk.Tk()
        root.withdraw()
        style = Style()
        style.theme_use('clam')  # Choose from 'alt', 'default', 'classic', 'vista', 'xpnative'
        grayscale_var = tk.IntVar()
        grayscale_checkbox = messagebox.askyesno("Grayscale", "Do you want to print in grayscale?")
        if grayscale_checkbox:
            grayscale_var.set(1)
        else:
            grayscale_var.set(0)
        page_number = simpledialog.askinteger("Page Number", "Enter the page number:", minvalue=1)
        if page_number is not None:
            double_sided = messagebox.askyesno("Double-Sided Printing", "Do you want to print in double-sided mode?")
            if double_sided:
                start_page = simpledialog.askinteger("Start Page", "Enter the starting page number:", minvalue=1)
                end_page = simpledialog.askinteger("End Page", "Enter the ending page number:", minvalue=start_page)
                for page in range(start_page, end_page + 1):
                    print_pdf_page(file_path, page, "Canon_E410_series", duplex=True, grayscale=grayscale_var.get())
                    continue_printing = messagebox.askyesno("Continue Printing", "Do you want to continue printing?")
                    if not continue_printing:
                        break
            else:


                printer_name = "Canon_E410_series"  # Replace this with your printer's name
                print_pdf_page(file_path, page_number, printer_name, duplex=False, grayscale=grayscale_var.get())


if __name__ == "__main__":
    main()
