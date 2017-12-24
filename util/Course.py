class Course(object):
    """Course Object. Houses data concerning a course"""
    # pylint: disable=R0913
    # pylint: disable=R0902
    # pylint: disable=R0903
    def __init__(
            self,
            subject,
            course_number,
            class_name,
            prof_name,
            gur,
            dates,
            credits_min,
            credits_max,
            fee,
            restrictions,
            prereq,
            additional_info,
            crn
        ):
        self.subject = subject
        self.course_number = course_number
        self.class_name = class_name
        self.prof_name = prof_name
        self.gur = gur
        self.dates = dates
        self.credits_min = credits_min
        self.credits_max = credits_max
        self.fee = fee
        self.restrictions = restrictions
        self.prereq = prereq
        self.additional_info = additional_info
        self.crn = crn
