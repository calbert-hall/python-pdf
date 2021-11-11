import os
import io
import pytest
import requests
from PIL import Image
import pdfbox
from applitools.images import Eyes, BatchInfo, logger

logger.set_logger(logger.StdoutLogger())

@pytest.fixture(name="eyes", scope="function")
def eyes_setup():
    """
    Basic Eyes setup. It'll abort test if wasn't closed properly.
    """
    eyes = Eyes()
    eyes.configure.batch = BatchInfo("Demo Batch - Images - Python")
    yield eyes
    # If the test was aborted before eyes.close was called, ends the test as aborted.
    eyes.abort()


def test_tutorial(eyes):

    eyes.open("Images-PDF Python", "Test PDF")

    p = pdfbox.PDFBox()
    # Change PDF Path here
    p.pdf_to_images('/Users/casey/Desktop/Python/PDF_Images_Python/Resources/sample_pdf.pdf')

    # Change directory here
    directory = '/Users/casey/Desktop/Python/PDF_Images_Python/Resources'
    pagenum = 1
    dirList = os.listdir(directory)
    dirList.sort()
    for filename in dirList:
        if filename.endswith(".jpg") or filename.endswith(".png"):
            file = open(directory + "/" + filename, "rb")
            image = Image.open(file)
            eyes.check_image(image, "Page " + str(pagenum))
            file.flush()
            pagenum += 1

        else:
            continue

    eyes.close(False)