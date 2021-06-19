from datetime import datetime
#import pyautogui as pg
#import pywhatkit as pt
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import re
import csv
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
from JobPortal_Common_Defs import JobPortal_Common
import Driver_Paths
import logging
import random
import webbrowser as web

class Glassdoor:
    job_email_list = []
    job_phoneNo_list=[]
    glassdoor_phno = []
    glassdoor_email = []
    driver = None
    #List_of_urls = []
    job_titles = []
    job_locat = []
    no_jobs = []
    job_date = []
    wait = WebDriverWait(driver, 60)
    url = ""
    jobs=0
    start_time = datetime.now()
    job_details = {'Job Category':'','Date&Time': '', 'Searched Job Title': '', 'Searched Job Location': '', 'Job Portal': 'Glassdoor',
                   'Job Date Posted': '', 'Job Title': '',
                   'Job Company Name': '', 'Job Location': '', 'Job Phone No': [], 'Job Email': '', 'Job Link': '',
                   'Job Description': ''}


    def __init__(self,driver,url):
        print(self.start_time)
        self.driver=driver
        self.url=url
        logging.basicConfig(filename='scrapper.log', filemode='a',
                            format='%(asctime)s %(name)s - %(levelname)s - %(funcName)s- %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
        print("######################################################################### \n"
              "                                                                          \n"
              "===========================Glassdoor Job Search==========================\n"
              "                                                                          \n"
              "#########################################################################")
        print(url)


    def glassdoor_get_jobs(self,job_name,job_location,jp_common):

        #for job_name, job_location in zip(arr[0], arr[1]):
        self.job_details['Searched Job Title'] = job_name
        self.job_details['Searched Job Location'] = job_location
        jp_common.get_url(self.driver, self.url)
        #self.driver = webdriver.Chrome(executable_path="C:/Users/bincy/Downloads/chromedriver_win32/chromedriver.exe")
        #self.driver.get("https://www.glassdoor.com/blog/tag/job-search/")
        #self.driver.maximize_window()
        time.sleep(3)
        self.job_details['Date&Time'] = datetime.now().strftime("%b-%m-%Y %H:%M:%S")
        self.job_details['Job Category'] = jp_common.set_job_category(job_name)
        #self.glassdoor_functions(job_name, job_location,jp_common)
        self.glassdoor_search_jobs(job_name, job_location)
        self.job_titles.append(job_name)
        self.job_locat.append(job_location)

        print("********************Glassdoor Report*********************")
        #for i in range(0,len(self.job_titles)):
            #print(self.job_titles[i],"  ",self.job_locat[i], ":", self.no_jobs[i], "jobs \n")
        jp_common.time_to_execute()
        print("************************************************************")
        #self.driver.close()

    def glassdoor_functions(self,job_name,job_location,jp_common):
        self.glassdoor_search_jobs(job_name,job_location)
        #self.glassdoor_links_days()
        #self.glassdoor_job_text(jp_common)


    def glassdoor_search_jobs(self,job_name,job_location):

        try:

            #self.driver.maximize_window()
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="TopNav"]/nav/div[2]/ul[2]/li[2]').click()
            time.sleep(2)
            title = self.driver.find_element_by_xpath('//*[@id="KeywordSearch"]')
            title.send_keys(job_name)
            location = self.driver.find_element_by_xpath('//*[@id="LocationSearch"]')
            location.clear()
            location.send_keys(job_location)
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="HeroSearchButton"]').click()
            date_posted = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="filter_fromAge"]')))

            date_posted.click()
            #self.driver.find_element_by_xpath('//*[@id="filter_fromAge"]').click()
            #time.sleep(1)
            Last_24hrs = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="PrimaryDropdown"]/ul/li[2]')))
            Last_24hrs.click()
            #self.driver.find_element_by_xpath('//*[@id="PrimaryDropdown"]/ul/li[2]').click()
            #time.sleep(1)
            print ('before link days')

            print ('after link days')
        except Exception as e:

            print("Unknown Exception occurred in Class Glassdoor", e)
            logging.error("Unknown Exception occurred in Class Glassdoor", e)
            self.driver.get_screenshot_as_file("Screenshots\Glassdoor_class_exception.png")

        self.glassdoor_links_days()


    def glassdoor_links(self, soup, page_count, count):
        print ('in glassdoor_links')

        List_of_urls = []

        for links in soup.find_all('div', {'class': 'jobHeader'}):

            for link in links.find_all('a'):
                List_of_urls.append(link.get('href'))
                self.glassdoor_jobdate(soup)
                count += 1

        try:
            print("Next page")
            web_element = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="FooterPageNav"]/div/ul/li/a/span')))
            length = len(web_element)

            print("length",length)
            if web_element[length-1].get_attribute("class") == "disabled":
                page_count = False
            else:
                web_element[length - 1].click()
        except Exception as e:
            print("e",e)
            print("No Next page")
            page_count = False


        try:
            WebDriverWait(self.driver, 0.3).until(EC.presence_of_element_located((By.ID, "prefix__icon-close-1")))
            self.driver.find_element_by_id("prefix__icon-close-1").click()
            wait = WebDriverWait(self.driver, 1)
        except:
            print("NO popup")

        self.glassdoor_job_text(jp_common)

        return page_count,List_of_urls



    def glassdoor_jobdate(self,soup):
        #jobDate = soup.find_all('div', {'class': 'd-flex align-items-end pl-std minor css-65p68w'})
        jobDate = soup.find_all('div', {'class': 'd-flex align-items-end pl-std css-mi55ob'})
        for date in jobDate:
            self.job_date.append(date.get_text())


    def glassdoor_links_days(self):
        page_count = True
        count = 0
        wait = None
        while page_count:
            #self.driver.get(self.driver.current_url)
            print (self.driver.get(self.driver.current_url))
            self.driver.execute_script("window.scrollTo(0, 5000);")
            #soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            soup = BeautifulSoup(self.driver.page_source,'html.parser')
            print ('before page_count')
            page_count = self.glassdoor_links(soup,page_count,count)
            print ('after pagecount')
        #print("date",len(self.job_date), len(self.List_of_urls))


    def glassdoor_job_text(self,jp_common):
        i = 0
        print("Inside glassdoor_job_text")
        #final_text = []
        for link in self.List_of_urls:
            new_link = "https://www.glassdoor.com" + link
            Glassdoor.job_details["Job Link"] = new_link

            Glassdoor.job_details["Job Date Posted"] = self.job_date[i]
            self.driver.get(new_link)
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            div = soup.find_all('div', {'class': 'desc css-58vpdc ecgq1xb3'})
            # for message in div:
            #     print("@@@@@@@@@@@@@@@@@@@@@@@")
            #     job_description=message.get_text()
            #     print(job_description)
            #     self.phone_email(job_description)
            #     self.glassdoor_company_name(soup)
            #     self.glassdoor_job_name(soup)
            #     self.glassdoor_job_location(soup)
            #     i += 1
            #
            #     print("*************************************************************************************************")
            #     print(Glassdoor.job_details)
            #     jp_common.write_to_csv(Glassdoor.job_details)
            #     self.jobs += 1
            #     if self.jobs % 10 == 0:
            #         time.sleep(random.randint(8, 12))
            #breakpoint()
            try:

                if (self.driver.find_element_by_xpath('//*[@id="JobDescriptionContainer"]')):
                    job_description= (self.driver.find_element_by_xpath('//*[@id="JobDescriptionContainer"]')).text
                    #print(job_description)
                    Glassdoor.job_details["Job Description"] = job_description
                    #self.phone_email(job_description)
                    Glassdoor.job_details['Job Phone No'] = self.get_Phno_desc(job_description)
                    Glassdoor.job_details['Job Email'] = self.get_Email_desc(job_description)

                    self.glassdoor_company_name(soup)
                    self.glassdoor_job_name(soup)
                    self.glassdoor_job_location(soup)
                    i+=i
                    #print(Glassdoor.job_details)
                    jp_common.write_to_csv(Glassdoor.job_details)
                    self.jobs += 1
                    if self.jobs % 50 == 0:
                        print("sleeping+++++++++++++++++++++++++++++++++++")
                        logging.info("Sleeping")
                        time.sleep(random.randint(10, 15))
                    print(i)
            except Exception as e:
                print("Unknown exception in glassdoor_job_text", e)
                logging.error("Unknown exception in glassdoor_job_text")
                logging.exception(e)
                self.driver.get_screenshot_as_file("Screenshots\glassdoor_job_text.png")
        self.no_jobs.append(i)
        #self.driver.close()


    def glassdoor_company_name(self, soup):
        div2 = soup.find_all('div', {'class': 'css-16nw49e e11nt52q1'})

        for div in div2:
             company_name = div.get_text()
             print("Company name  : ", company_name)
             Glassdoor.job_details["Job Company Name"] = company_name


    def glassdoor_job_name(self, soup):
        div2 = soup.find_all('div', {'class': 'css-17x2pwl e11nt52q5'})
        for div in div2:
            job_name = div.get_text()
            print("job_name    : ", job_name)
            Glassdoor.job_details["Job Title"] = job_name


            # getting job location
    def glassdoor_job_location(self, soup):
            # getting job location
        job_Location = ""
        try:
            job_Location = self.driver.find_element_by_xpath(
                '//*[@id="JobView"]/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div/div[3]').text
        except:
            div2 = soup.find_all('div', {'class': 'css-13et3b1 e11nt52q2'})
            for div in div2:
                job_Location = div.get_text()
        print("job_location : ", job_Location)
        Glassdoor.job_details["Job Location"] = job_Location


    def phone_email(self,job_description):
        print("Inside phone_email")

        match = re.findall(r'[\w\.-]+@[\w\.-]+', job_description)
        print("match",match)
        #ph_match = re.findall(r'[0-9]{3}-[0-9]{3}-[0-9]{4}', job_description)
        ph_match = re.findall(r'[0-9]{3}-[0-9]{3}-[0-9]{4}|[+][1]\s[0-9]{3}\s[0-9]{3}\s[0-9]{4}|'
                              r'[(][0-9]{3}[)]\s[0-9]{3}-[0-9]{4}',job_description)
        print("phone",ph_match)
        for lines1 in match:
            Glassdoor.job_details["Job Email"] = lines1
            print(lines1)

        Glassdoor.job_details["Job Phone No"] = ph_match
        #self.driver.quit()

    def get_Phno_desc(self, job_desc):
        job_phoneNo_list = []
        try:
            # Get phone and store
            phoneNo_match = re.findall(r'[0-9]{3}-[0-9]{3}-[0-9]{4}|[+][1]\s[0-9]{3}\s[0-9]{3}\s[0-9]{4}|'
                                       r'[(][0-9]{3}[)]\s[0-9]{3}-[0-9]{4}', job_desc)
            # phoneNo_match = re.findall(r'[0-9]{3}-[0-9]{3}-[0-9]{4}', job_desc)
            for phoneNo in phoneNo_match:
                if phoneNo not in self.job_phoneNo_list:
                    self.job_phoneNo_list.append(phoneNo)
                    print(phoneNo)
        except Exception as e:
            print("Exception in Class:JobPortal_Common def:get_Email_desc", e)
            logging.error("Exception in Class:JobPortal_Common def:get_Email_desc", e)
        else:
            return phoneNo_match

    def get_Email_desc(self,job_desc):


        email_list=[]
        try:
            #print(job_desc)
            email_match = re.findall(r'[\w\.-]+@[\w\.-]+', job_desc)
            for email in email_match:
                if email not in self.job_email_list:
                    #if not ("accommodation" in email or "disabilit" in email or "employeeservice" in email ):
                    if not (re.search('accommodation', email, re.IGNORECASE) or re.search('disabilit', email,
                                                                                          re.IGNORECASE) or re.search(
                            'employeeservice', email, re.IGNORECASE)):
                        email_list.append(email)
                        self.job_email_list.append(email)
                        print(email)
        except Exception as e:
            print("Exception in Class:JobPortal_Common def:get_Email_desc",e)
            logging.error("Exception in Class:JobPortal_Common def:get_Email_desc",e)
            #breakpoint()
        else:
            return email_list

