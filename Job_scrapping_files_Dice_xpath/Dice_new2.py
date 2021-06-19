import re
import datetime
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains
import urllib3
import csv
from bs4 import BeautifulSoup
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from JobPortal_Common_Defs import JobPortal_Common
import Driver_Paths


class Dice:
    try:
        dice_job_email = []
        dice_job_phoneNo = []
        driver = None
        start_time = datetime.now()
        url = ""
        wait = ''
        link_count = 0
        job_count = []
        job_details = {'Job Category': '', 'Date Time Scrapped': '', 'Searched Job Title': '', 'Searched Job Location': '',
                       'Job Portal': 'Dice', 'Job Date Posted': '', 'Job Title': '',
                       'Job Company Name': '', 'Job Location': '', 'Job Phone No': '', 'Job Email': '', 'Job Link': '',
                       'Job Description': ''}

        def __init__(self, driver, url):
            try:
                print(self.start_time)
                self.driver = driver
                self.url = url
                self.wait = WebDriverWait(self.driver, 30)
                logging.basicConfig(filemode='a', format='%(name)s - %(levelname)s - %(message)s',
                                    level=logging.INFO)

                logging.info("######################################################################### \n"
                             "                                                                          \n"
                             "===========================Dice Job Search=============================\n"
                             "                                                                          \n"
                             "##########################################################################")
                logging.info(url)
            except Exception as e:
                print("Unknown Exception in Dice class __init__ ", e)
                logging.exception("Unknown Exception in Dice class __init__ ")
                logging.exception(e)

        # search jobs
        def dice_search_jobs(self, jp_common, job_title, job_location):
            try:
                print("In dice_search_jobs")

                # Finding Job Title Textbox element and sending text.
                job_title_web_element = jp_common.find_web_element("//*[@data-cy='typeahead-input']",
                                                                   "Job Title Textbox", "one", self.wait)
                jp_common.web_element_action(job_title_web_element, "send_keys", job_title, "Job Title Textbox")

                # Finding Job Location Textbox element and sending text.
                job_location_web_element = jp_common.find_web_element("//*[@data-cy='google-location-search-input']",
                                                                      "Job Location Textbox", "one", self.wait)
                jp_common.web_element_action(job_location_web_element, "send_keys", job_location,
                                             "Job Location Textbox")

                # Finding Search Button element and clicking it.
                search_web_element = jp_common.find_web_element("//*[@data-cy='submit-search-button']", "Search Button",
                                                                "one", self.wait)
                jp_common.web_element_action(search_web_element, "click", "", "Search Button")
                # Loading 100 jobs in one page
                selection_web_element = jp_common.find_web_element("//*[@id ='pageSize_2']", "Set 100", "one",
                                                                   self.wait)
                jp_common.web_element_action(selection_web_element, "select", "", "Set 100")

                # Search only jobs that posted today
                today_web_element = jp_common.find_web_element("//button[contains(text(),'Today')]",
                                                               "Today", "one",
                                                               self.wait)
                jp_common.web_element_action(today_web_element, "click", "", "Today")
                # Exclude Remote jobs
                remote_web_element = jp_common.find_web_element("//*[contains(text(),'Exclude Remote')]",
                                                                "ExcludeRemote", "one", self.wait)
                jp_common.web_element_action(remote_web_element, "click", "", "ExcludeRemote")
                time.sleep(2)


            except Exception as e:
                print("Unexpected error in dice_search_jobs", e)
                logging.exception("Unexpected exception in dice_search_jobs")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_search_jobs_exception.png")

        def dice_valid_job(self, jp_common):
            try:
                logging.info("In dice_valid_jobs")
                print("In dice_valid_jobs")
                msg = "New Jobs in U.S"
                if msg == "Sorry, we didn't find any jobs matching your criteria":

                    return False
                else:
                    return True
            except Exception as e:
                print("Unexpected error in dice_valid_jobs", e)
                logging.error("Unexpected exception in dice_valid_jobs")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_valid_jobs_exception.png")

        def dice_loadmore_jobs(self):
            logging.info("In dice_loadmore_jobs")
            print("In dice_loadmore_jobs")
            click = 0
            # time.sleep(3)
            try:

                click += 1
                self.driver.switch_to.window(self.driver.window_handles[0])
                load_more_1 = self.driver.find_elements_by_xpath("//*[@class= 'pagination']/li")
                length = len(load_more_1)
                print(length)
                # pagination = str(load_more_1[length - 1].get_attribute("class"))
                try:
                    if load_more_1[length - 1].get_attribute("class") == "pagination-next page-item ng-star-inserted disabled":
                        return False
                    else:
                        load_more_1[length - 1].click()
                        print("LoadMore jobs clicked")
                        time.sleep(8)
                        return True
                except Exception as e:
                    logging.exception("Unexpected error when clicking load more button")
                    logging.exception(e)
                    print("Unexpected error when clicking load more button", e)

            except Exception as e:
                print("Unexpected error in dice_loadmore_jobs", e)
                logging.error("Unexpected exception in dice_loadmore_jobs" + str(e))
                self.driver.get_screenshot_as_file("Screenshots\monster_load_more_jobs_exception.png")

        # Get list of job links populated
        def dice_get_job_links(self, jp_common):
            #  job links xpath
            print("In dice_get_job_links")
            logging.info("In dice_get_job_links")
            self.driver.switch_to.window(self.driver.window_handles[0])
            try:
                # job_links_web_element = jp_common.find_web_element(
                #     "//*[@id='searchDisplay-div']/div[2]/dhi-search-cards-widget/div/dhi-search-card/div/div/div/div[2]/div/h5/a",
                #     "Job Links", "multiple", self.wait)
                job_links_web_element = self.driver.find_elements_by_xpath("//*[@id='searchDisplay-div']/div[2]/dhi-search-cards-widget/div/dhi-search-card/div/div/div/div[2]/div/h5/a")
                return job_links_web_element

            except Exception as e:
                print("Unknown Exception in dice_get_jobs_links", e)
                logging.error("Unknown Exception in dice_get_jobs_links")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_job_links_exception.png")

        # Get list of job company names
        def dice_get_job_company(self, jp_common):
            print("In dice_get_job_company")
            logging.info("In dice_get_job_company")
            try:
                job_company_web_element = jp_common.find_web_element("//span[@id='hiringOrganizationName']",
                                                                     "Job Company Name", "one", self.wait)
                # print(job_company_web_element.text)
                self.job_details['Job Company Name'] = job_company_web_element.text
                #return job_company_web_element
            except Exception as e:
                print("Unknown Exception in dice_get_job_company", e)
                logging.error("Unknown Exception in dice_get_job_company")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_job_company.png")

        # Get names of job locations
        def dice_get_job_location(self, jp_common):
            print("In dice_get_job_location")
            logging.info("In dice_get_job_location")
            try:
                job_location_web_element = jp_common.find_web_element("//ul[@class='list-inline details']/li[2]",
                                                                      "Job Location", "one", self.wait)
                self.job_details['Job Location'] = job_location_web_element.text
                #return job_location_web_element
            except Exception as e:
                print("Unknown Exception in get_jobs_location".e)
                logging.error("Unknown Exception in get_jobs_location")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_job_location_exception.png")

        # Get Date-time of job posted
        def dice_get_job_posted_datetime(self, jp_common):
            print("In dice_get_posted_datetime")
            logging.info("In dice_get_posted_datetime")
            try:
                job_posted_datetime_web_element = jp_common.find_web_element(
                    "//ul[@class='list-inline details']/li[3]/span",
                    "Job Date Posted", "one", self.wait)
                # print(job_posted_datetime_web_element.text)
                self.job_details['Job Date Posted'] = job_posted_datetime_web_element.text
                #return job_posted_datetime_web_element
            except Exception as e:
                print("Unknown Exception in dice_get_jobs_poster_datetime")
                logging.error("Unknown Exception in dice_get_jobs_poster_datetime")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_job_posted_datetime_exception.png")

        # Get Job description and scrape Email and Phone number
        def dice_get_job_desc(self, job_title, job_loc, job_links, jp_common):
            print("In dice_get_jobs_desc")
            logging.info("In dice_get_jobs_desc")
            # print(self.driver.page_source)
            # if "//*[@id='JobBody']" in self.driver.page_source:
            #     print("yes")
            # else:
            #     print("no")
            # breakpoint()
            try:
                #self.link_count = 0
                self.job_details['Searched Job Title'] = job_title
                self.job_details['Searched Job Location'] = job_loc
                print(len(job_links))
                about = []
                for a in job_links:
                    about.append(a.get_attribute("href"))
                # print(about)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                for link in about:
                    job_desc = []
                    self.driver.get(link)
                    # logging.info("job title: " + link.text)
                    # logging.info("Dice, Link clicked  :" + job_title + " " + job_loc + " " + str(
                    #     self.link_count + 1) + " / " + str(len(job_links)))
                    #
                    # logging.info("==============================================> " + str(self.link_count + 1))
                    try:
                        job_title_web_element = jp_common.find_web_element("//h1[@id='jt']","Job Title","one",self.wait)
                        self.job_details['Job Title'] = job_title_web_element.text
                        #self.job_details['Job Title'] = self.driver.find_element_by_xpath("//h1[@id='jt']").text
                        self.dice_get_job_company(jp_common)
                        self.dice_get_job_location(jp_common)
                        self.dice_get_job_posted_datetime(jp_common)
                        time.sleep(2)
                        # job_description_web_element = self.driver.find_element_by_xpath("//*[@id ='jobdescSec']").text
                        job_description_web_element = jp_common.find_web_element(
                            "//*[@id ='jobdescSec']", "Job Description", "multiple", self.wait)
                        for element in job_description_web_element:
                            job_desc.append(element.text)
                    except Exception as e:
                        print("Unknown Exception occurred while clicking to get job description", e)
                        logging.error("Unknown Excecption occurred while clicking to get job description")
                        logging.exception(e)
                    else:
                        job_desc = ' '.join(map(str, job_desc))
                        # print(job_desc)
                        #self.job_details['Job Description'] = job_description_web_element
                        self.job_details['Job Description'] = job_desc
                        self.job_details['Job Email'] = jp_common.get_Email_desc(job_desc)
                        logging.info(self.job_details['Job Email'])
                        self.job_details['Job Phone No'] = jp_common.get_Phno_desc(job_desc)
                        logging.info(self.job_details['Job Phone No'])

                        self.job_details['Date Time Scrapped'] = datetime.now().strftime("%b-%d-%Y %H:%M:%S")
                        if len(self.job_details['Job Email']) != 0 or len(self.job_details['Job Phone No']) != 0:
                            jp_common.write_to_csv(self.job_details)
                # about.send_keys(Keys.COMMAND + 'W')
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.link_count += 1

                #  self.driver.page_source
            except Exception as e:
                print("Unknown exception in dice_get_job_desc", e)
                logging.error("Unknown exception in dice_get_job_desc")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_job_desc_exception.png")

        # To get jobs from the user given choices
        def dice_get_jobs(self, job_title, job_loc, jp_common):
            print("In dice_get_jobs")
            logging.info("In dice_get_jobs")
            try:
                jp_common.get_url(self.driver, self.url)
                # for title, loc in zip(arr[0], arr[1]):
                #     job_title = title
                #     job_loc = loc
                self.dice_clear_search(job_title, job_loc)
                self.dice_search_jobs(jp_common, job_title, job_loc)

                if (self.dice_valid_job(jp_common) == True):
                    job_links = self.dice_get_job_links(jp_common)
                    if job_links:
                        self.driver.execute_script("window.open('')")
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        self.job_details['Job Category'] = jp_common.set_job_category(job_title)
                        logging.info(
                            "Links Populated for Dice : " + job_title + " " + job_loc + " are : " + str(len(job_links)))
                        self.dice_get_job_desc(job_title, job_loc, job_links, jp_common)
                        #self.job_count.append(self.link_count)
                        jp_common.get_all_phno()
                        jp_common.get_all_email()
                        while self.dice_loadmore_jobs():
                            job_links = self.dice_get_job_links(jp_common)
                            if job_links:
                                self.driver.execute_script("window.open('')")
                                self.driver.switch_to.window(self.driver.window_handles[0])
                                self.job_details['Job Category'] = jp_common.set_job_category(job_title)
                                logging.info(
                                    "Links Populated for Dice : " + job_title + " " + job_loc + " are : " + str(
                                        len(job_links)))
                                self.dice_get_job_desc(job_title, job_loc, job_links, jp_common)
                                # self.job_count.append(self.link_count)
                                jp_common.get_all_phno()
                                jp_common.get_all_email()

                        self.dice_clear_search(job_title, job_loc)
                    else:
                        print("no jobs found in:" + job_loc + " with job title " + job_title)
                        logging.info("no jobs found in:" + job_loc + " with job title " + job_title)
                        self.dice_clear_search(job_title, job_loc)
                    # self.report(arr,"Sorry no jobs matching your search",jp_common)
                # else:
                #
                #     self.driver.switch_to.window(self.driver.window_handles[-1])
                #     self.driver.close()
                jp_common.time_to_execute()
            except Exception as e:
                print("Unknown exception in dice_get_jobs", e)
                logging.error("Unknown exception in dice_get_jobs")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_jobs_exception.png")


        # clear search boxes
        def dice_clear_search(self, job_title, job_loc):
            print("In dice_clear_search")
            logging.info("dice_clear_search")
            try:
                for i in range(len(job_title)):
                    self.driver.find_element_by_xpath("//*[@data-cy='typeahead-input']").send_keys(Keys.BACKSPACE)

                for i in range(len(job_loc)):
                    self.driver.find_element_by_xpath("//*[@id='google-location-search']").send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE)

            except Exception as e:
                print("Unknown exception in dice_clear_search", e)
                logging.error("Unknown exception in dice_clear_search")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_clear_search_exception.png")

        def report(self, arr, msg,jp_common):
            try:
                logging.info("================================")
                logging.info("=======Dice Report===========")
                for title, loc, count in zip(arr[0], arr[1], range(len(self.job_count))):
                    if len(self.job_count) > 0:
                        logging.info(title + " " + loc + ":" + str(self.job_count[count]) + " Jobs")
                    else:
                        logging.info(title+"  "+ loc + " : "+ msg)
                logging.info("Total Dice Execution :" + str(jp_common.time_to_execute()))
                logging.info("================================")
            except Exception as e:
                print("Unknown exception in dice_clear_search", e)
                logging.exception("Unknown exception in dice_clear_search")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_clear_search_exception.png")

    except Exception as e:
        print("Unknown Exception occurred in Class Dice", e)
        logging.error("Unknown Exception occurred in Class Dice")
        logging.exception(e)
        driver.get_screenshot_as_file("Screenshots\monster_class_exception.png")


# job_search=["Java Developer","Seattle"]
# job_search=["SDET","Python Developer","Java Developer","Chicago","Seattle","Atlanta"]
#job_search = ["SDET", "Chicago"]
#job_search = ["SDET", "atlanta"]

#job_search = ["SDET", "SDET", "SDET", "Chicago", "Oregon", "atlanta"]
#job_search=["sdet","Oregon"]
#job_search=["python SDET","Atlanta"]

# job_search=["Python SDET","DS", "Atlanta", "Seattle"]
#job_search=["SDET","Franklin-TN"]
# job_search=["Python Developer","New York"]
# print(job_search)
# job_arr = np.array(job_search).reshape(2, int(len(job_search) / 2))
# jp_common = JobPortal_Common()
# driver = jp_common.driver_creation("chrome")
# dice_obj = Dice(driver, Driver_Paths.dice_url)
# dice_obj.dice_get_jobs(job_arr, jp_common)
