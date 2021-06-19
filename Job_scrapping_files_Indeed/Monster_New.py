import re
import datetime
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import urllib3
import csv
from bs4 import BeautifulSoup
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys
from JobPortal_Common_Defs import JobPortal_Common
import Driver_Paths
import random
from selenium.webdriver.common.keys import Keys

class Monster:
    try:
        monster_job_email = []
        monster_job_phoneNo = []
        driver = None
        start_time = datetime.now()
        url = ""
        wait = ''
        link_count = 0
        job_count = []

        # logging.basicConfig(filename='monster.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO)
        # logger = logging.getLogger(__name__)
        job_details = {'Job Category': '', 'Date&Time': '', 'Searched Job Title': '', 'Searched Job Location': '',
                       'Job Portal': 'Monster', 'Job Date Posted': '', 'Job Title': '',
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
                             "===========================Monster Job Search=============================\n"
                             "                                                                          \n"
                             "##########################################################################")
                logging.info(url)
            except Exception as e:
                print("Unknown Exception in Monster class __init__ ", e)
                logging.exception("Unknown Exception in Monster class __init__ ")
                logging.exception(e)

        # search jobs
        def monster_search_jobs(self, jp_common, job_title, job_location):
            try:
                logging.info("In monster_search_jobs")
                print("In monster_search_jobs")

                # Finding Job Title Textbox element and sending text.
                job_title_web_element = jp_common.find_web_element("//*[@id='keywords2']", "Job Title Textbox", "one",
                                                                   self.wait)
                jp_common.web_element_action(job_title_web_element, "send_keys", job_title, "Job Title Textbox")

                # Finding Job Location Textbox element and sending text.
                job_location_web_element = jp_common.find_web_element("//*[@id='location']", "Job Location Textbox",
                                                                      "one", self.wait)
                jp_common.web_element_action(job_location_web_element, "send_keys", job_location,
                                             "Job Location Textbox")

                # Finding Search Button element and clicking it.
                search_web_element = jp_common.find_web_element("//*[@id='doQuickSearch']", "Search Button", "one",
                                                                self.wait)
                jp_common.web_element_action(search_web_element, "click", "", "Search Button")
                
                time.sleep(3)
                print ("near filter")
                Filter = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="filter-flyout"]')))

                Filter.click()

                time.sleep(3)
                Last_24 = Select (self.driver.find_element_by_xpath('//*[@id="FilterPosted"]'))
                Last_24.select_by_visible_text("Today")

                time.sleep(1)

                self.driver.find_element_by_xpath('//*[@id="use-filter-btn"]').click()

                time.sleep(2)

            except Exception as e:
                print("Unexpected error in monster_search_jobs", e)
                logging.exception("Unexpected exception in monster_search_jobs")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_search_jobs_exception.png")

        def monster_search_jobs_past24hrs(self,jp_common, job_title, job_location):
                    try:
                        logging.info("In monster_search_jobs_past24hrs")
                        print("In monster_search_jobs_past24hrs")
                        #breakpoint()
                        print(jp_common.find_web_element("//*[@id='main-nav-0']/a", "Find Jobs Select box",
                                                                           "one",self.wait))
                        # Choose Find Jobs-> Advanced Search
                        find_jobs_web_element = jp_common.find_web_element("//*[@id='main-nav-0']/a", "Find Jobs Select box",
                                                                           "one",self.wait)
                        jp_common.web_element_action(find_jobs_web_element, "click", "", "Advanced Search Button")

                        adv_search_web_element = jp_common.find_web_element("//*[@id='sub-nav-1']/a",
                                                                           "Find Jobs Select box",
                                                                           "one", self.wait)
                        jp_common.web_element_action(adv_search_web_element, "click", "", "Advanced Search Button")

                        #find_jobs_web_element.select_by_visible_text('Advanced Search')

                        'Finding Job Title Textbox element and sending text.'
                        job_adv_title_web_element = jp_common.find_web_element("//*[@id='txtKeyword']", "Job Advanced Title Textbox",
                                                                           "one",
                                                                           self.wait)
                        jp_common.web_element_action(job_adv_title_web_element, "send_keys", job_title, "Job Advanced Title Textbox")
                        #job_adv_title_sugession_web_element = jp_common.find_web_element("//*[@id='//input[@id='txtKeyword']/following-sibling::pre[1]'",
                        #                                                       "Job Advanced Title Sugession box",
                        #                                                       "one",self.wait)
                        #jp_common.web_element_action(job_adv_title_sugession_web_element, "click", "", "Advanced Search Button")

                        time.sleep(1)
                        jp_common.web_element_action(job_adv_title_web_element, "send_keys", Keys.TAB,
                                                     "Job Advanced Title Textbox")

                        'Finding Job Location Textbox element and sending text.'
                        job_adv_location_web_element = jp_common.find_web_element("//*[@id='advLocation']",
                                                                              "Job Advanced Location Textbox",
                                                                              "one", self.wait)
                        jp_common.web_element_action(job_adv_location_web_element, "send_keys", job_location,
                                                     "Job Advanced Location Textbox")
                        time.sleep(1)
                        jp_common.web_element_action(job_adv_location_web_element, "send_keys", Keys.TAB,
                                                     "Job Advanced Location Textbox")

                        'Choose Posting Date -> Today'
                        find_jobs_web_element = Select(
                            jp_common.find_web_element("//*[@id='ctl00_ctl00_ctl00_body_body_wacCenterStage_ddlDate']", "Job Posted Select box",
                                                       "one", self.wait))
                        find_jobs_web_element.select_by_visible_text("Today")

                        'Finding Search Button element and clicking it.'
                        search_web_element = jp_common.find_web_element("//*[@id='submitButton']", "Advanced Search Button",
                                                                        "one",
                                                                        self.wait)
                        jp_common.web_element_action(search_web_element, "click", "", "Advanced Search Button")

                    except Exception as e:
                        print("Unexpected error in monster_search_jobs_past24hrs", e)
                        logging.exception("Unexpected exception in monster_search_jobs_past24hrs")
                        logging.exception(e)
                        self.driver.get_screenshot_as_file("Screenshots\monster_search_jobs_past24hrs_exception.png")

        def monster_valid_job(self, jp_common):
            try:
                logging.info("In monster_valid_jobs")
                print("In monster_valid_jobs")

                # Finding Job Title Textbox element and sending text.
                # msg = jp_common.find_web_element("/html/body/div[2]/section/div/header/h1", "Job Search Message", "one",
                #                                                   self.wait).text
                # job_search_message_web_element = jp_common.find_web_element("/html/body/div[2]/section/div/header",
                #                                                            "Job Search Message", "one",
                #                                                            self.wait)
                # print(jp_common.web_element_action(job_search_message_web_element, "get_text","", "Job Search Message"))
                # msg=job_search_message_web_element.text

                #msg = self.driver.find_element_by_xpath("//header[@class='title']/h1").text
                msg = jp_common.find_web_element("//header[@class='title']/h1", "Invalid Search Text",
                                                                        "one",
                                                                        self.wait)
                print(msg.text)
                #breakpoint()
                #msg = "New Jobs in U.S"
                logging.info(msg.text)
                # print(driver.find_element_by_xpath("/html/body/div[2]/section/div/header/h1").text)
                # if job_search_message_web_element.text == "New Jobs in the US":
                if msg.text == "Sorry, we didn't find any jobs matching your criteria":

                    return False
                else:
                    return True

            except Exception as e:
                print("Unexpected error in monster_valid_jobs", e)
                logging.error("Unexpected exception in monster_valid_jobs")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_valid_jobs_exception.png")

        # load more
        def monster_loadmore_jobs(self):
            logging.info("In monster_loadmore_jobs")
            print("In monster_loadmore_jobs")
            click = 0
            time.sleep(3)
            try:
                load_more_web_element = self.driver.find_element_by_xpath(
                    "//*[@id='loadMoreJobs'][@class='mux-btn btn-secondary load-more-btn ']")
                print(load_more_web_element, "load more found")
                # load_more_web_element=jp_common.find_web_element("//*[@id='loadMoreJobs']", "Load More Button", "one", self.wait)
                while load_more_web_element:
                    load_more_web_element.click()
                    time.sleep(3)
                    click += 1
                    load_more_web_element = self.driver.find_element_by_xpath(
                        "//*[@id='loadMoreJobs'][@class='mux-btn btn-secondary load-more-btn ']")
                    print("Load More found and clicked", click, "time(s)")

            except Exception as e:
                print("Unexpected error in monster_loadmore_jobs", e)
                logging.error("Unexpected exception in monster_loadmore_jobs" + str(e))
                self.driver.get_screenshot_as_file("Screenshots\monster_load_more_jobs_exception.png")

        # Get list of job links populated
        def monster_get_job_links(self, jp_common):
            #  job links xpath
            print("In monster_get_job_links")
            logging.info("In monster_get_job_links")
            try:
                job_links_web_element = jp_common.find_web_element(
                    "//*[@id='SearchResults']/section/div/div[2]/header/h2/a",
                    "Job Links", "multiple", self.wait)
                return job_links_web_element
            except Exception as e:
                print("Unknown Exception in monster_get_jobs_links", e)
                logging.error("Unknown Exception in monster_get_jobs_links")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_job_links_exception.png")

        # Get list of job company names
        def monster_get_job_company(self, jp_common):
            print("In monster_get_job_company")
            logging.info("In monster_get_job_company")
            try:
                job_company_web_element = jp_common.find_web_element(
                    "//*[@id='SearchResults']/section/div/div[2]/div[1]/span",
                    "Job Company Name", "multiple", self.wait)
                return job_company_web_element
            except Exception as e:
                print("Unknown Exception in monster_get_job_company", e)
                logging.error("Unknown Exception in monster_get_job_company")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_job_company.png")

        # Get names of job locations
        def monster_get_job_location(self, jp_common):
            print("In monster_get_job_location")
            logging.info("In monster_get_job_location")
            try:
                job_location_web_element = jp_common.find_web_element(
                    "//*[@id='SearchResults']/section/div/div[2]/div[2]/span",
                    "Job Location", "multiple", self.wait)
                return job_location_web_element
            except Exception as e:
                print("Unknown Exception in get_jobs_location".e)
                logging.error("Unknown Exception in get_jobs_location")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_job_location_exception.png")

        # Get Date-time of job posted
        def monster_get_job_posted_datetime(self, jp_common):
            print("In monster_get_posted_datetime")
            logging.info("In monster_get_posted_datetime")
            try:
                job_posted_datetime_web_element = jp_common.find_web_element(
                    "//*[@id='SearchResults']/section/div/div[3]/time",
                    "Job Date Posted", "multiple", self.wait)
                return job_posted_datetime_web_element
            except Exception as e:
                print("Unknown Exception in monster_get_jobs_poster_datetime")
                logging.error("Unknown Exception in monster_get_jobs_poster_datetime")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_job_posted_datetime_exception.png")

        # Get Job description and scrape Email and Phone number
        def monster_get_job_desc(self, job_date_posted, job_title, job_loc, job_links, job_company, job_location,
                                 jp_common):
            print("In monster_get_jobs_desc")
            logging.info("In monster_get_jobs_desc")
            #print(self.driver.page_source)
            if "//*[@id='JobBody']" in self.driver.page_source:
                print("yes")
            else:
                print("no")
            # breakpoint()
            try:
                self.link_count = 0
                self.job_details['Searched Job Title'] = job_title
                self.job_details['Searched Job Location'] = job_loc
                for link in job_links:
                    job_desc = []

                    logging.info("job title: " + link.text)
                    logging.info("Monster, Link clicked  :" + job_title + " " + job_loc + " " + str(
                        self.link_count + 1) + " / " + str(len(job_links)))

                    logging.info("==============================================> " + str(self.link_count + 1))
                    self.job_details['Job Link'] = link.get_attribute("href")
                    self.job_details['Job Title'] = link.text
                    self.job_details['Job Company Name'] = job_company[self.link_count].text
                    self.job_details['Job Location'] = job_location[self.link_count].text
                    self.job_details['Job Date Posted'] = job_date_posted[self.link_count].text

                    try:
                        jp_common.web_element_action(link, "click", "", "Job link")
                        # jp_common.get_url(driver,link.get_attribute("href"))
                        # job_description_web_element=jp_common.find_web_element("//*[@id='main-content']/div/div/div/div[3]",
                        #                                                       "Job Description", "multiple",self.wait)
                        job_description_web_element = jp_common.find_web_element(
                            "//*[@id='JobBody']", "Job Description", "multiple", self.wait)
                        for element in job_description_web_element:
                            job_desc.append(element.text)
                    except Exception as e:
                        print("Unknown Exception occurred while clicking to get job description", e)
                        logging.error("Unknown Excecption occurred while clicking to get job description")
                        logging.exception(e)
                    else:
                        # for element in job_description_web_element:
                        #    job_desc.append(element.text)
                        # job_desc+=element.text
                        job_desc = ' '.join(map(str, job_desc))
                        # print(job_desc)
                        self.job_details['Job Description'] = job_desc
                        self.job_details['Job Email'] = jp_common.get_Email_desc(job_desc)
                        logging.info(self.job_details['Job Email'])
                        self.job_details['Job Phone No'] = jp_common.get_Phno_desc(job_desc)
                        logging.info(self.job_details['Job Phone No'])

                        self.job_details['Date&Time'] = datetime.now().strftime("%b-%d-%Y %H:%M:%S")
                        jp_common.write_to_csv(self.job_details)
                        # jp_common.copy_to_json("Job_Details.json",self.job_details)
                        if self.link_count % 150 == 0:
                            print("sleeping++++++++++")
                            logging.info("sleeping")
                            time.sleep(random.randint(15, 20))

                    self.link_count += 1
            except Exception as e:
                print("Unknown exception in monster_get_job_desc", e)
                logging.error("Unknown exception in monster_get_job_desc")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_job_desc_exception.png")

        # To get jobs from the user given choices
        def monster_get_jobs(self, job_title,job_loc,jp_common):
            print("In monster_get_jobs")
            logging.info("In monster_get_jobs")
            try:
                jp_common.get_url(self.driver, self.url)
                #self.monster_search_jobs_past24hrs(jp_common, job_title, job_loc)
                self.monster_search_jobs(jp_common, job_title, job_loc)
                if (self.monster_valid_job(jp_common) == True):
                    self.monster_loadmore_jobs()
                    job_links = self.monster_get_job_links(jp_common)
                    job_company = self.monster_get_job_company(jp_common)
                    job_location = self.monster_get_job_location(jp_common)
                    job_date_posted = self.monster_get_job_posted_datetime(jp_common)
                    self.job_details['Job Category'] = jp_common.set_job_category(job_title)

                    logging.info("Links Populated for Monster : " + job_title + " " + job_loc+ " are : " + str(len(job_links)))

                    self.monster_get_job_desc(job_date_posted, job_title, job_loc, job_links, job_company,
                                              job_location, jp_common)
                    self.job_count.append(self.link_count)
                    jp_common.get_all_phno()
                    jp_common.get_all_email()

                    #self.monster_clear_search(job_title, job_loc)
                    #self.report(job_title,job_location, "Sorry no jobs matching your search", jp_common)

                    jp_common.time_to_execute()
            except Exception as e:
                print("Unknown exception in monster_get_jobs", e)
                logging.error("Unknown exception in monster_get_jobs")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_jobs_exception.png")

        # clear search boxes
        def monster_clear_search(self, job_title, job_loc):
            print("In monster_clear_search")
            logging.info("monster_clear_search")
            try:
                for i in range(len(job_title)):
                    self.driver.find_element_by_xpath("//*[@id='keywords2']").send_keys(Keys.BACKSPACE)

                for i in range(len(job_loc)):
                    self.driver.find_element_by_xpath("//*[@id='location']").send_keys(Keys.BACKSPACE)

            except Exception as e:
                print("Unknown exception in monster_clear_search", e)
                logging.error("Unknown exception in monster_clear_search")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_clear_search_exception.png")

        def report(self, job_title,job_location, msg, jp_common):
            try:
                logging.info("================================")
                logging.info("=======Monster Report===========")
                #for title, loc, count in zip(job_title[0], job_location[1], range(len(self.job_count))):
                if len(self.job_count) > 0:
                    logging.info(job_title + " " + job_location + ":" + str(self.job_count[0]) + " Jobs")
                else:
                    logging.info(job_title + "  " + job_location + " : " + msg)
                logging.info("Monster Execution time for :",job_title,job_location + str(jp_common.time_to_execute()))
                logging.info("================================")
            except Exception as e:
                print("Unknown exception in monster_clear_search", e)
                logging.exception("Unknown exception in monster_clear_search")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\monster_get_clear_search_exception.png")

    except Exception as e:
        print("Unknown Exception occurred in Class Monster", e)
        logging.error("Unknown Exception occurred in Class Monster")
        logging.exception(e)
        driver.get_screenshot_as_file("Screenshots\monster_class_exception.png")


