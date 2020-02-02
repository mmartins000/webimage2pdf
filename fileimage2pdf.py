#!/usr/local/bin/python3

# fileimage2pdf v0.1
# Author: Marcelo Martins (exploitedbunker.com)
# Source: https://github.com/mmartins000/webimage2pdf
# Combines images from a single folder into one PDF file.
#
# This project requires img2pdf
# $ pip install img2pdf

import argparse
import re
import os
import time
import img2pdf

__VERSION__ = "0.1"

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--folder", dest='folder', help="Source folder")
parser.add_argument("-q", "--quiet", dest='quiet', action='store_true', help="Quiet mode")
args = parser.parse_args()


def usage():
    args.quiet or \
        print("Usage: $0 -f|--folder <path>] [-q|--quiet]"
              "\nOnly -f|--folder is mandatory."
              "\n\nExample:\n"
              "$0 -u ~/Documents/images/")
    exit(1)


def append_pdf(image_list, destination_folder):
    with open(destination_folder + ".pdf", "wb") as f:
        os.chdir(destination_folder)
        try:
            f.write(img2pdf.convert([i for i in image_list]))
        except Exception as e:
            if str(e).startswith("Refusing"):
                print("Error: the module img2pdf cannot work with images with alpha channels.")
                print("Probably one of the images is a PNG with alpha channel.")
                print("On macOS, use Preview Inspector (Cmd+I) to find if an image has an alpha channel.")
                print("Also, Preview can remove the alpha channel and save the image under another filename.")
                print("You can also use Preview to export the image to JPEG.")
                print("On Linux, 'convert' from ImageMagick may be used to remove the alpha channel.")
                exit(2)
    args.quiet or print("Done. PDF generated as file " + destination_folder + ".pdf")


def check_folder(folder):
    if os.path.exists(folder):
        return True
    else:
        if os.path.exists(os.getcwd() + '/' + folder):
            return True
    return False


def assemble_file_list(folder):
    regex = 'jpg|jpeg|png'  # default regex
    image_list = list()
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if not os.path.isdir(path):
            extension = str(filename).rsplit('.', 1)[1]
            if re.match(regex, extension):
                image_list.append(filename)
    return image_list


def main():
    start_time = time.time()
    check_folder(args.folder) or usage()
    args.quiet or print("fileimage2pdf " + __VERSION__)

    image_list = assemble_file_list(args.folder)

    append_pdf(image_list, args.folder)
    args.quiet or print("Runtime took " + str(round(time.time() - start_time, 2)) + " seconds.")


if __name__ == "__main__":
    main()
