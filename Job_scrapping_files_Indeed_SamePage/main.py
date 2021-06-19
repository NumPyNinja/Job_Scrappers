# from Monster_New import Monster
from Indeed_24 import IndeedMain
from Glassdoor import Glassdoor
import numpy as np
import sys
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

conn = psycopg2.connect(
    host='ec2-50-17-90-177.compute-1.amazonaws.com',
    database='dbo53q05khphsq',
    user='tjwamztwfeudyf',
    password='4016af97c725336d823c79afd14e790341ff2b3b6849ea1ed1f3260b2f4fb46b'
)
cur1 = conn.cursor()
cur1.execute('SELECT "job_title" FROM herokudjangoapp_jobs WHERE "job_title" IS NOT NULL')
job_title = cur1.fetchall()
print(list(job_title))
print(job_title)

job_title = np.fromiter([i[0] for i in job_title], dtype='<U50')
print(job_title)
logging.info("Job titles")
logging.info(job_title)

cur1.execute('SELECT "job_location" FROM herokudjangoapp_jobs')
job_location = cur1.fetchall()
job_location = np.fromiter([i[0] for i in job_location], dtype='<U50')
print(job_location)
logging.info("Job Locations")
logging.info(job_location)

'Create JobPortal_Common() object to access common functions'
jp_common = JobPortal_Common()
jp_common.time_to_execute()

'Create browser driver'

browser_list = ["chrome", "gecko", "msedge"]
driver = jp_common.driver_creation("gecko")

list1 = ['Java Developers']
list2 = ["Columbus, Ohio",
         "Durham-Chapel Hill, North Carolina", "Boulder, Colorado", "Boston, MA",
         "Colorado Springs, Colorado", "San Diego, California",
         "Jacksonville, Florida", "Tampa, Florida", "Baltimore, Maryland",
         "San Francisco, California"]

for i in range(job_title.size):
    for j in range(job_location.size):
        print(job_title[i], job_location[j])

        # 'Indeed Search,Create Indeed object and get jobs'
        indeed_obj = IndeedMain(driver, Driver_Paths.indeed_url)
        indeed_obj.indeed_iterating_job_location(job_title[i], job_location[j], jp_common)

'Upload CSV to S3 Bucket'
AWS_ACCESS_KEY_ID = 'AKIA3MXFWFP7UTGONDPF'
AWS_SECRET_ACCESS_KEY = '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'

s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

for bucket in s3.buckets.all():
    print(bucket.name)
try:
    timestr = time.strftime("%Y%m%d")
    print(timestr)
    filename = "IndeedJobs" + timestr + ".csv"
    s3.meta.client.upload_file('C:\\Users\\Administrator\\Job_scrapping_files_Indeed\\Jobs_Scrapped_new.csv',
                               'numpyninja-jobscrapper', filename)
    print("Uploaded the fileto s3 Bucket")
    logging.info("File uploaded to S3 Bucket")
except Exception as e:
    print("Error in  uploading the file to s3 Bucket", e)
    logging.info("Error in uploading the file", e)

'Quit Browser'
jp_common.exit_browser(driver)
logging.info(str(jp_common.time_to_execute()))

'Send Log file to developer'
jp_common.send_email()
print("Job Search Ended.")
