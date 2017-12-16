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
    
    databaseFetcher = DatabaseFetcher(
        term=WINTER_TERM_2018,
    )
    
    courseList = databaseFetcher.query()
    
    term = Term(name="Winter 2018")
    term.save()
    for course in courseList:
        courseModel = Course(
            course_subject = course.subject,
            course_number = course.courseNumber,
            course_name = course.className,
            course_prof_name = course.profName,
            course_gur = course.gur,
            course_credits = course.credits,
            course_fee = course.fee,
            course_restrictions = course.restrictions,
            course_prereq = course.prereq,
            course_additional_info = course.additionalInfo
        )
        
        courseModel.save()
        
        for date in course.dates:
            dateModel = CourseDate(
                time_start = date.timeStart,
                time_end = date.timeEnd,
                time_start_period = date.timeStartPeriod,
                time_end_period = date.timeEndPeriod,
                time_days = date.days,
                time_building = date.classBuilding,
                time_room_number = date.classNumber
            )
            dateModel.save()
            courseModel.course_dates.add(dateModel)
            
        courseModel.save()
        term.courses.add(courseModel)
    
    term.save()

if __name__ == '__main__':
    main()
