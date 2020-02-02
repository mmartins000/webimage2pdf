# webimage2pdf

webimage2pdf scrapes images from webpages, downloads and combines them into one PDF file.
fileimage2pdf combines images from a single folder into one PDF file.

### Why?

### webimage2pdf

To help download and combine images that would take a lot of time and effort. 

Initial use case: to read documents freely available on [Scribd](https://scribd.com).

But it is possible to use the script on other websites, as long as they have a consistent naming scheme for their image filenames and URLs. 

### fileimage2pdf

To help in those situations when you can only send one PDF file but have several images to send. 

## Release notes

This repository contains webimage2pdf and fileimage2pdf. 

## Requirements

### webimage2pdf

Based on Python 3 and requires the packages Selenium, Requests, img2pdf

- Clone this repository (or download the single Python script)
- Install the packages
  - $ pip install seleniumhq requests img2pdf
- Download ChromeDriver from https://chromedriver.chromium.org/downloads or:
  - macOS: $ brew cask install chromedriver

### fileimage2pdf

Based on Python 3 and requires the package img2pdf

- Clone this repository (or download the single Python script)
- Install the packages
  - $ pip install img2pdf

## Execution

### webimage2pdf

- Run
  - $ python3 webimage2pdf.py -u https://example.com/directory/page

#### Command line options

Usage: python3 webimage2pdf.py \<options\>

- -u|--url url: Webpage URL
- [-f|--file \<filename\>]: Destination file/folder
- [-e|--element \<html element\>]: HTML element that should be present before scroll down starts
- [-r|--regex \<regex\>]: Regular expression to find image links on page. Default: https://.*jpg 
- [-a|--headless]: Start a Headless browser
- [-d|--discard]: Discard jpg files downloaded
- [-t|--timeout \<secs\>]: Timeout for HTML element presence to be found
- [-p|--pause \<secs\>]: Pause time between scroll downs. Default: 0.05
- [--height \<pixels\>]: Screen height for scroll down. Default: 1080
- [-q|--quiet]: Quiet mode (absolutely zero output, in case of error exits with error code 1)
- [--firefox]: Loads Firefox instead of Chrome

Only -u|--url is mandatory.

Example:
$ python3 webimage2pdf.py -u https://www.scribd.com/doc/.../..."

### fileimage2pdf

- Run
  - $ python3 fileimage2pdf.py -f ~/Documents/images/

#### Command line options

Usage: python3 fileimage2pdf.py \<options\>

- -f|--folder \<folder name\>: Source folder
- [-q|--quiet]: Quiet mode (absolutely zero output, in case of error exits with error code 1)
