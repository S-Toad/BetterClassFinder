
class ClassDate():
    def __init__(self, rawTime, rawClass):
        self.rawTime = rawTime
        self.rawClass = rawClass
        
        self.timeStart = ''
        self.timeEnd = ''
        self.timeStartPeriod = ''
        self.timeEndPeriod = ''
        self.days = ''
        self.classBuilding = ''
        self.classNumber = ''
    
    def clean(self):
        if (self.rawTime == 'TBA' or self.rawTime.split(' ')[3] == '-'):
            self.days = 'TBA'
            self.timeStart = self.timeEnd = self.timeStartPeriod = self.timeEndPeriod = None
        else:
            timeSplit = self.rawTime.split(' ')
            self.days = timeSplit[1]
            timeSpan = timeSplit[3]
            self.timeEndPeriod = 'P' if timeSplit[4] == 'pm' else 'A'
            
            self.timeStart, self.timeEnd = timeSpan.split('-')
            
            if (self.timeEndPeriod == 'A'):
                self.timeStartPeriod = 'A'
            else:
                timeStartInt = int(self.timeStart.split(':')[0])
                timeEndInt = int(self.timeEnd.split(':')[0])
                
                if (timeStartInt == 12 or (timeEndInt != 12 and timeStartInt <= timeEndInt)):
                    self.timeStartPeriod = 'P'
                else:
                    self.timeStartPeriod = 'A'
        
        if (self.rawClass == 'TBA'):
            self.classBuilding = 'TBA'
            self.classNumber = 'N/A'
        else:
            self.classBuilding, self.classNumber = self.rawClass.split(' ')
            self.classNumber = self.classNumber.replace(u'\xa0', u'')

    def getMilitaryTime(self):
        if not self.timeStart:
            return [-1, -1]

        militaryTime = []

        startTimeInt = int(self.timeStart.replace(":", ""))
        endTimeInt = int(self.timeEnd.replace(":", ""))

        if (self.timeStartPeriod == 'A'):
            militaryTime.append(startTimeInt)
        else:
            militaryTime.append(startTimeInt + 1200)
        
        if (self.timeEndPeriod == 'A'):
            militaryTime.append(endTimeInt)
        else:
            militaryTime.append(endTimeInt + 1200)

        return militaryTime
