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
    call('python ../manage.py migrate BetterClassFinder zero', shell=True)
    call('python ../manage.py makemigrations BetterClassFinder', shell=True)
    call('python ../manage.py migrate BetterClassFinder', shell=True)

    list_of_terms = [
        ('WINTER_2018', '201810'),
        ('SPRING_2018', '201820'),
    ]

    for term_tuple in list_of_terms:
        database_fetcher = DatabaseFetcher(
            term=term_tuple[1],
        )

        course_list = database_fetcher.query()

        term = Term(name=term_tuple[0])
        term.save()

        amount_of_courses = len(course_list)
        current_course = 1
        for course in course_list:
            print('{}/{} courses saved to database for term {}.'.format(
                current_course, amount_of_courses, term_tuple[0]))
            current_course += 1

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
