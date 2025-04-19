import requests
from bs4 import BeautifulSoup
from datetime import date

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
        for x in list:
            print(x['eventDate'])
    
# https://nodarbibas.rtu.lv/findCourseByProgramId  semesterId=24&programId=333
# https://nodarbibas.rtu.lv/findGroupByCourseId    courseId=1&semesterId=24&programId=333
# https://nodarbibas.rtu.lv/isSemesterProgramPublished  semesterProgramId=25644
# https://nodarbibas.rtu.lv/getSemProgSubjects          semesterProgramId=25644
# https://nodarbibas.rtu.lv/getSemesterProgEventList    semesterProgramId=25644&year=2025&month=4
# https://nodarbibas.rtu.lv/findProgramsBySemesterId

kalendars = Kalendars()
izv = kalendars.chooseSemester()
programs = kalendars.getPrograms(izv)
progId = kalendars.chooseProgramId(programs)
course = kalendars.chooseCourse(izv, progId)
group = kalendars.chooseGroup(izv, progId, course)
list = kalendars.getSemEventList(group)
print(kalendars.getDates(list))