import csv

import logging
import multiprocessing
import sys
import time
from datetime import datetime

import psycopg2
from pandas import np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import Utilities
from POM.Dice_Portal import Dice
from POM.Indeed_portal import Indeed
from POM.Job_Portal_Base import JobPortal
from POM.Monster_Portal import Monster

logging.basicConfig(filename="scrapper-" + datetime.now().strftime("%m-%d-%Y-%H-%M-%S") + ".log",
                            format='%(asctime)s %(name)s - %(levelname)s - %(funcName)s- %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

if len(sys.argv) < 2:
    print("please provide 2 arg. for eg: main.py and portal name like Dice|Indeed|monster")
    sys.exit()


def get_job_portal(portal_name: str, driver: webdriver) -> JobPortal:
    if portal_name.lower() == "dice":
        logging.info("creating dice portal")
        return Dice(driver)
    elif portal_name.lower() == "monster":
        logging.info("creating monster portal")
        return Monster(driver)
    elif portal_name.lower() == "indeed":
        logging.info("creating indeed portal")
        return Indeed(driver)
    else:
        print(" please provide portal name. for eg: dice|monster|Indeed")
        sys.exit()


def single_process_job(job_title: str):
    filename = job_title.replace(" ", "").replace("/", "").replace("\\", "")
    with open(filename + '.csv', mode='w', encoding='utf-8') as jobs:
        fieldnames = ['Job Category', 'Date&Time', 'Searched Job Title', 'Searched Job Location', 'Job Portal',
                      'Job Date Posted', 'Job Title',
                      'Job Company Name', 'Job Location', 'Job Phone No', 'Job Email', 'Job Link',
                      'Job Description']
        jobs_writer = csv.DictWriter(jobs, fieldnames=fieldnames, delimiter=',', quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)
        jobs_writer.writeheader()
        for job_location in job_locations:
            logging.info("trying to create Driver")
            driver = Utilities.get_driver()

            try:
                # concept of Polymorphism-> same like my conftest fundas(Travolook)
                job_portal = get_job_portal(portal, driver)

                job_title_input_box = job_portal.get_job_title_input_box()
                job_title_input_box.clear()
                logging.info("sending job title " + "\"" + job_title + "\"")
                while True:
                    job_title_input_box.send_keys(job_title)
                    time.sleep(1)
                    if job_title_input_box.get_attribute("value") != "":
                        break
                job_portal.set_job_location_and_search(job_location)
                job_portal.apply_job_filters()
                time.sleep(1)
                if not job_portal.is_job_found():
                    break

                logging.info("getting all jobs link in variable")

                job_list = job_portal.get_job_list()
                logging.info("looping through all the jobs")

                while True:
                    if len(job_list) == 0:
                        break

                    for job in job_list:
                        try:
                            logging.info("getting job details")
                            job_details = job_portal.get_job_details(job)
                            job_details["Searched Job Title"] = job_title
                            job_details["Searched Job Location"] = job_location
                            job_details["Job Portal"] = portal
                            jobs_writer.writerow(job_details)
                            logging.info("got job details")
                        except Exception as e:
                            logging.exception("failed to get job details for job: " + job.text)

                    job_list = job_portal.get_jobs_next_page()

                logging.info("completed scrapping jobs for job title:" + job_title + " and job location:" + job_location)
            except Exception as e:
                filename = "Screenshot\error-" + datetime.now().strftime("%m-%d-%Y-%H-%M-%S") + ".png"
                logging.exception(
                    "error occured during performing job search for job title:" + job_title + " and job location:" + job_location + " .screenshot captured at " + filename)
                driver.get_screenshot_as_file(filename)

            finally:
                driver.quit()

conn = psycopg2.connect(
    host = 'ec2-50-17-90-177.compute-1.amazonaws.com',
    database = 'dbo53q05khphsq',
    user = 'tjwamztwfeudyf',
    password = '4016af97c725336d823c79afd14e790341ff2b3b6849ea1ed1f3260b2f4fb46b'
)
cur1 = conn.cursor()
cur1.execute('SELECT "job_title" FROM herokudjangoapp_jobs WHERE "job_title" IS NOT NULL')
job_titles = cur1.fetchall()
job_titles = np.fromiter([i[0] for i in job_titles], dtype='<U50')

logging.info("Job titles")
logging.info(job_titles)

cur1.execute('SELECT "job_location" FROM herokudjangoapp_jobs')
job_locations = cur1.fetchall()
job_locations = np.fromiter([i[0] for i in job_locations], dtype='<U50')
logging.info("Job Locations")
logging.info(job_locations)
portal = sys.argv[1]


# job_title = ""
# job_location = ""
if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=2)
    pool.map(single_process_job, job_titles)

logging.info("job scrapping completed")




