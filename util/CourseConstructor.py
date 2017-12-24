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

        if "-" in self.credits:
            self.creditMin, self.creditMax = self.credits.split("-")
        elif "/" in self.credits:
            numerator, denominator = self.credits.split("/")
            self.creditMin = self.creditMax = float(numerator) / float(denominator)
        else:
            self.creditMin = self.creditMax = self.credits


        return Course(
            self.subject,
            self.courseNumber,
            self.className,
            self.profName,
            self.gur,
            self.dates,
            self.creditMin,
            self.creditMax,
            self.fee,
            self.restrictions,
            self.prereq,
            self.additionalInfo,
            self.crn
        )
