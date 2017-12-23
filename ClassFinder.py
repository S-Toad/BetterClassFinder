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
    
    call('python3 ../manage.py migrate BetterClassFinder zero', shell=True)
    call('python3 ../manage.py makemigrations BetterClassFinder', shell=True)
    call('python3 ../manage.py migrate BetterClassFinder', shell=True)
    
    databaseFetcher = DatabaseFetcher(
        term=WINTER_TERM_2018,
        subjects=['MATH'],
    )
    
    courseList = databaseFetcher.query()
    
    term = Term(name="Winter 2018")
    term.save()
    for course in courseList:
        primaryDate = course.dates[0]
        militaryTime = primaryDate.getMilitaryTime()
        primaryDateModel = CourseDate(
            time_start = militaryTime[0],
            time_end = militaryTime[1],
            time_days = primaryDate.days,
            time_building = primaryDate.classBuilding,
            time_room_number = primaryDate.classNumber
        )
        primaryDateModel.save()

        secondaryDateModel = None
        if len(course.dates) > 1:
            secondaryDate = course.dates[1]
            militaryTime = secondaryDate.getMilitaryTime()
            secondaryDateModel = CourseDate(
                time_start = militaryTime[0],
                time_end = militaryTime[1],
                time_days = secondaryDate.days,
                time_building = secondaryDate.classBuilding,
                time_room_number = secondaryDate.classNumber
            )
            secondaryDateModel.save()
        
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
            course_additional_info = course.additionalInfo,
            course_crn = course.crn,
            primary_course_date = primaryDateModel,
            secondary_course_date = secondaryDateModel,
        )
        courseModel.save()
        term.courses.add(courseModel)
    
    term.save()

if __name__ == '__main__':
    main()
