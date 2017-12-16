from util.ClassDate import ClassDate
from util.Course import Course
from util.CourseConstructor import CourseConstructor
from bs4 import BeautifulSoup
import requests
# TODO: Possible values for the parameters should be scraped from database, maybe?

class DatabaseFetcher():
    WINTER_TERM = '201810'
    URL = 'https://admin.wwu.edu/pls/wwis/wwsktime.ListClass'     
    STARTING_FONT_INDEX = 16
    
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
#        'All', Doesn't work
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
        'sel_subj' : [ # Dummy values have to be passed because I bet debug code was left in
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
        'sel_crn' : '', # Doesnt do anything, see above comment
        'sel_crse' : '',
        'begin_hh' : '',
        'end_hh' : '',
        'begin_mi' : '',
        'end_mi' : '',
        'sel_cdts' : '',
    }

    # By default the parameters set is the equivlant of every single course
    def __init__(
        self,
        subjects=ALL_SUBJECTS,
        gurs=['All'],
        open=False,
        term=WINTER_TERM,
        instructor='ANY',
        startTime=0,
        startTimePeriod='A',
        endTime=0,
        endTimePeriod='A',
        days=[],
        credits='%',
        courseNumber=''
    ):
        # Copy the default post dictionary so that values and params can be added
        self.postDict = self.BASE_DICT.copy()
        
        # Code below appends onto the dictionary
        self.postDict['sel_subj'].extend(subjects)
        self.postDict['sel_gur'].extend(gurs)
        self.postDict['sel_day'].extend(days)
        
        self.postDict['term'] = term
        self.postDict['sel_inst'] = instructor
        self.postDict['sel_cdts'] = credits
        self.postDict['sel_crse'] = courseNumber
        
        self.postDict['begin_hh'] = startTime
        self.postDict['begin_mi'] = startTimePeriod
        self.postDict['end_hh'] = endTime
        self.postDict['end_mi'] = endTimePeriod
        
        # If we're not looking for open classes we simply send a payload of nothing because that makes sense right
        if (open):
            self.postDict['sel_open'].append('Y')
    
    def query(self):
        print(self.postDict)
        r = requests.post(self.URL, self.postDict)
        print(r.status_code, r.reason)
        
        return self.constructCourses(r)

    def constructCourses(self, request):
        soup = BeautifulSoup(request.text, 'html.parser')
        f = open('test.html', 'w')
        f.write(soup.prettify())
        f.close()
        crns = soup.find_all('input', {"name" : "sel_crn"})
        
        results = soup.find_all('font')
        
        courseConstructor = CourseConstructor()
        courseList = []
        
        i = self.STARTING_FONT_INDEX
        j = 0
        cap = len(results)
        while(i < cap):
            while(i < cap and not self.isClass(results[i])):
                i+=1

            if (i==cap):
                break

            resultText = results[i].text
            resultText = resultText.replace('I T', 'IT')

            print(resultText)
            courseConstructor.subject, courseConstructor.courseNumber = resultText.split(' ')

            i+=1
            courseConstructor.className = results[i].text

            i+=1
            courseConstructor.classSize = results[i].text

            i+=3
            courseConstructor.profName = results[i].text

            i+=1
            courseConstructor.span = results[i].text

            i+=1
            resultText = results[i].text
            if (resultText != ''):
                courseConstructor.gur = resultText

            i+=1
            time = results[i].text

            i+=1
            room = results[i].text
            courseConstructor.dates.append(ClassDate(time, room))

            i+=1
            courseConstructor.credits = results[i].text

            i+=1
            resultText = results[i].text
            if ("$" in resultText):
                courseConstructor.fee = resultText
                i+=1
                if(i == cap):
                    break

            additionalTimes = []
            prereq = ''
            restrictions = ''
            additionalInfo = ''

            resultText = results[i].text

            if (':' in resultText and '-' in resultText):
                time = results[i].text
                i+=1
                room = results[i].text
                i+=1

                courseConstructor.dates.append(ClassDate(time, room))

            if(i == cap):
                break
            resultText = results[i].text

            if (resultText == 'Restrictions: '):
                i+=1
                while(i != cap and results[i].text != 'Prerequisites:' and self.isRed(results[i])):
                    restrictions += ' '  + results[i].text
                    i+=1
                courseConstructor.restrictions = restrictions

            if(i == cap):
                break
            resultText = results[i].text

            if (resultText == 'Prerequisites:'):
                i+=1
                while(i != cap and self.isRed(results[i])):
                    prereq += ' ' + results[i].text
                    i+=1
                courseConstructor.prereq = prereq

            while (i != cap and self.isAdditionalInfo(results[i])):
                additionalInfo += ' '  + results[i].text
                i+=1

            courseConstructor.additionalInfo = additionalInfo
            courseConstructor.crn = crns[j]['value']
            courseList.append(courseConstructor.construct())
            courseConstructor = CourseConstructor()
            j+=1

            # When we reach a new course section we have to skip over a few lines of junk
            if (i != cap and results[i].text == 'Class'):
                print('SKIPPING')
                i+=14

        return courseList

    def isRed(self, result):
        return (result.has_attr('color') and result['color'] == 'red')

    def isClass(self, result):
        value = result.find('a')
        return (value != None)

    def isAdditionalInfo(self, result):
        return (result.has_attr('size') and result['size'] == '-2')
