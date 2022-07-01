
import pathlib
import unittest
import os

from selenium import webdriver

class WebpageTests(unittest.TestCase):
    
    def test_title(self):
        driver = webdriver.Chrome()
        driver.get("http://localhost:8000/")
        self.assertEqual(driver.title, "Social Network")

if __name__ == "__main__":
    unittest.main()