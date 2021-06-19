import schedule
import time
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())


def some_job():
    driver.get('https://fast.com')
    time.sleep(10)
    value = driver.find_element_by_xpath('//*[@id="speed-value"]').text
    print("Internet Speed:",value)
    print ("Current time",datetime.now())

"""
schedule.every(30).minutes.do(some_job)

while True:
    schedule.run_pending()
    time.sleep(1)
"""

some_job()
