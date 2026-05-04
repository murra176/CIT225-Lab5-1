from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest


class TestHomepage(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

    def test_h5_tag_content(self):
        self.driver.get("http://10.48.228.111")
        h5_text = self.driver.find_element(By.TAG_NAME, "h5").text
        self.assertEqual("Pipeline Works!", h5_text)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
