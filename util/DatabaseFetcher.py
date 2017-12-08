from TimeRange import TimeRange
from Course import Course
from bs4 import BeautifulSoup
import requests
# TODO: Possible values for the parameters should be scraped from database, maybe?

class DatabaseFetcher():
    WINTER_TERM = '201810'
    URL = 'https://admin.wwu.edu/pls/wwis/wwsktime.ListClass'     
    
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
    ALL_GURS = [
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
    
    PASS_ON_LIST = [
        'Class',
        'Title',
        'Crn',
        'Instructor',
        'Dates',
    ]
    
    BASE_DICT = {
        'sel_subj' : [
            'dummy',
            'dummy',
        ],
        'sel_gur' : [
            'dummy',
            'dummy',
        ],
        'sel_day' : [
            'dummy',
        ],
        'sel_open' : [
            'dummy',
        ],
        'term' : '',
        'sel_inst' : '',
        'sel_crn' : '', #Doesnt do anything
        'sel_crse' : '',
        'begin_hh' : '',
        'end_hh' : '',
        'begin_mi' : '',
        'end_mi' : '',
        'sel_cdts' : '',
    }

    def __init__(
        self,
        subjects=ALL_SUBJECTS,
        gurs=['All'],
        open=False,
        term=WINTER_TERM,
        instructor='ANY',
        timeRange=TimeRange(0, 'A', 0, 'A'),
        credits='%',
        courseNumber=''
    ):
        self.postDict = self.BASE_DICT.copy()
        
        self.postDict['sel_subj'].extend(subjects)
        self.postDict['sel_gur'].extend(gurs)
        self.postDict['sel_day'].extend(timeRange.days)
        
        self.postDict['term'] = term
        self.postDict['sel_inst'] = instructor
        self.postDict['sel_cdts'] = credits
        self.postDict['sel_crse'] = courseNumber
        
        self.postDict['begin_hh'] = timeRange.startTime
        self.postDict['begin_mi'] = timeRange.startTimePeriod
        self.postDict['end_hh'] = timeRange.endTime
        self.postDict['end_mi'] = timeRange.endTimePeriod
        
        if (open):
            self.postDict['sel_open'].append('Y')
    
    def query(self):
        print(self.postDict)
        r = requests.post(self.URL, self.postDict)
        print(r.status_code, r.reason)
        # print(r.text + '...')
        
        courseList = []
        
        soup = BeautifulSoup(r.text, 'html.parser')
        f = open('test.html', 'w')
        f.write(soup.prettify())
        f.close()
        
        results = soup.find_all('font', {'color': '#000080'})
        
        # for result in results:
            # print(result.text)
        
        i = 5
        cap = len(results)
        while i < 20:
            tempList = results[i].text.split(' ')
            classSubject = tempList[0]
            classNumber = tempList[1]
            i += 1
            
            className = results[i].text
            i += 1
            
            profName = results[i].text
            profFirst = None
            profSecond = None
            
            if (', ' in profName):
                tempList = profFirst.split(', ')
                profFirst = tempList[1]
                profSecond = tempList[0]
            else:
                # 'Staff' is an example of what may occur here
                profFirst = profName
                profSecond = ''
            i += 1
            # Do something with span here
            i += 1
            print("Class: " + results[i].text)
            print("Class Name: " + results[i].text)
            print("Class Prof: " + results[i].text)
            print("Span: " + results[i].text)
            print("-------------")
            
        #tables = soup.find_all("table")
        #table = tables[1]
        
        #print(table)