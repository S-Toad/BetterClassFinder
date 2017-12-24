# pylint: disable=R0902
class ClassDate(object):
    """Creates a Class_Date object which contains information on when a class is."""
    def __init__(self, raw_time, raw_class):
        self.raw_time = raw_time
        self.raw_class = raw_class
        self.time_start = ''
        self.time_end = ''
        self.time_start_period = ''
        self.time_end_period = ''
        self.days = ''
        self.class_building = ''
        self.class_number = ''

    def clean(self):
        """Cleans up attributes of ClassDate"""
        if (self.raw_time == 'TBA' or self.raw_time.split(' ')[3] == '-'):
            self.days = 'TBA'
            self.time_start = self.time_end = self.time_start_period = self.time_end_period = None
        else:
            time_split = self.raw_time.split(' ')
            self.days = time_split[1]
            time_span = time_split[3]
            self.time_end_period = 'P' if time_split[4] == 'pm' else 'A'

            self.time_start, self.time_end = time_span.split('-')

            if self.time_end_period == 'A':
                self.time_start_period = 'A'
            else:
                time_start_int = int(self.time_start.split(':')[0])
                time_end_int = int(self.time_end.split(':')[0])

                if (time_start_int == 12 or
                        (time_end_int != 12 and time_start_int <= time_end_int)):
                    self.time_start_period = 'P'
                else:
                    self.time_start_period = 'A'

        if self.raw_class == 'TBA':
            self.class_building = 'TBA'
            self.class_number = 'N/A'
        else:
            self.class_building, self.class_number = self.raw_class.split(' ')
            self.class_number = self.class_number.replace(u'\xa0', u'')

    def get_military_time(self):
        """Converts stored time attributes to military time

        Returns:
            Integer List (Ex: [800, 1000])"""
        if not self.time_start:
            return [-1, -1]

        military_time = []

        start_time_int = int(self.time_start.replace(":", ""))
        end_time_int = int(self.time_end.replace(":", ""))

        if self.time_start_period == 'A':
            military_time.append(start_time_int)
        else:
            military_time.append(start_time_int + 1200)

        if self.time_end_period == 'A':
            military_time.append(end_time_int)
        else:
            military_time.append(end_time_int + 1200)

        return military_time
