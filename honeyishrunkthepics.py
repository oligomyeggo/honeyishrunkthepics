# honeyishrunkthepics.py compresses html files with inline data-uri PNG images.
# It extracts all PNG images from an html file, optimizes them, then sticks them back in.
# This greatly reduces the size of large html files.

# This script uses Crunch, a tool for lossy PNG image file optimization.
# Installation and usage for Crunch can be found here: https://github.com/chrissimpkins/Crunch

import base64
import codecs
from bs4 import BeautifulSoup
import pathlib
import time
import subprocess
import glob
import re
import shutil
import sys, argparse
import os

# Specifying command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("html_file", help="path to html file or directory of html files with inline data-uri PNG images")
parser.add_argument("-o", "--optimizer", help="custom optimizer command", default="crunch *.png")
parser.add_argument("-c", "--clean_up", help="remove temp folder", default=False)

args = parser.parse_args()

# Make path to a temp folder for html images
tmp_path = f"/tmp/img_folder_{time.time()}"
pathlib.Path(tmp_path).mkdir()

def main(argv):

    # Resolving input (if single file path vs. path to directory of files)
    pattern = args.html_file
    if pattern[-4:] != 'html':
        pattern += "*.html"

    html_paths = glob.glob(pattern)
    for path in html_paths:
        honeyishrunkthepics(path)

def honeyishrunkthepics(input_path):

    # Open html file
    html_file = codecs.open(input_path, "r", "utf-8")

    # Parse html file
    parsed_html = BeautifulSoup(html_file, "html.parser")

    # Get all images from parsed html file
    images = parsed_html.body.find_all("img")

    # Decoding and exporting all images
    for i, img in enumerate(images):
        img_file = open(f"{tmp_path}/img-{i}.png", "wb")
        img_file.write(base64.b64decode(img.get('src')[22:]))
        img_file.close()

    # Crunch the images
    subprocess.call(args.optimizer, shell=True, cwd=tmp_path)

    # Get list of crunched image paths, and sort
    img_crunch = glob.glob(f"{tmp_path}/img-*-crunch.png")
    img_crunch = sorted(img_crunch, key=lambda x:int(re.findall(r"(\d+)",x)[2]))

    # Open crunched images, encode, and put back into html file
    for i, img in enumerate(img_crunch):
        img_file = open(img, "rb")
        img_data = base64.b64encode(img_file.read())
        img_data = img_data.decode('utf-8')
        images[i]["src"] = f"data:image/png;base64,{img_data}"
        img_file.close()

    # Write new crunched html file
    with open(f"{input_path[0:-5]}_crunched.html", "w") as file:
        file.write(str(parsed_html))

    # Remove temp folder
    if args.clean_up:
        shutil.rmtree(tmp_path)

if __name__ == '__main__':
    main(sys.argv[1:])