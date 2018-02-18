from util.DatabaseFetcher import DatabaseFetcher
import os
import sys
import django
from subprocess import call
sys.path.insert(0, '../.')
os.environ["DJANGO_SETTINGS_MODULE"] = "mainWebsite.settings"
django.setup()
from BetterClassFinder.models import Course, Term, CourseDate

def main():
    WINTER_TERM_2018 = '201810'
    SPRING_TERM_2018 = '201820'

    call('python ../manage.py migrate BetterClassFinder zero', shell=True)
    call('python ../manage.py makemigrations BetterClassFinder', shell=True)
    call('python ../manage.py migrate BetterClassFinder', shell=True)

    database_fetcher = DatabaseFetcher(
        term=SPRING_TERM_2018,
    )

    course_list = database_fetcher.query()

    term = Term(name="Winter 2018")
    term.save()
    for course in course_list:
        primary_date = course.dates[0]
        military_time = primary_date.get_military_time()
        primary_date_model = CourseDate(
            time_start=military_time[0],
            time_end=military_time[1],
            time_days=primary_date.days,
            time_building=primary_date.class_building,
            time_room_number=primary_date.class_number
        )
        primary_date_model.save()

        secondary_date_model = None
        if len(course.dates) > 1:
            secondary_date = course.dates[1]
            military_time = secondary_date.get_military_time()
            secondary_date_model = CourseDate(
                time_start=military_time[0],
                time_end=military_time[1],
                time_days=secondary_date.days,
                time_building=secondary_date.class_building,
                time_room_number=secondary_date.class_number
            )
            secondary_date_model.save()

        course_model = Course(
            course_subject=course.subject,
            course_number=course.course_number,
            course_name=course.class_name,
            course_prof_name=course.prof_name,
            course_gur=course.gur,
            course_credits_min=course.credits_min,
            course_credits_max=course.credits_max,
            course_fee=course.fee,
            course_restrictions=course.restrictions,
            course_prereq=course.prereq,
            course_additional_info=course.additional_info,
            course_crn=course.crn,
            primary_course_date=primary_date_model,
            secondary_course_date=secondary_date_model,
        )
        course_model.save()
        term.courses.add(course_model)
    term.save()

if __name__ == '__main__':
    main()
