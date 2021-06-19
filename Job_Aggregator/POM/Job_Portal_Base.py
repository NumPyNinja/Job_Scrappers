import logging
import re
from abc import abstractmethod
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait




def get_contact_details(job_desc):
    logging.info("getting job company url")
    job_phone_no_list = []
    try:
        # Get phone and store
        phone_no_match = re.findall(r'[0-9]{3}-[0-9]{3}-[0-9]{4}|[+][1]\s[0-9]{3}\s[0-9]{3}\s[0-9]{4}|'
                                    r'[(][0-9]{3}[)]\s[0-9]{3}-[0-9]{4}', job_desc)
        # phoneNo_match = re.findall(r'[0-9]{3}-[0-9]{3}-[0-9]{4}', job_desc)
        for phoneNo in phone_no_match:
            if phoneNo not in job_phone_no_list:
                job_phone_no_list.append(phoneNo)
    except Exception as e:
        logging.exception("Exception in getting job phone no.")

    return ", ".join(job_phone_no_list)


def get_job_email_address(job_desc):
    logging.info("getting job company url")
    email_list = []
    try:
        # print(job_desc)
        email_match = re.findall(r'[\w\.-]+@[\w\.-]+', job_desc)
        for email in email_match:
            # if not ("accommodation" in email or "disabilit" in email or "employeeservice" in email ):
            if not (
                    re.search('accommodation', email, re.IGNORECASE) or
                    re.search('disabilit', email, re.IGNORECASE) or
                    re.search('employeeservice', email, re.IGNORECASE) or email in email_list
            ):
                email_list.append(email)
    except:
        logging.error("Exception in getting email address", exc_info=True)

    return ', '.join(email_list)


class JobPortal:
    driver: webdriver = None
    wait: WebDriverWait = None
    current_job = None

    job_details = {'Job Category': '', 'Date&Time': '', 'Searched Job Title': '', 'Searched Job Location': '',
                   'Job Portal': '', 'Job Date Posted': '', 'Job Title': '',
                   'Job Company Name': '', 'Job Location': '', 'Job Phone No': '', 'Job Email': '', 'Job Link': '',
                   'Job Description': ''}

    @abstractmethod
    def get_job_title_input_box(self) -> webelement:
        pass

    @abstractmethod
    def get_job_location_input_box(self) -> webelement:
        pass

    @abstractmethod
    def apply_job_filters(self) -> webelement:
        pass

    @abstractmethod
    def get_job_list(self) -> webelement:
        pass

    @abstractmethod
    def get_jobs_next_page(self):
        pass

    @abstractmethod
    def get_job_title(self):
        pass

    @abstractmethod
    def get_job_company_name(self):
        pass

    @abstractmethod
    def get_job_posting_location(self):
        pass

    @abstractmethod
    def get_job_posted_date(self):
        pass

    @abstractmethod
    def is_job_found(self):
        pass

    @abstractmethod
    def get_job_description(self):
        pass

    @abstractmethod
    def set_job_location_and_search(self, job_location):
        pass

    @abstractmethod
    def open_job(self, job):
        pass

    @abstractmethod
    def close_job(self):
        pass

    def get_job_url(self):
        try:
            logging.info("getting job company url")
            return self.driver.current_url
        except Exception as e:
            logging.exception(" error in fetching job url")
            return

    def get_element(self, locator: ()) -> webelement:
        try:
            logging.info("searching for webelement with \"" + locator[1] + "\"")
            return self.wait.until(EC.presence_of_element_located(locator))
            #return self.driver.find_element(locator[0], locator[1])
        except Exception as e:
            filename = "Screenshot\error-" + datetime.now().strftime("%m-%d-%Y-%H-%M-%S") + ".png"
            logging.exception("failed to get webelement \"" + locator[1] + "\" .screenshot captured at " + filename)
            self.driver.get_screenshot_as_file(filename)
            raise

    def get_elements(self, locator: ()) -> list:
        try:
            logging.info("searching for webelements with \"" + locator[1] + "\"")
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except Exception as e:
            filename = "Screenshot\error-" + datetime.now().strftime("%m-%d-%Y-%H-%M-%S") + ".png"
            logging.exception("failed to get webelements \"" + locator[1] + "\" .screenshot captured at " + filename)
            self.driver.get_screenshot_as_file(filename)
            raise

    def get_child_element(self, element: webelement, locator: ()) -> webelement:
        try:
            logging.info("searching for webelement with \"" + locator[1] + "\"")
            return element.find_element(locator[0], locator[1])
        except Exception as e:
            filename = "Screenshot\error-" + datetime.now().strftime("%m-%d-%Y-%H-%M-%S") + ".png"
            logging.exception("failed to get webelement \"" + locator[1] + "\" .screenshot captured at " + filename)
            self.driver.get_screenshot_as_file(filename)
            raise

    def get_child_elements(self, element: webelement, locator: ()) -> list:
        try:
            logging.info("searching for webelements with \"" + locator[1] + "\"")
            return element.find_elements(locator[0], locator[1])
        except Exception as e:
            filename = "Screenshot\error-" + datetime.now().strftime("%m-%d-%Y-%H-%M-%S") + ".png"
            logging.exception("failed to get webelements \"" + locator[1] + "\" .screenshot captured at " + filename)
            self.driver.get_screenshot_as_file(filename)
            raise

    def get_job_details(self, job: webelement):
        self.current_job = job
        self.open_job(job)
        self.job_details["Job Title"] = self.get_job_title()
        self.job_details["Job Company Name"] = self.get_job_company_name()
        self.job_details["Job Location"] = self.get_job_posting_location()
        self.job_details["Job Date Posted"] = self.get_job_posted_date()
        self.job_details["Job Description"] = self.get_job_description()
        self.job_details["Job Email"] = get_job_email_address(self.job_details["Job Description"])
        self.job_details["Job Phone No"] = get_contact_details(self.job_details["Job Description"])
        self.job_details["Date&Time"] = datetime.now().strftime("%b-%d-%Y %H:%M:%S")
        self.job_details["Job Link"] = self.get_job_url()
        self.close_job()
        return self.job_details
