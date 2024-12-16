# Extract machine-readable tidal information from the PLA PDF
The Port of London Authority [publish tidal predictions](http://www.pla.co.uk/Safety/Tide-Tables) in advance for the whole year. They publish it in the form of a PDF, which is great for humans but not so good for machines. So this thing will download the PDF and OCR it to extract the raw data, so you can run your own analytics on it.

**pdf2json.py** Download, extract and analyze the tide-table PDFs, producting a JSON file for each year.

**dev_ocr.ipynb:** Jupyter notebook for a more interactive experience.

In order to use the Jupyter notebook, you must at least have downloaded and extracted data for 2025. You can do this with:

    ./pdf2json.py 2025 1,2 0-6 48

If you have access to GitHub Codespaces, you can open it there. Alternatively you can install Docker Desktop and VSCode, and just clone the repo and open it in VSCode. It should be smart enough to figure out how to start it running. The Jupyter notebook makes it very easy to analyse the data.
