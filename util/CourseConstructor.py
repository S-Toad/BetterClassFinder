from util.Course import Course


# pylint: disable=too-many-instance-attributes
# pylint: disable=too-few-public-methods
class CourseConstructor(object):
    """CourseConstructor prepares a Course Object to be created"""
    def __init__(self):
        self.subject = ''
        self.course_number = ''
        self.class_name = ''
        self.class_size = ''
        self.prof_name = ''
        self.span = ''
        self.gur = ''
        self.dates = []
        self.credits = ''
        self.fee = ''
        self.restrictions = ''
        self.prereq = ''
        self.additional_info = ''
        self.crn = ''
        self.credit_min = ''
        self.credit_max = ''

    def construct(self):
        """Constructs course object using attributes.

        Returns:
            Course Object
        """
        self.prereq = self.prereq.replace('  ', ' ').rstrip()
        self.restrictions = self.restrictions.replace('  ', ' ').rstrip()
        self.additional_info = self.additional_info.replace('  ', ' ').rstrip()

        # There's a space in front of these strings
        self.prereq = self.prereq[1:]
        self.restrictions = self.restrictions[1:]
        self.additional_info = self.additional_info[1:]

        # Performing our own check later
        self.additional_info = self.additional_info.replace('CLOSED:  Waitlist Available', '')
        self.additional_info = self.additional_info.replace('CLOSED', '')

        if self.fee != '':
            self.fee = "$" + self.fee.split("$")[1]

        for course_date in self.dates:
            course_date.clean()

        if "-" in self.credits:
            self.credit_min, self.credit_max = self.credits.split("-")
        elif "/" in self.credits:
            numerator, denominator = self.credits.split("/")
            self.credit_min = self.credit_max = float(numerator) / float(denominator)
        else:
            self.credit_min = self.credit_max = self.credits


        return Course(
            self.subject,
            self.course_number,
            self.class_name,
            self.prof_name,
            self.gur,
            self.dates,
            self.credit_min,
            self.credit_max,
            self.fee,
            self.restrictions,
            self.prereq,
            self.additional_info,
            self.crn
        )
