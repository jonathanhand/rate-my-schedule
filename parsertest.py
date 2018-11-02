import urllib.request
import re
from bs4 import BeautifulSoup
import unicodedata
import sqlite3

conn=sqlite3.connect('IScourses.db')
print("Connection opened")

cur=conn.cursor()

cur.execute('DROP TABLE IF EXISTS InfoSystems') #drop existing table
#make new table
cur.execute('''CREATE TABLE InfoSystems (CNum INTEGER, Days TEXT, Time TEXT, Location TEXT, Professor TEXT);''')
#passing hardcoded values
cur.execute('''INSERT INTO InfoSystems (CNum, Days, Time, Location, Professor) \
    VALUES(4324,'MW','8-9:15AM','PSY-154', 'Thomason A')''');
cNumTest= 190
#format to pass variables
cur.execute('''Insert INTO InfoSystems VALUES (?,'TR','9-10','CBA101','James')''', [(cNumTest)]);

cur = conn.execute("SELECT * from InfoSystems")
for row in cur:
    print(row)


address = "http://web.csulb.edu/depts/enrollment/registration/class_schedule/Spring_2019/By_Subject/IzS.html"
response = urllib.request.urlopen(address)
bytes = response.read()
text = bytes.decode()

htmlText = open("csulbhtml.txt", "w")

soup = BeautifulSoup(text, 'html5lib')

print("------------------------------------------")
courseCode=soup.select("[class~=courseCode]")
courseTitle=soup.select("[class~=courseTitle]")


#rows = soup.find("[scope~=row]")

table = soup.find_all('table', 'sectionTable')
#divCourseHeader = soup.find('div', 'courseHeader').get_text()
divCourseHeader = soup.find('div', 'courseHeader')
siblingHeader = divCourseHeader.next_child
spanCode = soup.find('span', 'courseCode')
nextSpan = spanCode.find_next('span', 'courseCode')
allCourseCodeDiv = soup.find_all('div', 'courseHeader')



#tableTitle = list(soup.divCourseHeader.children)
td = soup.table('td')
#text = soup.table.find_next_sibling('td').get_text()


block = soup.td.findAll('td')


data = []
#print(courseCode[0].get_text())
#print(divCourseHeader)
#print(siblingHeader)
#print(spanCode)
#print("NEXT: ",nextSpan)

courseBlockDivs = soup.find_all('div', 'courseBlock')
classNumDict = dict()
subjectClassDict = dict()
classesList = []
counter = 0
for div in courseBlockDivs:
    courseCodeSpan = div.find('span', 'courseCode').get_text()
    sectionTable = div.find('table', 'sectionTable')
    print(courseCodeSpan)
    print("____________")
    trRows = sectionTable.find_all('tr')

    counter = 0
    for row in trRows: #FIXME ENDED HERE 10/30. classes for each column?
        tdRows = row.find_all('td')
       
        for i in tdRows:
            print(i)
            c=0
        
        #go by section number to help counter??
        counter=0
        #for td in tdRows:
            #print(counter)
            #counter+=1
    
    

    
#cur.executemany('INSERT INTO InfoSystems values (?,?,?,?,?,?,?,?,?,?,?)', (classesList[0],))
conn.commit()
        #print(row.get_text(), end="\n")
    
            
    
        
for course in table:
    courseCodeSpan = course.find('th')
    #print("NEXT SIB: ", courseCodeSpan)
    td = course('td')
    for i in td: #takes the data from the rows and puts into list
        #data.append(i.get_text(), end="\n")
        x=0

conn.close()

dOfCourses=dict()
#takes in list and then removes bad data and puts into a dictionary
while '' in data: #strip the blank spaces
    data.remove('')
while '\xa0' in data: #strip the unicode transferred spaces
    data.remove('\xa0')
    

dCourseWCode=dict()     
for course in allCourseCodeDiv:
    courseCodeSpan = course.find('span', 'courseCode').get_text()
    #print(courseCodeSpan)
for column in data:
    if column.isnumeric() and len(column)>3: #checks if it is numeric (only course number is)
        key = column
    else:
        dOfCourses.setdefault(key,[]).append(column)

#print(dOfCourses.get('10718'))
            

                


htmlText.close()
