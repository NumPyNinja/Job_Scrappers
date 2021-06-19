from Monster_New import Monster
#from Indeed_24 import IndeedMain
#from Glassdoor import Glassdoor
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

#new connection
conn = psycopg2.connect(
    host = 'ec2-3-213-106-122.compute-1.amazonaws.com',
    database = 'd18r3c2bcl7ejd',
    user = 'mzpveolwadlwqy',
    password = '358a874bb273e4ed6b6ef4d2af95f96c459b6842cb49e289f079c17d98ff6e7e'
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
browser_list=["chrome","gecko","msedge"]


#job_title.tolist()
#job_location.tolist()
#print("===================")
#job_title = ['Java Developer','Python Developer', 'Data Science', 'SDET', 'Software Quality Assurance Engineer']
#print(job_title)
#print(job_location)


'Create remaining_list'
#remaining_list=[]
#for i in range(len(job_title)):
#        for j in range(len(job_location)):
#            remaining_list.append((job_title[i],job_location[j]))

'Create numpy remaining_list'
remaining_list = np.array(np.meshgrid(job_title, job_location)).T.reshape(-1, 2)            
print(remaining_list)

'Print remaining list'            
#print([search for search in remaining_list])
#total = len(remaining_list)
#print("Len of remaining_list", total)

'finished list is empty'
#finished_list=[]

'numpy finished_list is empty'
finished_list = np.empty((0,2))

#short version
#remaining_list =np.array([ ('Python Developer', 'Austin,TX'),('Python Developer' ,'Atlanta, GA'),('Python Developer', 'Baltimore, MD'),('Python Developer' ,'Boston, MA'),('Python Developer' ,'Boulder, CO'),('Python Developer' ,'Charlotte, NC'),('Python Developer' ,'Colorado Springs, CO'),('Python Developer' ,'Columbus, OH'),('Python Developer', 'Dallas, TX'),('Python Developer', 'Denver, CO'),('Python Developer' ,'Durham-Chapel Hill, NC'),('Python Developer', 'Huntsville, AL'),('Python Developer' ,'Jacksonville, FL'),('Python Developer' ,'Nashville, TN'),('Python Developer', 'New York, NY') ,('Python Developer' ,'Raleigh, NC'),('Python Developer' ,'San Diego, CA'), ('Python Developer' ,'San Francisco, CA'),('Python Developer' ,'San Jose, CA'),('Python Developer' ,'Seattle, WA'),('Python Developer' ,'Tampa, FL') ,('Python Developer', 'Washington, DC') ,('Data Science', 'Austin,TX'), ('Data Science', 'Atlanta, GA'), ('Data Science', 'Baltimore, MD'), ('Data Science', 'Boston, MA'), ('Data Science', 'Boulder, CO'), ('Data Science', 'Charlotte, NC'), ('Data Science', 'Colorado Springs, CO'), ('Data Science', 'Columbus, OH'), ('Data Science', 'Dallas, TX'), ('Data Science', 'Denver, CO'), ('Data Science', 'Durham-Chapel Hill, NC'), ('Data Science', 'Huntsville, AL'), ('Data Science', 'Jacksonville, FL'), ('Data Science', 'Nashville, TN'), ('Data Science', 'New York, NY'), ('Data Science', 'Raleigh, NC'), ('Data Science', 'San Diego, CA'), ('Data Science', 'San Francisco, CA'), ('Data Science', 'San Jose, CA'), ('Data Science', 'Seattle, WA'), ('Data Science', 'Tampa, FL'), ('Data Science', 'Washington, DC'), ('SDET', 'Austin,TX'), ('SDET', 'Atlanta, GA'), ('SDET', 'Baltimore, MD'), ('SDET', 'Boston, MA'), ('SDET', 'Boulder, CO'), ('SDET', 'Charlotte, NC'), ('SDET', 'Colorado Springs, CO'), ('SDET', 'Columbus, OH'), ('SDET', 'Dallas, TX'), ('SDET', 'Denver, CO'), ('SDET', 'Durham-Chapel Hill, NC'), ('SDET', 'Huntsville, AL'), ('SDET', 'Jacksonville, FL'), ('SDET', 'Nashville, TN'), ('SDET', 'New York, NY'), ('SDET', 'Raleigh, NC'), ('SDET', 'San Diego, CA'), ('SDET', 'San Francisco, CA'), ('SDET', 'San Jose, CA'), ('SDET', 'Seattle, WA'), ('SDET', 'Tampa, FL'), ('SDET', 'Washington, DC'), ('Software Quality Assurance Engineer', 'Austin,TX'), ('Software Quality Assurance Engineer', 'Atlanta, GA'), ('Software Quality Assurance Engineer', 'Baltimore, MD'), ('Software Quality Assurance Engineer', 'Boston, MA'), ('Software Quality Assurance Engineer', 'Boulder, CO'), ('Software Quality Assurance Engineer', 'Charlotte, NC'), ('Software Quality Assurance Engineer', 'Colorado Springs, CO'), ('Software Quality Assurance Engineer', 'Columbus, OH'), ('Software Quality Assurance Engineer', 'Dallas, TX'), ('Software Quality Assurance Engineer', 'Denver, CO'), ('Software Quality Assurance Engineer', 'Durham-Chapel Hill, NC'), ('Software Quality Assurance Engineer', 'Huntsville, AL'), ('Software Quality Assurance Engineer', 'Jacksonville, FL'), ('Software Quality Assurance Engineer', 'Nashville, TN'), ('Software Quality Assurance Engineer', 'New York, NY'), ('Software Quality Assurance Engineer', 'Raleigh, NC'), ('Software Quality Assurance Engineer', 'San Diego, CA'), ('Software Quality Assurance Engineer', 'San Francisco, CA'), ('Software Quality Assurance Engineer', 'San Jose, CA'), ('Software Quality Assurance Engineer', 'Seattle, WA'), ('Software Quality Assurance Engineer', 'Tampa, FL'), ('Software Quality Assurance Engineer', 'Washington, DC'),('Java Developer' 'Austin,TX'), ('Java Developer' 'Atlanta, GA'), ('Java Developer', 'Baltimore, MD'),('Java Developer', 'Boston, MA'),('Java Developer', 'Boulder, CO'),('Java Developer' ,'Charlotte, NC'),('Java Developer', 'Colorado Springs, CO'),('Java Developer' ,'Columbus, OH'),('Java Developer' ,'Dallas, TX'),('Java Developer' ,'Denver, CO'),('Java Developer' ,'Durham-Chapel Hill, NC'),('Java Developer', 'Huntsville, AL'),('Java Developer' ,'Jacksonville, FL'),('Java Developer' ,'Nashville, TN'),('Java Developer' ,'New York, NY'),('Java Developer' ,'Raleigh, NC'),('Java Developer' ,'San Diego, CA'),('Java Developer' ,'San Francisco, CA'),('Java Developer' ,'San Jose, CA'),('Java Developer' ,'Seattle, WA'),('Java Developer' ,'Tampa, FL'),('Java Developer' ,'Washington, DC')])
#remaining_list =np.array([('Python Developer', 'Huntsville, AL'),('Python Developer' ,'Jacksonville, FL'),('Python Developer' ,'Nashville, TN'),('Python Developer', 'New York, NY') ,('Python Developer' ,'Raleigh, NC'),('Python Developer' ,'San Diego, CA'), ('Python Developer' ,'San Francisco, CA'),('Python Developer' ,'San Jose, CA'),('Python Developer' ,'Seattle, WA'),('Python Developer' ,'Tampa, FL') ,('Python Developer', 'Washington, DC') ])
#remaining_list =np.array([('Data Science', 'San Diego, CA'), ('Data Science', 'San Francisco, CA'), ('Data Science', 'San Jose, CA'), ('Data Science', 'Seattle, WA'), ('Data Science', 'Tampa, FL'), ('Data Science', 'Washington, DC'), ('SDET', 'Austin,TX'), ('SDET', 'Atlanta, GA'), ('SDET', 'Baltimore, MD'), ('SDET', 'Boston, MA'), ('SDET', 'Boulder, CO'), ('SDET', 'Charlotte, NC'), ('SDET', 'Colorado Springs, CO'), ('SDET', 'Columbus, OH'), ('SDET', 'Dallas, TX'), ('SDET', 'Denver, CO'), ('SDET', 'Durham-Chapel Hill, NC'), ('SDET', 'Huntsville, AL'), ('SDET', 'Jacksonville, FL'), ('SDET', 'Nashville, TN'), ('SDET', 'New York, NY'), ('SDET', 'Raleigh, NC'), ('SDET', 'San Diego, CA'), ('SDET', 'San Francisco, CA'), ('SDET', 'San Jose, CA'), ('SDET', 'Seattle, WA'), ('SDET', 'Tampa, FL'), ('SDET', 'Washington, DC'), ('Software Quality Assurance Engineer', 'Austin,TX'), ('Software Quality Assurance Engineer', 'Atlanta, GA'), ('Software Quality Assurance Engineer', 'Baltimore, MD'), ('Software Quality Assurance Engineer', 'Boston, MA'), ('Software Quality Assurance Engineer', 'Boulder, CO'), ('Software Quality Assurance Engineer', 'Charlotte, NC'), ('Software Quality Assurance Engineer', 'Colorado Springs, CO'), ('Software Quality Assurance Engineer', 'Columbus, OH'), ('Software Quality Assurance Engineer', 'Dallas, TX'), ('Software Quality Assurance Engineer', 'Denver, CO'), ('Software Quality Assurance Engineer', 'Durham-Chapel Hill, NC'), ('Software Quality Assurance Engineer', 'Huntsville, AL'), ('Software Quality Assurance Engineer', 'Jacksonville, FL'), ('Software Quality Assurance Engineer', 'Nashville, TN'), ('Software Quality Assurance Engineer', 'New York, NY'), ('Software Quality Assurance Engineer', 'Raleigh, NC'), ('Software Quality Assurance Engineer', 'San Diego, CA'), ('Software Quality Assurance Engineer', 'San Francisco, CA'), ('Software Quality Assurance Engineer', 'San Jose, CA'), ('Software Quality Assurance Engineer', 'Seattle, WA'), ('Software Quality Assurance Engineer', 'Tampa, FL'), ('Software Quality Assurance Engineer', 'Washington, DC')])
total = len(remaining_list)
print("Len of remaining_list", total)
print("remaining List: " ,remaining_list)

def run_monster(remaining_list):
    'numpy finished_list is empty'
    finished_list = np.empty((0,2))    

    for search in remaining_list:
            
            search = np.array(search).reshape(1, 2)
            
            print("*******************************************")
            print("Job search for : ", search[0][0],search[0][1])
            print("*******************************************")

            try:
                'Create JobPortal_Common() object to access common functions'
                jp_common=JobPortal_Common()
                jp_common.time_to_execute()

                'Monster Search, Create Monster object and get jobs'
                driver_gecko = jp_common.driver_creation("gecko")
                monster_obj = Monster(driver_gecko,Driver_Paths.monster_url)
                monster_obj.monster_get_jobs(search[0][0],search[0][1],jp_common)
                jp_common.exit_browser(driver_gecko)

                #finished_list.append(search)
                finished_list = np.append(finished_list,search, axis=0)
                
                print("==========================================================")
                print("Finished List: ", len(finished_list), "\n" , finished_list)
                print("==========================================================")

                'Deleting objs'
                del driver_gecko
                del jp_common
                del monster_obj
                time.sleep(5)
                
                
            except Exception as e:
                print("Unknown Exception in run_monster ", e)
                logging.exception("Unknown Exception in run_monster ")
                logging.exception(e)

                'Deleting objs'
                #driver_gecko.quit()
                del driver_gecko
                del jp_common
                del monster_obj
                time.sleep(1)
                
                print("Restarting with remaining job titles and locations")

                if len(finished_list) < total:
                    
                    'Subtract finished_list from remaining_list to get current remaining_list'
                    #remaining_list = list(set(remaining_list) - set(finished_list))
                    #remaining_list = [item for item in filter(lambda x: x not in finished_list, remaining_list)]

                    remaining_list_rows = remaining_list.view([('', remaining_list.dtype)] * remaining_list.shape[1])
                    finished_list_rows = finished_list.view([('', finished_list.dtype)] * finished_list.shape[1])
                    remaining_list =np.setdiff1d(remaining_list_rows, finished_list_rows).view(remaining_list.dtype).reshape(-1, remaining_list.shape[1])

                   
                    print("==========================================================")
                    print("Finished List: ", len(finished_list), "\n" , finished_list)
                    print("==========================================================")
                    print("\n==========================================================")
                    print(" Remaining List: ", len(remaining_list), "\n" , remaining_list)
                    print("==========================================================")
                
                    'Restart run() with remaining_list'
                    print("Sleeping 5 mins before re-starting")
                    time.sleep(300)
                    run_monster(remaining_list)
                else:
                    print("Script execution completed successfully")

            print("Script execution completed successfully!")        
                
        

'Start run'
run_monster(remaining_list)

'Quit Browser'
#jp_common.exit_browser(driver_gecko)
#logging.info(str(jp_common.time_to_execute()))

'Send Log file to developer'
#jp_common.send_email("Email_List.json")
#jp_common.send_mail()
print("Job Search Ended Successfully.")
