from TimeRange import TimeRange
from Course import Course
from CourseConstructor import CourseConstructor
from bs4 import BeautifulSoup
import requests
# TODO: Possible values for the parameters should be scraped from database, maybe?

class DatabaseFetcher():
    WINTER_TERM = '201810'
    URL = 'https://admin.wwu.edu/pls/wwis/wwsktime.ListClass'     
    STARTING_FONT = 16
    
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
        timeRange=TimeRange(0, 'A', 0, 'A'),
        credits='%',
        courseNumber=''
    ):
        # Copy the default post dictionary so that values and params can be added
        self.postDict = self.BASE_DICT.copy()
        
        # Code below appends onto the dictionary
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
        
        # If we're not looking for open classes we simply send a payload of nothing because that makes sense right
        if (open):
            self.postDict['sel_open'].append('Y')
    
    def query(self):
        # Prints out our post request to verify it was generated quickly
        print(self.postDict)
        # Send the request to the DB
        r = requests.post(self.URL, self.postDict)
        print(r.status_code, r.reason)
        
        # Parses the text and writes it to a file for further verificaiton
        soup = BeautifulSoup(r.text, 'html.parser')
        f = open('test.html', 'w')
        f.write(soup.prettify())
        f.close()

        # CRNs nicely line up with the courses so we collect them and leave them in a list for now
        crns = soup.find_all('input', {"name" : "sel_crn"})
        
        # 'font' is the tag that houses all the data we're looking for, how convienient :D
        results = soup.find_all('font')
        
        # We start the construction of a course, everytime a new course is created we set this to a new course constructor
        courseConstructor = CourseConstructor()
        courseList = []
        
        # We start on 16 (STARTING_FONT) so that we can skip the headers of the table.
        # This magic number is gathered from the raw html page
        i = self.STARTING_FONT
        # J is essentially the index of courses, it keeps account of what CRNs we're tying.
        # This makes more sense later down
        j = 0
        cap = len(results)
        print("-------------")
        while i < cap:
            # We get the the current text we're on and get rid of trailing characters
            resultText = results[i].text.rstrip()

            # Increment our line
            i+=1

            # GURs are simply a single word which makes this check very easy to do and find
            # Example 'QSR'
            if (resultText in self.ALL_GURS):
                courseConstructor.gur = resultText
                continue

            # Staff is also another easy knock out, this is a professor name when the prof has
            # not been decided yet. Single word string
            if (resultText == 'Staff'):
                courseConstructor.profName = resultText
                continue

            # Prerequisites are an easy check off as well. We follow the text after seeing this line
            # At the end of this is where we construct as well
            if (resultText == 'Prerequisites:'):
                prereq = ''
                prereq += results[i].text.rstrip()
                i+=1

                # We essentially keep iterating through future lines until we either hit a new subject or
                # we hit the end of the file.
                while(True):
                    # End of file condition
                    if (i + 1 > cap):
                        break

                    # Blank line condition
                    if (results[i].text.rstrip() == ''):
                        i+=1
                        continue

                    # New subject condition
                    if (results[i].text.rstrip().split(' ')[0] in self.ALL_SUBJECTS):
                        break

                    # New prereq line so we append to what we have so far
                    prereq += ' ' + results[i].text.rstrip()
                    i+=1

                # Get rid of double spaces and replace with single
                prereq = ' '.join(prereq.split())
                # Get rid of waitlist avaialable, we can show this a different way later
                prereq = prereq.replace('CLOSED: Waitlist Available', '')
                courseConstructor.prereq = prereq

                # When we construct we finally get our crns via another list. The order is thankfully consistent with 
                # our classes
                courseConstructor.crn = crns[j]['value']
                j+=1

                # Construct and generate new constructor
                # TODO: Add to list here
                courseConstructor.construct()
                courseConstructor = CourseConstructor()
                continue

            # If there's a comma we either have a a prereq or a professor name.
            # Normally we should check to see if splitting the string on a ', ' results in 2 words because
            # a prereq could have a comma.
            # However we find prereqs following a "Prerequisites" making this additional check pointless
            if (', ' in resultText):
                splitString = resultText.split(', ')
                courseConstructor.profName = splitString[1] + ' ' + splitString[0]
                continue

            # If there's a - the only thing that has that is a date span or a time span
            # We determine which is which from checking to see if it has a / or a :
            # We can be pretty sure in what we find
            if ('-' in resultText):
                if ('/' in resultText):
                    courseConstructor.span = resultText
                    continue
                if (':' in resultText):
                    courseConstructor.time = resultText
                    continue

            # If we've gotten this far we got rid of all the easy checks, so we need to see what happens if we split on a space.
            # We could get a class or a building.
            splitString = resultText.split(' ')

            # If the first word is a value in all of our subjects, we have a subject
            if (splitString[0] in self.ALL_SUBJECTS):
                courseConstructor.subject = splitString[0] # Class is the first part
                courseConstructor.classNumber = splitString[1] # Class number is the second part
                courseConstructor.name = results[i].text.rstrip() # Clean text up, the detailed name is convinentlty the next line
                i+=1 # Increment since we stole the text from the next iteration
                courseConstructor.classSize = results[i].text.rstrip() # Conviently after class name
                i+=1 # Iterate because we skipped over again
            else: # If the first word isnt a subject we can assume is the room building
                courseConstructor.roomBuilding = splitString[0] # Part 1 of string
                courseConstructor.roomNumber = splitString[1] # Part 2 of string
                courseConstructor.credits = results[i].text.rstrip() # Credits is also convinentlty after room number too
                i+=1 # Again, increment because we stole the next results
            continue
