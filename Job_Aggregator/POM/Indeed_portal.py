import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from POM.Job_Portal_Base import JobPortal


class Indeed(JobPortal):
    LOCATION_INPUT_BOX_LOCATOR = (By.ID, "text-input-where")
    TITLE_INPUT_BOX_LOCATOR = (By.ID, "text-input-what")
    JOB_LIST_LOCATOR = (By.CSS_SELECTOR, "[class='jobsearch-SerpJobCard unifiedRow row result clickcard']")

    def __init__(self, driver: webdriver):
        logging.info("creating Indeed class")
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        logging.info("Indeed site opening")
        self.driver.get("https://www.indeed.com/")

    def get_job_location_input_box(self):
        logging.info("getting indeed job location box ")
        return self.get_element(self.LOCATION_INPUT_BOX_LOCATOR)

    def is_job_found(self):
        try:
            logging.info("relevant jobs as per job search not found")
            self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@class='no_results']")))
            return False
        except:
            logging.info("relevant jobs as per job search found")
            return True

    def get_job_title_input_box(self):
        logging.info("getting Indeed job title box")
        return self.get_element(self.TITLE_INPUT_BOX_LOCATOR)

    def get_job_list(self):
        logging.info("creating list of dice search job title")
        time.sleep(1)
        return self.get_elements(self.JOB_LIST_LOCATOR)

    def apply_job_filters(self) -> webelement:
        logging.info("applying filters")
        try:
            self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//button/span[contains(text(),'Date Posted')]"))).click()
            self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//a/span[contains(text(),'Last 24 hours')]"))).click()
        except Exception as e:
            logging.info(" no filters found as per job search", e)

    def set_job_location_and_search(self, job_location):
        job_location_input_box = self.get_job_location_input_box()
        job_location_input_box.send_keys(Keys.CONTROL, "a", Keys.BACK_SPACE)
        logging.info("sending job location " + "\"" + job_location + "\"")
        job_location_input_box.send_keys(job_location, Keys.RETURN)

    def get_jobs_next_page(self):
        logging.info("getting next page button ")
        try:
            next_page_link = self.driver.find_element(By.CSS_SELECTOR, "ul[class='pagination-list'] li>a[aria-label='Next']")
            next_page_link.click()
            time.sleep(1)
            return self.get_job_list()
        except Exception as e:
            logging.info("next page not found")
            return []

    def get_job_title(self):
        logging.info("getting job title")
        try:
            return self.get_element((By.XPATH, "//div[contains(@class,'jobsearch-JobInfoHeader-title-container')]")).text
        except Exception as e:
            logging.warning("job title not found", e)
            return ""

    def get_job_company_name(self):
        logging.info("getting job company information")
        try:
            return self.get_element((By.XPATH, "//div[contains(@class,'jobsearch-InlineCompanyRating')]/div")).text
        except Exception as e:
            logging.warning("job company not found", e)
            return ""

    def get_job_posting_location(self):
        logging.info("getting job location")
        try:
            return self.get_element((By.XPATH, "//div[contains(@class,'jobsearch-InlineCompanyRating')]/div[not(@class)]")).text
        except Exception as e:
            logging.warning("job location not found", e)
            return ""

    def get_job_posted_date(self):
        logging.info("getting job posted date")
        try:
            return self.get_element((By.XPATH, "//div[@class='jobsearch-JobMetadataFooter']/span[not(@class)]")).text.replace('- ', "")
        except Exception as e:
            logging.warning("job posted date not found", e)
            return ""

    def get_job_description(self):
        logging.info("getting job description")
        try:
            return self.get_element((By.CSS_SELECTOR, "div[id='jobDescriptionText']")).text
        except Exception as e:
            logging.warning("job description not found", e)
            return ""

    def open_job(self, job):
        logging.info("opening single job ")
        self.wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "h2[class='title']")))
        self.get_child_element(self.current_job, (By.CSS_SELECTOR, "h2[class='title']")).click()
        self.wait.until(expected_conditions.frame_to_be_available_and_switch_to_it(0))

    def close_job(self):
        self.driver.switch_to.default_content()




