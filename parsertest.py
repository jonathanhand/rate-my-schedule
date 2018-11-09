import urllib.request
from bs4 import BeautifulSoup
import sqlite3

def main():
    csulbCourseCodes = getCodeNames()
    conn=sqlite3.connect('csulbCourses.db')
    cur=conn.cursor()
    tableName = 'springSchedule'
    cur.execute('DROP TABLE IF EXISTS ' + tableName) #drop existing table
    #make new table
    cur.execute('CREATE TABLE ' + tableName + ' (courseCode TEXT, courseTitle TEXT, CNum INTEGER, noCost TEXT, reserve TEXT, notes TEXT, \
    type TEXT, Days TEXT, Time TEXT, openSeats TEXT, Location TEXT, Professor TEXT, comment TEXT, department TEXT);')

    for code in csulbCourseCodes:
        class_list = bsParser(code)
        courseDB(code, class_list, tableName)

def getCodeNames():
    #----------------------gets all code names from index page-----------------------------
    address = "http://web.csulb.edu/depts/enrollment/registration/class_schedule/Spring_2019/By_Subject/index.html"
    response = urllib.request.urlopen(address)
    bytes = response.read()
    text = bytes.decode()

    soup = BeautifulSoup(text, 'html.parser')

    
    courseLinkDiv = soup.find_all('div', 'indexList') #gets courseblock divs
    courseCodeCSV=[]
    for div in courseLinkDiv: #loops all courseblocks
        
        codeLink = div.find_all('a', href=True)
        for link in codeLink:
                string = link['href']
                if string != '#':
                        stripped = string.strip('.html')
                        courseCodeCSV.append(stripped)
    return courseCodeCSV

def bsParser(eA):
    #----------------------beautiful soup stuff-----------------------------
    endAddress = eA
    baseAddress = "http://web.csulb.edu/depts/enrollment/registration/class_schedule/Spring_2019/By_Subject/"
    address = baseAddress + endAddress + ".html"
    response = urllib.request.urlopen(address)
    bytes = response.read()
    text = bytes.decode()

    soup = BeautifulSoup(text, 'html.parser')
    

    courseBlockDivs = soup.find_all('div', 'courseBlock') #gets courseblock divs
    classesList = []
    counter=0

    for div in courseBlockDivs: #loops all courseblocks
        
        courseCodeSpan = div.find('span', 'courseCode').get_text()
        courseTitleSpan = div.find('span', 'courseTitle').get_text()
        sectionTable = div.find('table', 'sectionTable')
        trRows = sectionTable.find_all('tr')
        counter=0
        for row in trRows: #for each table
            counter+=1
            if counter > 1:
                classesList.append(courseCodeSpan)
                classesList.append(courseTitleSpan)
            tdRows = row.find_all('td') #find all td in table
            for i in tdRows: #loops through each indiviudal td
                classesList.append(i.get_text()) #adds text in each td to a list


                
    #runs through class list and changes all empty values to null
    for n, i in enumerate(classesList):
        if i == '':
            classesList[n] = None
        elif i == '\xa0':
            classesList[n] = None
            
    return classesList


#-------------------------DB stuff-----------------------------------------
def courseDB (dN, c_l, tN):
    department = dN
    tableName = tN
    classesList = c_l
    conn=sqlite3.connect('csulbCourses.db')
    print("Connection opened")


        

    cur=conn.cursor()
    
    #loops to add each course into a DB
    i=0
    while i <len(classesList):
        cur.execute('INSERT INTO ' + tableName + ' VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)' , [classesList[i],
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
                                                                                classesList[i+11],
                                                                                classesList[i+12],
                                                                                department]);
        i+=13

    conn.commit()
    cur = conn.execute("SELECT * from " + tableName + "")
    #for row in cur:
        #print(row)
    #took this print statement out because already tested and takes forever to print every class at CSULB

    conn.close()
    print("connection closed")
    
main()