"""
    def sendMessage(self):

        msg = "Hi, I am interested in this position"
        cur_time = str(datetime.now().time())
        print(cur_time)
        strip_time = datetime.strptime(cur_time,"%H:%M:%S.%f")
        h= strip_time.hour
        m = strip_time.minute
        #pt.sendwhatmsg("+14254437830",msg,h,m+2)
        contact = "+17472268916"
        web.open("https://web.whatsapp.com/send?phone="+ contact + '&text'+msg)
        time.sleep(2)
        width,height = pg.size()
        pg.click(width/2,height/2)
"""

#
# job_search = np.genfromtxt('Search_Jobs.csv', delimiter=",", skip_header=1,dtype=None,encoding = None)
# job_title=(job_search[:,-2])
# job_location=(job_search[:,-1])
# print(job_title)
# erase_empty=np.array([''])
# job_title=np.setdiff1d(job_title,erase_empty)
# print("job_title",job_title)
# print(job_location)
# job_location=np.setdiff1d(job_location,erase_empty)
# print("job_location",job_location)
#
# 'Create JobPortal_Common() object to access common functions'
# jp_common=JobPortal_Common()
# 'Create browser driver'
# browser_list=["chrome","gecko","msedge"]
# driver=jp_common.driver_creation("gecko")

'Monster Search, Create Monster object and get jobs'
# glassdoor_obj = Glassdoor(driver,Driver_Paths.glassdoor_url)
#
# for i in range((job_title.size)):
#     for j in range((job_location.size)):
#         print(job_title[i], job_location[j])
#
#         glassdoor_obj.glassdoor_get_jobs(job_title[i],job_location[j],jp_common)
#

#job_search=["SDET","SDET","SDET","DS","Chicago","Virginia","Oregon","Oregon"]
# job_search=["SDET","SDET","Franklin-TN","Oregon"]
# print(job_search)
# job_arr = np.array(job_search).reshape(2, int(len(job_search)/2))
# for job_name, job_location in zip(job_arr[0], job_arr[1]):
#     jp_common=JobPortal_Common()
#     driver=jp_common.driver_creation("chrome")
#     glassdoor_obj= Glassdoor(driver,Driver_Paths.glassdoor_url)
#     glassdoor_obj.glassdoor_get_jobs(job_name,job_location,jp_common)

