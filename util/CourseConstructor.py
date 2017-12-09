from Course import Course

class CourseConstructor():
    def __init__(self):
        self.name = ''
        self.subject = ''
        self.classNumber = ''
        self.crn = ''
        self.roomBuilding = ''
        self.roomNumber = ''
        self.credits = ''
        self.classSize = ''
        self.profName = ''
        self.span = ''
        self.gur = ''
        self.prereq = ''
        
        self.time = ''
        self.timeStart = ''
        self.timeStartPeriod = ''
        self.timeEnd = ''
        self.timeEndPeriod = ''
        self.days = []
    
    def construct(self):
    
        self.generateTimes()
        
        f = open('courses.txt', 'a')
        
        f.write("--------------------------\n")
        f.write("Name: " + self.name + '\n')
        f.write("Subject: " + self.subject + '\n')
        f.write("Class Number: " + self.classNumber + '\n')
        f.write("Class Size: " + self.classSize + '\n')
        f.write("Credits: " + self.credits + '\n')
        f.write("CRN: " + self.crn + '\n')
        f.write("Building: " + self.roomBuilding + '\n')
        f.write("Room Number: " + self.roomNumber + '\n')
        f.write("Prereq: " + self.prereq + '\n')
        f.write("Prof Name: " + self.profName + '\n')
        f.write("Span: " + self.span + '\n')
        f.write("GUR: " + self.gur + '\n')
        
        f.write("Start: " + self.timeStart + '\n')
        f.write("Start Period: " + self.timeStartPeriod+ '\n')
        f.write("End: " + self.timeEnd + '\n')
        f.write("End Period: " + self.timeEndPeriod + '\n')
        
        f.close()
        
        # return Course(
            # self.name,
            # self.subject,
            # self.classNumber,
            # self.crn,
            # self.roomBuilding,
            # self.roomNumber,
            # self.credits
        # )
    
    def generateTimes(self):
        if ('pm' in self.time):
            self.timeEndPeriod = 'P'
        else:
            self.timeEndPeriod = 'A'
        
        splitString = ' '.join(self.time.split()).split(' ')
        
        for c in splitString[0]:
            self.days.append(c)
        
        if (self.timeEndPeriod == 'A'):
            self.timeStartPeriod = 'A'
            return
        
        splitTimeString = splitString[1].split('-')
        
        self.timeStart = splitTimeString[0]
        self.timeEnd = splitTimeString[1]
        
        startTimeInt = int(self.timeStart.split(':')[0])
        endTimeInt = int(self.timeEnd.split(':')[0])
        
        # Assuming that 11pm nor 12am are reasonable start times. Edge Cases
        if ((startTimeInt > endTimeInt and startTimeInt != 12) or startTimeInt == 11):
            self.timeStartPeriod = 'A'
        else:
            self.timeStartPeriod = 'P'