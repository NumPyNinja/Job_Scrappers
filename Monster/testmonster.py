from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

geoBlocked = webdriver.FirefoxOptions()
geoBlocked.set_preference("geo.prompt.testing", True)
geoBlocked.set_preference("geo.prompt.testing.allow", False)
driver = webdriver.Firefox(options=geoBlocked)
driver.get("https://www.monster.com/jobs/search/")
sleep(2)

titleTextBox = driver.find_element_by_xpath("//input[@name='q' and @type='text']")
titleTextBox.send_keys("SDET")
#Creating object of an Actions class
actions = ActionChains(driver)
actions.send_keys(Keys.TAB * 2)
actions.perform()

driver.find_element_by_xpath("/html/body/div[1]/header/div/div[3]/div/div/div[2]/form/button").click()
sleep(2)
#jobTitle = driver.find_element_by_xpath("//h2[@class='card-title']").text

#print(jobTitle)
Job_count = driver.find_elements_by_class_name("results-card ")
print(Job_count.__sizeof__())
for job in Job_count:
    print(job.find_element_by_xpath("//h2[@name='card_title']").text)
    print(job.find_element_by_xpath("//h3[@name='card_companyname']").text)
    print(job.find_element_by_xpath("//span[@name='card_job_location']").text)
    print(job.find_element_by_xpath("//div[@name='card-job-description']").text)


    #print(job.text)
driver.close()