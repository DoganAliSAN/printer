import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os", "tkinter", "cups", "PyPDF2", "pdf2image", "tempfile", "img2pdf"],
    "include_files": [],
    "excludes": [],
    "path": sys.path + ["/Users/doganalisan/Projects/printer"]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"
elif sys.platform == "darwin":
    base = None

executables = [
    Executable("tkcode.py", base=base)
]

setup(
    name="Printer",
    version="1.0",
    description="Print PDF pages double-sided",
    options={"build_exe": build_exe_options, "bdist_mac": {"bundle_name": "Printer"}},
    executables=executables
)
