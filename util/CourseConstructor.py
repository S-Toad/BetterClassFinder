from util.Course import Course

class CourseConstructor():
    def __init__(self):
        self.subject = ''
        self.courseNumber = ''
        self.className = ''
        self.classSize = ''
        self.profName = ''
        self.span = ''
        self.gur = ''
        self.dates = []
        self.credits = ''
        self.fee = ''
        self.restrictions = ''
        self.prereq = ''
        self.additionalInfo = ''
        self.crn = ''

    def construct(self):
        self.prereq = self.prereq.replace('  ', ' ').rstrip()
        self.restrictions = self.restrictions.replace('  ', ' ').rstrip()
        self.additionalInfo = self.additionalInfo.replace('  ', ' ').rstrip()
    
        # There's a space in front of these strings
        self.prereq = self.prereq[1:]
        self.restrictions = self.restrictions[1:]
        self.additionalInfo = self.additionalInfo[1:]
        
        # This isn't true all time time
        self.additionalInfo = self.additionalInfo.replace('CLOSED:  Waitlist Available', '')
        self.additionalInfo = self.additionalInfo.replace('CLOSED', '')

        if (self.fee != ''):
            self.fee = "$" + self.fee.split("$")[1]

        for courseDate in self.dates:
            courseDate.clean()
        '''
        f = open('courses.txt', 'a')        
        f.write("--------------------------\n")
        f.write("Name: " + self.className + '\n')
        f.write("Subject: " + self.subject + '\n')
        f.write("Course Number: " + self.courseNumber + '\n')
        f.write("Class Size: " + self.classSize + '\n')
        f.write("Prof Name: " + self.profName + '\n')
        f.write("Span: " + self.span + '\n')
        f.write("GUR: " + self.gur + '\n')
        f.write("Credits: " + self.credits + '\n')
        f.write("Fee: " + self.fee + '\n')
        f.write("Restrictions: " + self.restrictions + '\n')
        f.write("Prereq: " + self.prereq + '\n')
        f.write("Additional Info: " + self.additionalInfo + '\n')
        f.write("CRN: " + self.crn + '\n')
        
        for courseDate in self.dates:
            courseDate.clean()
            f.write('Days: ' + courseDate.days + '\n')
            f.write('Time: ' + courseDate.timeStart + courseDate.timeStartPeriod + '-' + courseDate.timeEnd + courseDate.timeEndPeriod + '\n')
            f.write('Room: ' + courseDate.classBuilding + ' ' + courseDate.classNumber + '\n')
        
        f.close()
        '''
        
        return Course(
            self.subject,
            self.courseNumber,
            self.className,
            self.profName,
            self.gur,
            self.dates,
            self.credits,
            self.fee,
            self.restrictions,
            self.prereq,
            self.additionalInfo,
            self.crn
        )
