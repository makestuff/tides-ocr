# Extract machine-readable tidal information from the PLA PDF
The Port of London Authority [publish tidal predictions](http://www.pla.co.uk/Safety/Tide-Tables) in advance for the whole year. They publish it in the form of a PDF, which is great for humans but not so good for machines. So this thing will download the PDF and OCR it to extract the raw data, so you can run your own analytics on it.

**get_all.sh** Download the tide-table PDFs from the PLA website.

**get_pages.sh:** Extract the tide tables as hi-res PNG images.

**main.py:** OCR the pages, print sample.

**dev_ocr.ipynb:** Jupyter notebook for a more interactive experience.

If you have access to GitHub Codespaces, you can open it there. Alternatively you can install Docker Desktop and VSCode, and just clone the repo and open it in VSCode. It should be smart enough to figure out how to start it running. The Jupyter notebook makes it very easy to analyse the data.
