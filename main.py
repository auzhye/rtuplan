import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
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
def get_today_tomorrow_classes(events):
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow_start = today_start + timedelta(days=1)
    day_after_start = tomorrow_start + timedelta(days=1)

    today_ms = int(today_start.timestamp() * 1000)
    tomorrow_ms = int(tomorrow_start.timestamp() * 1000)
    day_after_ms = int(day_after_start.timestamp() * 1000)

    today_classes = []
    tomorrow_classes = []

    for event in events:
        event_time = int(event)
        if today_ms <= event_time < tomorrow_ms:
            today_classes.append(event)
        elif tomorrow_ms <= event_time < day_after_ms:
            tomorrow_classes.append(event)

    return today_classes, tomorrow_classes


kalendars = Kalendars()
izv = kalendars.chooseSemester()
programs = kalendars.getPrograms(izv)
progId = kalendars.chooseProgramId(programs)
course = kalendars.chooseCourse(izv, progId)
group = kalendars.chooseGroup(izv, progId, course)
list = kalendars.getSemEventList(group)
dates = kalendars.getDates(list)
temp = []

today_classes, tomorrow_classes = get_today_tomorrow_classes(dates)
if not today_classes:
    dateorigins = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    dateorigin = dateorigins + timedelta(days=1)
    dateorigin = dateorigin.strftime('%Y-%m-%d')
    for x in tomorrow_classes:
        temp.append(x)
    temp.sort()
else:
    for x in dates:
        if x > current_milli_time() and x < int(time.time() * 1000 + 86400000): # bigger than current day, smaller than next day
            temp.append(x)
        else:
            pass
    temp.sort()

mobilly = Mobilly()
for x in mobilly.getStations()['stations']:
    print(x['letter_code'] + " : " + x['station_name'])
froms = input("Izvelies sakuma staciju: ")

trains = mobilly.getTrains(froms, "RIG", dateorigin)



# need to sort todays lekcijas times aswell
print("Dates:\n\n")
for x in temp:
    print(x)
print("Current: " + str(current_milli_time()) + "\n")
print("Day after: " + str(int(time.time() * 1000 + 86400000)) +"\n")
temp2 = []
i = 0
for x in trains['scheduled_route_costs']:
    if int(x['departure_datetime'])*1000 > current_milli_time():
        temp2.append(x)
        i+=1
temp3 = []
for x in temp2:
    print(x)
    if int(x['departure_datetime']) * 1000 > (temp[0] - 3 * 3600 * 1000) and int(x['departure_datetime']) * 1000 < temp[0]:
        
        temp3.append(x)
print("Departures: ")
for x in temp3:
    print(x)
print(i)