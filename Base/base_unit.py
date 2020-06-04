import unittest
from Common.function import config_url
from selenium import webdriver

class UnitBase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get(config_url())
        cls.driver.maximize_window()

    def tearDown(cls):
        cls.driver.quit()

