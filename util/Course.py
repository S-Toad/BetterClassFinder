
class Course():
    def __init__(
        self,
        subject,
        courseNumber,
        className,
        profName,
        gur,
        dates,
        credits,
        fee,
        restrictions,
        prereq,
        additionalInfo
        ):
        self.subject = subject
        self.courseNumber = courseNumber
        self.className = className
        self.profName = profName
        self.gur = gur
        self.dates = dates
        self.credits = credits
        self.fee = fee
        self.restrictions = restrictions
        self.prereq = prereq
        self.additionalInfo = additionalInfo
