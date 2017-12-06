from TimeRange import TimeRange
# TODO: Possible values for the parameters should be scraped from database, maybe?

class DatabaseFetcher():
    WINTER_TERM = '201810'
    
    ALL_SUBJECTS = [
        'A/HI',
        'ACCT',
        'AECI',
        'AHE',
        'AMST',
        'ANTH',
        'ARAB',
        'ART',
        'ASTR',
        'BIOL',
        'C/AM',
        'C2C',
        'CD',
        'CHEM',
        'CHIN',
        'CISS',
        'CLST',
        'COMM',
        'CSCI',
        'CSD',
        'DNC',
        'DSCI',
        'DSGN',
        'EAST',
        'ECE',
        'ECON',
        'EDAD',
        'EDUC',
        'EE',
        'EGEO',
        'ELED',
        'ELL',
        'ENG',
        'ENGR',
        'ENRG',
        'ENTR',
        'ENVS',
        'ESCI',
        'EUS',
        'FAIR',
        'FIN',
        'FREN',
        'GEOL',
        'GERM',
        'GRAD',
        'GREK',
        'HIST',
        'HLED',
        'HNRS',
        'HRM',
        'HSP',
        'I T',
        'IBUS',
        'ID',
        'INTL',
        'ITAL',
        'JAPN',
        'JOUR',
        'KIN',
        'KORE',
        'LANG',
        'LAT',
        'LBRL',
        'LDST',
        'LIBR',
        'LING',
        'M/CS',
        'MATH',
        'MBA',
        'MDS',
        'MFGE',
        'MGMT',
        'MIS',
        'MKTG',
        'MPAC',
        'MSCI',
        'MUS',
        'NURS',
        'OPS',
        'PCE',
        'PE',
        'PHIL',
        'PHYS',
        'PLSC',
        'PORT',
        'PSY',
        'RC',
        'RECR',
        'RUSS',
        'SAA',
        'SCED',
        'SEC',
        'SMNR',
        'SOC',
        'SPAN',
        'SPED',
        'TESL',
        'THTR',
        'VHCL',
        'WGSS',
    ]
    
    # Mostly for reference
    ALL_GURS= [
        'All',
        'ACOM',
        'ACGM',
        'BCOM',
        'BCGM',
        'CCOM',
        'CPST',
        'CF',
        'CF-E',
        'FIG',
        'TRVL',
        'FYE',
        'HUM',
        'LSCI',
        'SCI',
        'OL',
        'QSR',
        'SL',
        'SSC',
        'BREX',
        'BNEX',
        'DLEX',
        'EVEX',
        'MVEX',
        'NCEX',
        'PAEX',
        'PBEX',
        'NSEX',
        'TAEX',
        'WP1',
        'WP2',
        'WP3',
    ]

    def __init__(
        self,
        subjects=ALL_SUBJECTS,
        gurs=['All'],
        days=[],
        open=False,
        terms=[WINTER_TERM],
        instructors=['ANY'],
        timeRanges=[TimeRange(0, 'A', 0, 'A')],
        credits=['%25'],
        courses=['']
    ):
        
        self.subjects = subjects
        self.gurs = gurs
        self.days = days
        self.open = ['Y'] if open else []
        self.terms = terms
        self.instructors = instructors
        self.timeRanges = timeRanges
        self.credits = credits
        self.courses = courses
    
    def buildBaseString(self):
        URL = 'https://admin.wwu.edu/pls/wwis/wwsktime.ListClass?sel_subj=dummy&sel_subj=dummy&sel_gur=dummy&sel_gur=dummy&sel_day=dummy&sel_open=dummy&sel_crn=&'
        
        #URL += self.buildParam('term', self.term)
        #URL += self.buildParam('sel_inst', self.instructors)
        #URL += self.buildParam('sel_crse', self.courses)
        #URL += 'begin_hh=' + str(self.timeRanges[0].startTime) + "&"
        #URL += 'end_hh=' + str(self.timeRanges[0].endTime) + "&"
        #URL += 'begin_mi=' + str(self.timeRanges[0].startTimePeriod) + "&"
        #URL += 'end_mi=' + str(self.timeRanges[0].endTimePeriod) + "&"
        #URL += self.buildParam('sel_cdts', self.credits)
        URL += self.buildListParam('sel_day', self.days)
        URL += self.buildListParam('sel_gur', self.gurs)
        URL += self.buildListParam('sel_subj', self.subjects)
        URL += self.buildListParam('sel_open', self.open)
        
        return URL

    def buildListParam(self, prefix, listItem):
        paramString = ""
    
        for item in listItem:
            stringItem = str(item)
            if (stringItem == 'All'):
                return prefix + '=' + stringItem + '&'
        
            paramString += prefix + '=' + stringItem
            paramString += "&"
            
        return paramString
    
    def buildParam(self, prefix, item):
        return prefix + '=' + item + '&'
   
    def query(self):
        baseString = self.buildBaseString()
        appendors = []
        for term in self.terms:
            termString = self.buildParam('term', term)
            for instructor in self.instructors:
                instructorString = termString + self.buildParam('sel_inst', instructor)
                for course in self.courses:
                    courseString = instructorString + self.buildParam('sel_crse', course)
                    for credit in self.credits:
                        creditString = courseString + self.buildParam('sel_cdts', credit)
                        for timeRange in self.timeRanges:
                            timeRangeString = creditString
                            timeRangeString += buildParam('begin_hh', timeRange.startTime)
                            timeRangeString += buildParam('end_hh', timeRange.endTime)
                            timeRangeString += buildParam('begin_mi', timeRange.startTimePeriod)
                            timeRangeString += buildParam('end_mi', timeRange.endTimePeriod)
                            
                            appendors.append(timeRangeString)
        
        for appendor in appendors:
            print(baseString + appendor)