from django.db import models

class CourseDate(models.Model):
    """
    Contains:
        * time_start - Int value in military time of when a class starts
        * time_end - Int value in military time of when a class ends
        * time_days - String contai
    """
    time_start = models.IntegerField()
    time_end = models.IntegerField()
    time_days = models.CharField(max_length=8)
    time_building = models.CharField(max_length=8)
    time_room_number = models.CharField(max_length=8)

# Create your models here.
class Course(models.Model):
    """Course Model

    Contains:
        * course_subject - String | Name of the course's subject, 8 character max
        * course_number - String | Value of the course's "number" which can contain characters,
            8 characters max
        * course_name - String | Courses full name, 128 characters max
        * course_gur - String | Contains the relevant GURs a course may have
            seperated by spaces, 128 characters max
        * course_credits_min - Float | Contains the lower end amount of credits a class is worth
        * course_credits_max - Float | Contains the upper end amount of credits a class is worth
        * course_fee - String | Contains data about how much additional cost a course is
        * course_restrictiins - String | Contains data on what a course may be restricted by,
            can be blank
        * course_prereq - String | Contains data on what a course prerequistes may be,
            can be blank
        * course_additional_info - String | Contains data on additional info on a course,
            such as out of class lab time, can be blank
        * course_crn - String | A courses CRN
        * primary_course_date - CourseDate | A CourseDate model which contains the main times
            a class is
        * secondary_course_date - CourseDate | A CourseDate model which contains the
            lab times of a class, can be null"""


    course_subject = models.CharField(max_length=8)
    course_number = models.CharField(max_length=8)
    course_name = models.CharField(max_length=128)
    course_prof_name = models.CharField(max_length=128)
    course_gur = models.CharField(max_length=32)
    course_credits_min = models.FloatField()
    course_credits_max = models.FloatField()
    course_fee = models.CharField(max_length=32, blank=True)
    course_restrictions = models.CharField(max_length=512, blank=True)
    course_prereq = models.CharField(max_length=512, blank=True)
    course_additional_info = models.CharField(max_length=512, blank=True)
    course_crn = models.CharField(max_length=8)

    primary_course_date = models.OneToOneField(
        CourseDate,
        on_delete=models.CASCADE,
        related_name='primary_course_date',
    )

    secondary_course_date = models.OneToOneField(
        CourseDate,
        on_delete=models.CASCADE,
        related_name='secondary_course_date',
        null=True,
    )

class Term(models.Model):
    """Term Model.

    Contains:
        * Name (Ex:"Winter 2018")
        * Courses - ManyToMany Relationship with Course Model"""
    name = models.CharField(max_length=16)
    courses = models.ManyToManyField(Course)