# job_search=["Java Developer","Seattle"]
# job_search=["SDET","Python Developer","Java Developer","Chicago","Seattle","Atlanta"]
# job_search = ["dsds", "Seattle"]
# job_search=["SDET","Franklin-TN"]
# job_search=["SDET","SDET","DS","Franklin-TN","Oregon","Oregon"]
#job_search=["Java","Atlanta"]
#job_search=["Python SDET","Seattle"]
#job_search = ["Python Developer", "Python Developer", "Java Developer", "San Francisco", "New York", "San Francisco"]
# job_search=["Python Developer","San Francisco"]

# print(job_search)
# job_arr = np.array(job_search).reshape(2, int(len(job_search) / 2))
# jp_common = JobPortal_Common()
# driver = jp_common.driver_creation("gecko")
# monster_obj = Monster(driver, Driver_Paths.monster_url)
# monster_obj.monster_get_jobs(job_arr, jp_common)

#
# from openburrito import find_burrito_joints, BurritoCriteriaConflict
# # "criteria" is an object defining the kind of burritos you want.
# try:
#     places = find_burrito_joints(criteria)
# except BurritoCriteriaConflict as err:
#     logger.warn("Cannot resolve conflicting burrito criteria: {}".format(err.message))
#     places = list()

# https://www.datadoghq.com/blog/python-logging-best-practices/
# lowermodule.py
# import logging
#
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
# logger = logging.getLogger(__name__)
#
# #uppermodule
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
# logger = logging.getLogger(__name__)
# https://www.datadoghq.com/blog/python-logging-best-practices/
