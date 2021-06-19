import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from POM.Job_Portal_Base import JobPortal


class Monster (JobPortal):
    LOCATION_INPUT_BOX_LOCATOR = (By.ID, "where2")
    TITLE_INPUT_BOX_LOCATOR = (By.ID, 'q2')
    JOB_LIST_LOCATOR = (By.CSS_SELECTOR, "div[class='flex-row']")
    FILTER_BUTTON_LOCATOR = (By.CSS_SELECTOR, "button[id='filter-flyout']")

    def __init__(self, driver: webdriver):
        logging.info("creating monster class")
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        logging.info("Monster site opening")
        self.driver.get("https://www.monster.com//")

    def get_job_location_input_box(self):
        logging.info("getting monster job location box ")
        return self.get_element(self.LOCATION_INPUT_BOX_LOCATOR)

    def set_job_location_and_search(self, job_location):
        job_location_input_box = self.get_job_location_input_box()
        job_location_input_box.send_keys(Keys.CONTROL, "a", Keys.DELETE)
        logging.info("sending job location " + "\"" + job_location + "\"")
        job_location_input_box.send_keys(job_location, Keys.RETURN)

    def get_job_title_input_box(self):
        logging.info("getting monster job title box")
        return self.get_element(self.TITLE_INPUT_BOX_LOCATOR)

    def get_job_list(self):
        logging.info("getting monster job list")
        while True:
            try:
                load_more_jobs = self.wait.until(expected_conditions.presence_of_element_located((By.ID, "loadMoreJobs")))
                load_more_jobs.click()
                time.sleep(1)
            except:
                try:
                    load_more_jobs = self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//button[@class='mux-btn fenced-btn']/span[text()='SHOW RELATED RESULTS']")))
                    load_more_jobs.click()
                    time.sleep(1)
                except:
                    break

        return self.get_elements(self.JOB_LIST_LOCATOR)

    def apply_job_filters(self) -> webelement:
        logging.info("get all the jobs posted today")
        self.get_element(self.FILTER_BUTTON_LOCATOR).click()
        select = Select(self.get_element((By.ID, "FilterPosted")))
        select.select_by_visible_text("Today")
        self.get_element((By.ID, 'use-filter-btn')).click()

    def get_job_title(self):
        try:
            logging.info("getting job title")
            return self.get_element((By.CSS_SELECTOR, "h1[class='title']")).text
        except:
            return ""

    def get_job_company_name(self):
        try:
            logging.info("getting job company information")
            return self.get_child_element(self.current_job, (By.CSS_SELECTOR, "div[class='company']>span")).text

        except:
            return ""

    def get_job_posting_location(self):
        try:
            logging.info("getting job location")
            return self.get_child_element(self.current_job, (By.CSS_SELECTOR, "div[class='location']>span")).text
        except:
            return ""

    def get_job_posted_date(self):
        try:
            logging.info("getting job posted date")
            return self.get_child_element(self.current_job, (By.CSS_SELECTOR, "div[class='meta flex-col']>time")).text
        except:
            return ""

    def is_job_found(self):
        try:
            logging.info("relevant jobs as per job search not found")
            self.wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "h1[class='pivot block']")))
            return False
        except:
            logging.info("relevant jobs as per job search found")
            return True

    def get_job_description(self):
        try:
            logging.info("getting job description")
            return self.get_element((By.ID, "JobDescription")).text
        except:
            return ""

    def open_job(self, job):
        logging.info("opening single job ")
        self.get_child_element(job, (By.CSS_SELECTOR, "div[class='summary'] header")).click()

    def close_job(self):
        return



    def get_jobs_next_page(self):
        return []





