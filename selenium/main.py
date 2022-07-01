import pathlib
import unittest
import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

driver = webdriver.Chrome(ChromeDriverManager().install())

class WebpageTests(unittest.TestCase):
    
    def test_title(self):
        driver.get("http://localhost:8000/")
        self.assertEqual(driver.title, "Social Network")

if __name__ == "__main__":
    unittest.main()