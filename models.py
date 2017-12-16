from django.db import models

class CourseDate(models.Model):
    time_start = models.CharField(max_length=8)
    time_end = models.CharField(max_length=8)
    time_start_period = models.CharField(max_length=4)
    time_end_period = models.CharField(max_length=4)
    time_days = models.CharField(max_length=8)
    time_building = models.CharField(max_length=8)
    time_room_number = models.CharField(max_length=8)

# Create your models here.
class Course(models.Model):
    course_subject = models.CharField(max_length=8)
    course_number = models.CharField(max_length=8)
    course_name = models.CharField(max_length=128)
    course_prof_name = models.CharField(max_length=128)
    course_gur = models.CharField(max_length=32)
    course_credits = models.CharField(max_length=8)
    course_fee = models.CharField(max_length=32, blank=True)
    course_restrictions = models.CharField(max_length=512, blank=True)
    course_prereq = models.CharField(max_length=512, blank=True)
    course_additional_info = models.CharField(max_length=512, blank=True)

    course_dates = models.ManyToManyField(CourseDate)

class Term(models.Model):
    name = models.CharField(max_length=16)
    courses = models.ManyToManyField(Course)
