from Dice import Dice
# from Indeed_24 import IndeedMain
# from Glassdoor import Glassdoor
import numpy as np
import sys
import time
import Driver_Paths
from JobPortal_Common_Defs import JobPortal_Common
import logging
import psycopg2
import boto3
import time

logging.info("Starting, Job Search....")
print("Starting, Job Search....")
logging.basicConfig(filename='scrapper.log', filemode='a',
                    format='%(asctime)s %(name)s - %(levelname)s - %(funcName)s- %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

# new connection
conn = psycopg2.connect(
    host='ec2-3-213-106-122.compute-1.amazonaws.com',
    database='d18r3c2bcl7ejd',
    user='mzpveolwadlwqy',
    password='358a874bb273e4ed6b6ef4d2af95f96c459b6842cb49e289f079c17d98ff6e7e'
)

cur1 = conn.cursor()

cur1.execute('SELECT "job_title" FROM resumeapp_jobs WHERE "job_title" IS NOT NULL')
job_title = cur1.fetchall()
job_title = np.fromiter([i[0] for i in job_title], dtype='<U50')
logging.info("Job titles")
logging.info(job_title)

cur1.execute('SELECT "job_location" FROM resumeapp_jobs')
job_location = cur1.fetchall()
job_location = np.fromiter([i[0] for i in job_location], dtype='<U50')
logging.info("Job Locations")
logging.info(job_location)

'Browser List'
browser_list = ["chrome", "gecko", "msedge"]

job_title.tolist()
job_location.tolist()
print("===================")
print(job_title)
print(job_location)

'Create remaining_list'
remaining_list = []
for i in range(len(job_title)):
    for j in range(len(job_location)):
        remaining_list.append((job_title[i], job_location[j]))

'Print remaining list'
print([search for search in remaining_list])

total = len(remaining_list)
print("Len of remaining_list", total)

'finished list is empty'
finished_list = []


def run_dice(remaining_list):
    for search in remaining_list:

        print("*******************************************")
        print("Job search for : ", search[0], search[1])
        print("*******************************************")

        try:
            'Create JobPortal_Common() object to access common functions'
            jp_common = JobPortal_Common()
            jp_common.time_to_execute()

            'Dice Search, Create Dice object and get jobs'
            driver_chrome = jp_common.driver_creation("chrome")
            dice_obj = Dice(driver_chrome, Driver_Paths.dice_url)
            dice_obj.dice_get_jobs(search[0], search[1], jp_common)
            jp_common.exit_browser(driver_chrome)

            'Deleting objs'
            del driver_chrome
            del jp_common
            del dice_obj
            time.sleep(1)

            finished_list.append(search)
            print("==========================================================")
            print("Finished List: ", len(finished_list), "\n", finished_list)
            print("==========================================================")
            time.sleep(3)


        except Exception as e:
            print("Unknown Exception in run_dice ", e)
            logging.exception("Unknown Exception in run_dice ")
            logging.exception(e)

            'Deleting objs'
            del driver_chrome
            del jp_common
            del dice_obj
            time.sleep(1)

            print("Restarting with remaining job titles and locations")

            if len(finished_list) < total:
                'Subtract finished_list from remaining_list to get current remaining_list'
                # remaining_list = list(set(remaining_list) - set(finished_list))
                remaining_list = [item for item in filter(lambda x: x not in finished_list, remaining_list)]

                print("==========================================================")
                print("Finished List: ", len(finished_list), "\n", finished_list)
                print("==========================================================")
                print("\n==========================================================")
                print(" Remaining List: ", len(remaining_list), "\n", remaining_list)
                print("==========================================================")

                'Restart run() with remaining_list'
                print("Sleeping 5 mins before re-starting")
                time.sleep(300)
                run_dice(remaining_list)


'Start run'
run_dice(remaining_list)

'Quit Browser'
# jp_common.exit_browser(driver_gecko)
# logging.info(str(jp_common.time_to_execute()))

'Send Log file to developer'
# jp_common.send_email("Email_List.json")
# jp_common.send_mail()
print("Job Search Ended Successfully.")
