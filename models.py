from django.db import models

class CourseDate(models.Model):
    time_start = models.IntegerField()
    time_end = models.IntegerField()
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
    name = models.CharField(max_length=16)
    courses = models.ManyToManyField(Course)
