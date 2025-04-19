import requests
from bs4 import BeautifulSoup
from datetime import date
import time

class Kalendars:
    def __init__(self):
        self.URL = "https://nodarbibas.rtu.lv"
        self.html = BeautifulSoup(requests.get(self.URL).text, 'html.parser')
    def chooseSemester(self):
        options = self.html.select('#semester-id option')
        for x in options:
            print(x['value'] + " : " + x.text)
        izvele = input("Izvelies semestri: ")
        return izvele
    def getSemesterDate(self, izvele):
        r = requests.post(self.URL + "/getChousenSemesterStartEndDate", data={
            'semesterId':izvele
        })
        return r.json()
    def getPrograms(self, izvele):
        r = requests.post(self.URL + "/findProgramsBySemesterId", data={
            'semesterId':izvele
        })
        return r.json()
    def chooseProgramId(self, programs):
        for x in programs:
            print("\n\n" + x['titleLV'] + " : \n")
            for y in x['program']:
                print(str(y['programId']) + ' : ' + y['titleLV'])
        programId = input('Izvelies programmu: ')
        return programId
    def chooseCourse(self, izvele, progId):
        r = requests.post(self.URL + "/findCourseByProgramId", data={
            'semesterId':izvele,
            'programId':progId
        })
        js =  r.json()
        for x in js:
            print(x)
        izv = input('Izvelies kursu: ')
        return izv
    def chooseGroup(self, izvele, progId, course):
        r = requests.post(self.URL + "/findGroupByCourseId", data={
            'semesterId':izvele,
            'programId':progId,
            'courseId':course
        })
        js =  r.json()
        for x in js:
            print(str(x['semesterProgramId']) + " : "+ x['group'])
        izv = input('Izvelies grupu: ')
        return izv
    def getSemSubj(self, groupId):
        r = requests.post(self.URL + "/getSemProgSubjects", data={
            'semesterProgramId':groupId,
        })
        js =  r.json()
        return js
    def getSemEventList(self, groupId):
        month = date.today().month
        print(month)
        year = date.today().year
        r = requests.post(self.URL + "/getSemesterProgEventList", data={
            'semesterProgramId':groupId,
            'year':year,
            'month':month
        })
        js =  r.json()
        return js
    def getDates(self, list):
        temp = []
        for x in list:
            temp.append(x['eventDate'])
        return temp

class Mobilly:
    def __init__(self):
        self.URL = "https://clients.mobilly.lv/api/"
    def getStations(self):
        r = requests.post(self.URL, data={
            "COMMAND":"TRAIN_STATIONS",
            "RESPONSE_TYPE":"JSON",
            "APPLICATION_VERSION":"276129",
            "OS":"web",
            "OS_VERSION":"1",
            "NUMBER":"22222222",
            "HASH2":"",
            "APPLICATION_KEY":"W34uZqCZf6Frd1vsHtxtKDPTGs5vusHC",
            "SHOW_ALL":"1"
        })
        return r.json() 
    def getTrains(self, fromD, toD, date):
        r = requests.post(self.URL + "?cmd=TRAIN_SCHEDULE", data={
            'DATE':date, # 2025-04-20
            "DEPART_STATION":fromD, # OGR
            "ARRIVE_STATION":toD, # RIG
            "COMMAND":"TRAIN_SCHEDULE",
            "RESPONSE_TYPE":"JSON",
            "APPLICATION_VERSION":"276129",
            "OS":"web",
            "OS_VERSION":"1",
            "NUMBER":"22222222",
            "HASH2":"",
            "FOR_ROUNDTRIP":"0",
            "APPLICATION_KEY":"W34uZqCZf6Frd1vsHtxtKDPTGs5vusHC"
        })
        return r.json()

def current_milli_time():
    return round(time.time() * 1000)
dateorigin = date.today().strftime('%Y-%m-%d')

kalendars = Kalendars()
izv = kalendars.chooseSemester()
programs = kalendars.getPrograms(izv)
progId = kalendars.chooseProgramId(programs)
course = kalendars.chooseCourse(izv, progId)
group = kalendars.chooseGroup(izv, progId, course)
list = kalendars.getSemEventList(group)
dates = kalendars.getDates(list)
temp = []
for x in dates:
    if x > current_milli_time():
        temp.append(x)
    else:
        pass


mobilly = Mobilly()
for x in mobilly.getStations()['stations']:
    print(x['letter_code'] + " : " + x['station_name'])
froms = input("Izvelies sakuma staciju: ")
trains = mobilly.getTrains(froms, "RIG", date.today().strftime('%Y-%m-%d'))



# need to sort todays lekcijas times aswell
temp2 = []
i = 0
for x in trains['scheduled_route_costs']:
    if int(x['departure_datetime'])*1000 > current_milli_time() and i<3:
        temp2.append(x)
        i+=1
for x in temp:
    print(x)
print("\n\n")
for x in temp2:
    print(x)