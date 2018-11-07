
# importing the requests library 
import requests
import sqlite3



def main():
    rowsNum = 4640
    ratingList = requestRatings(rowsNum)
    ratingsDB(ratingList, rowsNum)


def ratingsDB (r_l, r_n):
    ratingList = r_l
    rowsNum = r_n
    conn=sqlite3.connect('csulbCourses.db')
    print("Connection opened")
    tableName = 'Professor_Ratings'

    cur=conn.cursor()
    cur.execute('DROP TABLE IF EXISTS ' + tableName) #drop existing table
    #make new table
    cur.execute('CREATE TABLE ' + tableName + ' (lastName TEXT,profNum INTEGER, schoolCode INTEGER, totRating FLOAT, \
    numRatings INTEGER, firstName TEXT, lastWithInitial);')

    #loops to add each course into a DB
    i=0
    while (i < rowsNum*6):
        cur.execute('INSERT INTO ' + tableName + ' VALUES(?,?,?,?,?,?,?)' , [ratingList[i],
                                                                                ratingList[i+1],
                                                                                ratingList[i+2],
                                                                                ratingList[i+3],
                                                                                ratingList[i+4],
                                                                                ratingList[i+5],
                                                                                ratingList[i+6]]);
        i+=7
    print(i)
    print(rowsNum)

    conn.commit()
    cur = conn.execute("SELECT * from " + tableName + "")
    #for row in cur:
        #print(row)
    #took this print statement out because already tested and takes forever to print every class at CSULB

    conn.close()
    print("connection closed")


def requestRatings(rowInt):
    # api-endpoint 
    URL = "http://search.mtvnservices.com/typeahead/suggest/"
    para = "?solrformat=true&"
    rowsURL = "rows="
    rowsStr = str(rowInt)
    callback="&callback=noCB&"
    q="q=*%3A*+AND+schoolid_s%3A162&"
    defType="defType=edismax"
    qf="&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&"
    bf = "bf=pow(total_number_of_ratings_i%2C2.1)&"
    sort="sort=total_number_of_ratings_i+desc&"
    siteName = "siteName=rmp&"
    rows2="rows=1&start=0&"
    fl="fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&"
    fq="fq="
      
      
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'start':20} 
      
    # sending get request and saving the response as response object 
    r = requests.get(url = URL+para+rowsURL+rowsStr+callback+q+defType+qf+bf+sort+siteName+rows2+fl+fq)

    returnText = r.text
    listTest = []



    i=0
    ratingList = []
    #Splits the data, so it can be put into list to pass to db
    for line in r.text.splitlines():
        if '{' in line:
            test=0
            #print("INCREMENT")
        #elif 'status' in line:
            #print("IGNORE")
       # elif 'QTime' in line:
            #print("IGNORE")
        #elif '}' in line:
            #print("IGNORE")
        #elif ');' in line:
            
        if 'teacherlast' in line:
            split1=line.rsplit(':"')[1]
            split2=split1.split('"')[0]
            ratingList.append(split2)
            lastName = split2
        elif 'pk_id' in line:
            i+=1

            split1=line.split(':')[1]
            split2=split1.split(',')[0]
            ratingList.append(split2)
        elif 'schoolid' in line:
            split1=line.split(':"')[1]
            split2=split1.split('"')[0]
            ratingList.append(split2)
        elif 'averagerating' in line:
            split1=line.split(':')[1]
            split2=split1.split(',')[0]
            ratingList.append(split2)
        elif 'total_number' in line:
            split1=line.split(':')[1]
            split2=split1.split(',')[0]
            ratingList.append(split2)
        elif 'teacherfirst' in line:
            split1=line.rsplit(':"')[1]
            split2=split1.split('"')[0]
            ratingList.append(split2)
            if len(split2) >0:
                ratingList.append(lastName + " " + split2[0])
            else:
                ratingList.append(None)
    return ratingList
main()
