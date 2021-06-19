import logging
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def get_driver() -> webdriver:
    try:
        logging.info("creating chrome driver")
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificates-errors')
        options.add_argument("--test-type")

        #driver = webdriver.Chrome(executable_path="c:\\chromedriver.exe", options=options)
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        driver.maximize_window()
        #driver.implicitly_wait(2)
        logging.info("driver created successfully")

        return driver
    except:
        logging.exception("failed to create driver")
        sys.exit()















