#browser exposes an executable file
#Through Selenium test we will invoke the executable file which will then #invoke #actual browser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By


def CombineSections(SecL,SizeL,i):
    CombinedSectionList = []
    k = (i-1)/9+1
    while(i>0):
        datatype = i%9
        #puts all data in the correct column of the spreadsheet
        if ((datatype==0 or datatype>3) and len(SecL)>0):
            CourseData[datatype+3].append(SecL.pop(0))
        if (datatype<=3 and datatype>0 and len(SizeL)>0):
            CourseData[datatype+3].append(SizeL.pop(0))
        i = i - 1
    return CombinedSectionList

IDs = []
Titles = []
Credits = []
Sec = []
Days = []
Time = []
Building = []
Instructor = []
FinalExam = []
Seats = []
Enroll = []
Wait = []

CourseData = [IDs,Titles,Credits,Sec,Wait,Enroll,Seats,FinalExam,Instructor,Building,Time,Days]

notList = [	'','Sec','Details','Days','      Time','Building / Room','Instructor','Final Exam','Seats','Enroll','Waits']
COURSE_FULL_LIST = []
j = 0
driver = webdriver.Chrome()
# to maximize the browser window
driver.maximize_window()
#get method to launch the URL
driver.get("https://acadinfo.wustl.edu/CourseListings/Semester/Listing.aspx")
#to refresh the browser
# identifying the link with the help of link text locator
DepartmentTable = driver.find_element(By.XPATH,'//*[@id="Body_dlDepartments"]')
rows = DepartmentTable.find_elements(By.XPATH, '//*[@id="Body_dlDepartments"]/tbody/tr')
#Get list of all rows of departments That are clickable
DepSizeRow = len(rows)
idlist = []
for row in rows:
    # Get the columns       
    cols = row.find_elements(By.TAG_NAME, "a")
    for col in cols:
        idlist.append(col.get_attribute("id"))
        #idlist has every webElement id that is a department link

for idDep in idlist:
    try:
        DepProp = driver.find_element(By.ID,idDep) 
        WebDriverWait(driver, 20).until(EC.visibility_of(DepProp))
        #First check to make sure the department is visible on the webpage
        DepProp.click()
        #Click the link
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "CrsOpen")))
        #Wait until courses in department are visible on webpage
        Courses = driver.find_elements(By.XPATH, "//*[contains(@class, 'CrsOpen')]")
        #create list of all course webElements
        for course in Courses:
            CourseList = []
            AllSectionsList = []
            AllSizesList = []
            #organizes types of data into lists
            CourseIDs = course.find_elements(By.TAG_NAME,'a')
            EachSectionS = course.find_elements(By.XPATH, "//*[contains(@class, 'ResultRow2 TypeS')]")
            for courseID in CourseIDs:
                #gets all courses titles, IDs, Credits
                if courseID.text not in notList:
                    CourseList.append(courseID.get_attribute('textContent'))
                    print(courseID.get_attribute('textContent'))
            SubSections = course.find_elements(By.CLASS_NAME, "ItemRow")
            #gets some subsection elements
            ClassSizes = course.find_elements(By.CLASS_NAME, "ItemRowCenter")
            #gets all class size related elements
            for SubSection in SubSections:
                AllSectionsList.append(SubSection.get_attribute('textContent'))
                print(SubSection.get_attribute('textContent'))
            for ClassSize in ClassSizes:
                AllSizesList.append(ClassSize.get_attribute('textContent'))
                print(ClassSize.get_attribute('textContent'))
            k = len(AllSectionsList)+len(AllSizesList)
            CombinedList = CombineSections(AllSectionsList,AllSizesList,k)
            #Combines SubSections and ClassSizes in one list
            l = int((k-1)/9)+1
            for i in range(l):
                CourseData[0].append(CourseList[0])
                CourseData[1].append(CourseList[1])
                CourseData[2].append(CourseList[2])
    except TimeoutException:
        print("No Course Listings for department")
    driver.refresh()
    time.sleep(5)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME,'ControlLink')))
    j +=1 
    print(j)
endList = [IDs,Titles,Credits, Sec,Days,Time,Building,Instructor,FinalExam,Seats,Enroll,Wait]
#reorders data in order on WebSTAC
df = pd.DataFrame(endList).transpose()
#create dataframe with transposed list
df.columns = ['Course ID','Course Title', 'Course Credits', 'Section', 'Day', 'Time', 'Building', 'Instructor', 'Final Exam', 'Seats', 'Enroll', 'WaitList']
#labels columns
df.to_excel('webstac4.xlsx')
#export to excel spreadsheet
driver.close