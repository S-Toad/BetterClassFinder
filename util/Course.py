
class Course():
    def __init__(
        self,
        subject,
        courseNumber,
        className,
        profName,
        gur,
        dates,
        creditMin,
        creditMax,
        fee,
        restrictions,
        prereq,
        additionalInfo,
        crn
        ):
        self.subject = subject
        self.courseNumber = courseNumber
        self.className = className
        self.profName = profName
        self.gur = gur
        self.dates = dates
        self.creditMin = creditMin
        self.creditMax = creditMax
        self.fee = fee
        self.restrictions = restrictions
        self.prereq = prereq
        self.additionalInfo = additionalInfo
        self.crn = crn
