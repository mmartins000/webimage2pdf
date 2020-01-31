#!/usr/local/bin/python3

# webimage2pdf v0.1
# Author: Marcelo Martins (exploitedbunker.com)
# Source: https://github.com/mmartins000/webimage2pdf
# Scrapes images from webpages, downloads and combines them into one PDF file.
#
# This project requires Selenium, Requests, img2pdf
# $ pip install selenium requests img2pdf
#
# Download ChromeDriver from https://chromedriver.chromium.org/downloads
# or on macOS: $ brew cask install chromedriver
# Test case: scribd.com
# May work with other sites besides scribd.com (but won't work if the images are blurred)

from urllib.parse import urlparse
import fnmatch
import requests
import argparse
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time
import math
import img2pdf

__VERSION__ = "0.1"

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", dest='url', help="Webpage URL")
parser.add_argument("-f", "--file", dest='file', help="Destination file/folder")
parser.add_argument("-a", "--headless", dest='headless', action='store_true', help="Start a Headless browser")
parser.add_argument("-e", "--element", dest='element', help="HTML element that should be present before scroll down")
parser.add_argument("-t", "--timeout", dest='timeout', help="Timeout for HTML element presence to be found")
parser.add_argument("-d", "--discard", dest='discard', action='store_true', help="Discard image files downloaded")
parser.add_argument("-p", "--pause", dest='pause', help="Pause time between scroll downs. Default: 0.05")
parser.add_argument("-r", "--regex", dest='regex', help="Regular expression to find image links on page")
parser.add_argument("-q", "--quiet", dest='quiet', action='store_true', help="Quiet mode")
parser.add_argument("--height", dest='height', help="Screen height for scroll down. Default: 1080")
parser.add_argument("--firefox", dest='firefox', action='store_true', help="Loads Firefox instead of Chrome")
args = parser.parse_args()


def usage():
    args.quiet or \
        print("Usage: $0 -u|--url <url> [-f|--file <filename>] "
              "[-e|--element <html element>] [-r|--regex <regex>] [-a|--headless] [-d|--discard] "
              "[-t|--timeout <secs>] [-p|--pause <secs>] [--height <pixels>] [-q|--quiet] [--firefox]"
              "\nOnly -u|--url is mandatory."
              "\n\nExample:\n"
              "$0 -u https://www.scribd.com/doc/.../...")
    exit(1)


def create_export_folder(filename_folder):
    # Uses filename to create a folder without the extension
    folder_name = filename_folder.rsplit('.', 1)[0]
    try:
        os.makedirs(folder_name)
    except OSError:
        pass


def download_images_from_list(image_list, destination_folder):
    for image in image_list:
        image_filename = image.rsplit('/', 1)[1]
        # Get binary content:
        if not os.path.exists(destination_folder + '/' + image_filename):
            r = requests.get(image)
            with open(destination_folder + '/' + image_filename, 'wb') as f:
                f.write(r.content)
                args.quiet or print("File " + image_filename + " downloaded.")

    args.quiet or print("\nImages downloaded to folder " + destination_folder + ".")


def append_pdf(image_list, destination_folder):
    extension = str(image_list[0]).rsplit('.', 1)[1]

    with open(destination_folder + ".pdf", "wb") as f:
        os.chdir(destination_folder)
        f.write(img2pdf.convert([i for i in image_list if i.endswith(extension)]))
    args.quiet or print("Done. PDF generated as file " + destination_folder + ".pdf")


def check_url(url):
    if urlparse(url):
        return True
    return False


def check_filename(filename):
    re_obj = re.compile(fnmatch.translate('*.*'))
    if filename is None or re_obj.match(filename):
        return True
    return False


def main():
    start_time = time.time()
    check_url(args.url) or usage()
    check_filename(args.file) or usage()
    args.quiet or print("webimage2pdf " + __VERSION__)

    # Why Selenium? Because some pages depend on Javascript to load the images.
    if not args.firefox:    # Chrome
        options = Options()
        if args.headless:
            options.headless = True
        driver = webdriver.Chrome(options=options)
        args.quiet or print("Chrome initialized.")
    else:   # Firefox
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        options = FirefoxOptions()
        if args.headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        args.quiet or print("Firefox initialized.")

    driver.get(args.url)

    timeout = 10    # default timeout
    if args.timeout:
        timeout = args.timeout

    try:
        if args.element:
            element_present = ec.presence_of_element_located((By.ID, args.element))
            WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        args.quiet or print("Timed out waiting for page to load.")
    finally:
        args.quiet or print("Page loaded.")

        # Why scroll? Because some pages only load the images after the user scrolls the page down.
        scroll_pause_time = 0.05    # default pause
        if args.pause:
            scroll_pause_time = float(args.pause)

        # Get page height
        page_height = driver.execute_script("return document.body.scrollHeight")

        slice_height = 1080     # default height
        if args.height:
            slice_height = int(args.height)

        takes = math.ceil(page_height / slice_height)
        if takes > 1:
            args.quiet or print("Scrolling down...")
        for i in range(takes):
            # Scroll down
            driver.execute_script("window.scrollTo(0, " + str(i * slice_height) + ");")

            # Wait to load page
            time.sleep(float(scroll_pause_time))

        page_source = driver.page_source
        driver.quit()

        regex = 'https://.*jpg'     # default regex
        if args.regex:
            regex = args.regex

        image_list = re.findall(regex, page_source)
        if not args.file:
            destination_folder = args.url.rsplit('/', 1)[1]
        else:
            destination_folder = args.file

        if not args.discard:
            create_export_folder(destination_folder)
            download_images_from_list(image_list, destination_folder)
            # Not discard: remove 'http' from images names to use in append_pdf()
            for idx, item in enumerate(image_list):
                if 'http' in item:
                    image_list[idx] = item.rsplit('/', 1)[1]

        append_pdf(image_list, destination_folder)
        args.quiet or print("Runtime took " + str(round(time.time() - start_time, 2)) + " seconds.")


if __name__ == "__main__":
    main()
