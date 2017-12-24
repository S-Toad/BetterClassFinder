import copy
import requests
from util.ClassDate import ClassDate
from util.CourseConstructor import CourseConstructor
from bs4 import BeautifulSoup


# TODO: Possible values for the parameters should be scraped from database, maybe?
class DatabaseFetcher(object):
    """Performs queries on Classfinder"""

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
        # 'All', Doesn't work
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

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=R0913
    def __init__(
            self,
            subjects=None,
            gurs=None,
            available_slots=False,
            term=WINTER_TERM,
            instructor='ANY',
            start_time=0,
            start_time_period='A',
            end_time=0,
            end_time_period='A',
            days=None,
            course_credits='%',
            course_number=''
    ):
        if not subjects:
            self.subjects = self.ALL_SUBJECTS

        if not gurs:
            self.gurs = ['All']

        if not days:
            self.days = []

        # Copy the default post dictionary so that values and params can be added
        self.post_dictionary = copy.deepcopy(self.BASE_DICT)

        self.post_dictionary['sel_subj'].extend(subjects)
        self.post_dictionary['sel_gur'].extend(gurs)
        self.post_dictionary['sel_day'].extend(days)
        self.post_dictionary['term'] = term
        self.post_dictionary['sel_inst'] = instructor
        self.post_dictionary['sel_cdts'] = course_credits
        self.post_dictionary['sel_crse'] = course_number
        self.post_dictionary['begin_hh'] = start_time
        self.post_dictionary['begin_mi'] = start_time_period
        self.post_dictionary['end_hh'] = end_time
        self.post_dictionary['end_mi'] = end_time_period

        # Only send payload if we want open courses
        if available_slots:
            self.post_dictionary['sel_open'].append('Y')

    def query(self):
        """Performs a post request

        Returns: List of Courses"""
        classfinder_request = requests.post(self.URL, self.post_dictionary)
        return self.construct_courses(classfinder_request)

    # pylint: disable=R0914
    # pylint: disable=R0915
    # pylint: disable=R0912
    def construct_courses(self, request):
        """ Creates a list of courses from a classfinder request

        Args:
            Request

        Returns:
            List of Courses"""

        soup = BeautifulSoup(request.text, 'html.parser')
        crns = soup.find_all('input', {"name" : "sel_crn"})
        results = soup.find_all('font')

        course_constructor = CourseConstructor()
        course_list = []

        line_index = self.STARTING_FONT_INDEX
        course_counter = 0
        cap = len(results)
        while line_index < cap:
            while (line_index < cap and not self.is_course(results[line_index])):
                line_index += 1

            if line_index == cap:
                break

            result_text = results[line_index].text
            result_text = result_text.replace('I T', 'IT')  # DB has this subject named incorrectly

            course_constructor.subject, course_constructor.course_number = result_text.split(' ')

            line_index += 1
            course_constructor.class_name = results[line_index].text

            line_index += 1
            course_constructor.class_size = results[line_index].text

            line_index += 3
            course_constructor.prof_name = results[line_index].text

            line_index += 1
            course_constructor.span = results[line_index].text

            line_index += 1
            result_text = results[line_index].text
            if result_text != '':
                course_constructor.gur = result_text

            line_index += 1
            time = results[line_index].text

            line_index += 1
            room = results[line_index].text
            course_constructor.dates.append(ClassDate(time, room))

            line_index += 1
            course_constructor.credits = results[line_index].text

            line_index += 1
            result_text = results[line_index].text
            if "$" in result_text:
                course_constructor.fee = result_text
                line_index += 1
                if line_index == cap:
                    break

            prereq = ''
            restrictions = ''
            additional_info = ''

            result_text = results[line_index].text
            if ':' in result_text and '-' in result_text:
                time = results[line_index].text
                line_index += 1
                room = results[line_index].text
                line_index += 1

                course_constructor.dates.append(ClassDate(time, room))

            if line_index == cap:
                break

            result_text = results[line_index].text
            if result_text == 'Restrictions: ':
                line_index += 1
                while (line_index != cap and
                       results[line_index].text != 'Prerequisites:' and
                       self.has_red_font(results[line_index])):
                    restrictions += ' '  + results[line_index].text
                    line_index += 1
                course_constructor.restrictions = restrictions

            if line_index == cap:
                break

            result_text = results[line_index].text
            if result_text == 'Prerequisites:':
                line_index += 1
                while line_index != cap and self.has_red_font(results[line_index]):
                    prereq += ' ' + results[line_index].text
                    line_index += 1
                course_constructor.prereq = prereq

            while line_index != cap and self.is_additional_info(results[line_index]):
                additional_info += ' '  + results[line_index].text
                line_index += 1

            course_constructor.additional_info = additional_info
            course_constructor.crn = crns[course_counter]['value']
            course_list.append(course_constructor.construct())
            course_constructor = CourseConstructor()
            course_counter += 1

            # When we reach a new course section we have to skip over a few lines of junk
            if line_index != cap and results[line_index].text == 'Class':
                line_index += 14
        return course_list

    @staticmethod
    def has_red_font(result):
        """Checks if bs4 result has red font

        Returns: Boolean, True if red font"""
        return result.has_attr('color') and result['color'] == 'red'

    @staticmethod
    def is_course(result):
        """Checks if bs4 result is a school course

        Returns: Boolean, True if course"""
        return result.find('a') != None

    @staticmethod
    def is_additional_info(result):
        """Checks if bs4 result has small text, AKA additional info

        Returns: Boolean, True if small text"""
        return result.has_attr('size') and result['size'] == '-2'
