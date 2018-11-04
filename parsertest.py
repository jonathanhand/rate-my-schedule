import urllib.request
import re
from bs4 import BeautifulSoup
import unicodedata
import sqlite3

#DB stuff
#def BS():
conn=sqlite3.connect('IScourses.db')
print("Connection opened")

cur=conn.cursor()

cur.execute('DROP TABLE IF EXISTS InfoSystems') #drop existing table
#make new table
cur.execute('''CREATE TABLE InfoSystems (courseCode TEXT,CNum INTEGER, noCost TEXT, reserve TEXT, notes TEXT, \
type TEXT, Days TEXT, Time TEXT, openSeats TEXT, Location TEXT, Professor TEXT, comment TEXT);''')

#beautiful soup stuff
address = "http://web.csulb.edu/depts/enrollment/registration/class_schedule/Spring_2019/By_Subject/IzS.html"
response = urllib.request.urlopen(address)
bytes = response.read()
text = bytes.decode()

htmlText = open("csulbhtml.txt", "w")

soup = BeautifulSoup(text, 'html5lib')

courseCode=soup.select("[class~=courseCode]")
courseTitle=soup.select("[class~=courseTitle]")


table = soup.find_all('table', 'sectionTable')
divCourseHeader = soup.find('div', 'courseHeader')
siblingHeader = divCourseHeader.next_child
spanCode = soup.find('span', 'courseCode')
nextSpan = spanCode.find_next('span', 'courseCode')
allCourseCodeDiv = soup.find_all('div', 'courseHeader')


courseBlockDivs = soup.find_all('div', 'courseBlock') #gets courseblock divs
classesList = []
counter=0


for div in courseBlockDivs: #loops all courseblocks
    
    courseCodeSpan = div.find('span', 'courseCode').get_text()
    sectionTable = div.find('table', 'sectionTable')
    trRows = sectionTable.find_all('tr')
    counter=0
    for row in trRows: #for each table
        counter+=1
        if counter > 1:
            classesList.append(courseCodeSpan)
        tdRows = row.find_all('td') #find all td in table
        for i in tdRows: #loops through each indiviudal td
            classesList.append(i.get_text()) #adds text in each td to a list


            
#runs through class list and changes all empty values to null
for n, i in enumerate(classesList):
    if i == '':
        classesList[n] = None
    elif i == '\xa0':
        classesList[n] = None
        
#loops to add each course into a DB
i=0
while i <len(classesList):
    cur.execute('INSERT INTO InfoSystems VALUES(?,?,?,?,?,?,?,?,?,?,?, ?)' , [classesList[i],
                                                                            classesList[i+1],
                                                                            classesList[i+2],
                                                                            classesList[i+3],
                                                                            classesList[i+4],
                                                                            classesList[i+5],
                                                                            classesList[i+6],
                                                                            classesList[i+7],
                                                                            classesList[i+8],
                                                                            classesList[i+9],
                                                                            classesList[i+10],
                                                                           classesList[i+11]]);
    i+=12

conn.commit()
cur = conn.execute("SELECT CNum, professor from InfoSystems where courseCode='I S 300'")
for row in cur:
    print(row)

conn.close()
htmlText.close()
