#from Monster import Monster
#from Indeed import IndeedMain
#from Glassdoor import Glassdoor
import numpy as np
import sys
import Driver_Paths
from JobPortal_Common_Defs import JobPortal_Common
import logging
import psycopg2

from Dice_new2 import Dice

logging.info("Starting, Job Search....")
print("Starting, Job Search....")
logging.basicConfig(filename='scrapper.log', filemode='a',
                            format='%(asctime)s %(name)s - %(levelname)s - %(funcName)s- %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

'Creating numpy array'
#job_search=[i for i in sys.argv[1].split(',')]
#job_arr = np.array(job_search).reshape(2, int(len(job_search)/2))
#job_arr = np.job_array([i for i in sys.argv[1].split(',')]).reshape(2, int(len([i for i in sys.argv[1].split(',')])/2))
# job_search = np.genfromtxt('Search_Jobs.csv', delimiter=",", skip_header=1,dtype=None,encoding = None)
# job_title=(job_search[:,-2])
# job_location=(job_search[:,-1])
# print(job_title)
# erase_empty=np.array([''])
# job_title=np.setdiff1d(job_title,erase_empty)
# print("job_title",job_title)
# logging.info("Job titles"+str(job_title))
# print(job_location)
# job_location=np.setdiff1d(job_location,erase_empty)
# print("job_location",job_location)
# logging.info("Job Locations"+str(job_location))

conn = psycopg2.connect(
    host = 'ec2-50-17-90-177.compute-1.amazonaws.com',
    database = 'dbo53q05khphsq',
    user = 'tjwamztwfeudyf',
    password = '4016af97c725336d823c79afd14e790341ff2b3b6849ea1ed1f3260b2f4fb46b'
)
cur1 = conn.cursor()
cur1.execute("SELECT job_title FROM herokudjangoapp_jobs WHERE job_title ='Python Developers'")
#cur1.execute('SELECT "job_title" FROM herokudjangoapp_jobs WHERE "job_title" IS NOT NULL')
#cur1.execute("SELECT job_title from herokudjangoapp_jobs WHERE job_title = 'Software Quality Assurance Engineer'")
#cur1.execute("SELECT job_title from herokudjangoapp_jobs WHERE job_title = 'SDET'")
job_title = cur1.fetchall()
print (list(job_title))
print (job_title)

job_title = np.fromiter([i[0] for i in job_title], dtype='<U50')
print (job_title)
logging.info("Job titles")
logging.info(job_title)

cur1.execute('SELECT "job_location" FROM herokudjangoapp_jobs')
# cur1.execute("SELECT job_location from herokudjangoapp_jobs WHERE job_location = 'New York, NY'")
job_location = cur1.fetchall()
job_location = np.fromiter([i[0] for i in job_location], dtype='<U50')
print (job_location)
logging.info("Job Locations")
logging.info(job_location)

# for i in range((job_title.size)):
#     for j in range((job_location.size)):
#         if job_title[i] =="Java Developer" and job_location[j] =="New York":
#             continue
#         if job_title[i] =="Java Developer" and job_location[j] =="Franklin-TN":
#             continue
#         if job_title[i] =="Java Developer" and job_location[j] =="Atlanta, Georgia":
#             continue
#         else:
#             print(job_title[i], job_location[j])
# sys.exit()

'Create JobPortal_Common() object to access common functions'
jp_common=JobPortal_Common()
jp_common.time_to_execute()

'Create browser driver'

browser_list=["chrome","gecko","msedge"]
driver=jp_common.driver_creation("chrome")

for i in range((job_title.size)):
    driver = jp_common.driver_creation("chrome")
    Dice_obj = Dice(driver, Driver_Paths.dice_url)
    jp_common.get_url(driver, Dice_obj.url)
    for j in range((job_location.size)):
        print(job_title[i], job_location[j])

        'Dice Search, Create Dice object and get jobs'
        Dice_obj.dice_get_jobs(job_title[i], job_location[j], jp_common)
    jp_common.exit_browser(driver)

       
