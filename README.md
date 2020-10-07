# honeyishrunkthepics
Helper function to compress overall size of html files by optimizing inline data-uri PNG images.

## Usage

Example usage for single file:

```
python honeyishrunkthepics.py my_giant_file.html
```

Example usage for directory:

```
python honeyishrunkthepics.py path/to/my_giant_files
```

## Dependencies

`honeyishrunkthepics.py` uses [Crunch](https://github.com/chrissimpkins/Crunch) as a default optimizer for PNG image files. In order to run `honeyishrunkthepics.py` you must first have `Crunch` installed and in your path. Alternatively you can provide a command for your own image optimizer using the `-o` option.

`honeyishrunkthepics.py` also uses [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for parsing and manipulating the html files. In order to run `honeyishrunkthepics.py` you must first have `BeautifulSoup` installed.