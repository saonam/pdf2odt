## @namespace pdf2odt.core
## @brief Core functions of the package
import datetime
import platform
import sys
import glob

if platform.system()=="Windows":
    print("This script only works on Linux")
    sys.exit(0)

import argparse
import gettext
import locale
import os
import pkg_resources

from colorama import Fore, Style, init as colorama_init
from pdf2odt.version import __versiondate__, __version__
from officegenerator import ODT_Standard
from odf.text import P
from PIL import Image

try:
    t=gettext.translation('pdf2odt',pkg_resources.resource_filename("pdf2odt","locale"))
    _=t.gettext
except:
    _=str

## pdf2odt main script
## If arguments is None, launches with sys.argc parameters. Entry point is pdf2odt:main
## You can call with main(['--pretend']). It's equivalento to os.system('pdf2odt --pretend')
## @param arguments is an array with parser arguments. For example: ['--max_files_to_store','9']. 
def main(arguments=None):
    start=datetime.datetime.now()
    parser=argparse.ArgumentParser(prog='pdf2odt', description=_('Converts a pdf to a LibreOffice Writer document with pages as images'), epilog=_("Developed by Mariano Muñoz 2019-{}".format(__versiondate__.year)), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument('--pdf', help=_("PDF file to convert"), action="store", default=None)
    parser.add_argument('output', help=_("Output odt file"), action="store")

    args=parser.parse_args(arguments)

    colorama_init(autoreset=True)

    # Sets locale to get integer format localized strings
    try:
        locale.setlocale(locale.LC_ALL, ".".join(locale.getlocale()))
    except:
        pass


    os.system("pdftoppm -png '{}' 'pdf2odt_temporal'".format(args.pdf))

    doc=ODT_Standard(args.output)
    doc.setMetadata("OfficeGenerator title", "OfficeGenerator subject", "Turulomio")

    for filename in sorted(glob.glob("pdf2odt_temporal*.png")):
        img = Image.open(filename)
        x,y=img.size
        cmx=17
        cmy=y*cmx/x
        doc.addImage(filename, filename)
        p = P(stylename="Illustration")
        p.addElement(doc.image(filename, cmx,cmy))
        doc.insertInCursor(p, after=True)
        p = P(stylename="Standard")
        doc.insertInCursor(p, after=True)
    doc.save()

    for filename in glob.glob("pdf2odt_temporal*.png"):
        os.system("rm '{}'".format(filename))