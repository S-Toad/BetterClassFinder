from django.http import JsonResponse
from BetterClassFinder.models import Term, Course, CourseDate
from django.db.models import Q

def get_courses(request):    
    paramDict = generateDictionary(request.META['QUERY_STRING'])
    
    listOfQObjects = []
    listOfQObjects.append(generateQObject(paramDict['c_subj'], True, 'course_subject__iexact'))
    listOfQObjects.append(generateQObject(paramDict['c_num'], True, 'course_number__iexact'))
    listOfQObjects.append(generateQObject(paramDict['c_name'], True, 'course_name__icontains'))
    listOfQObjects.append(generateQObject(paramDict['c_prof'], True, 'course_prof_name__icontains'))
    listOfQObjects.append(generateQObject(paramDict['c_gur'], True, 'course_gur__icontains'))
    listOfQObjects.append(generateQObject(paramDict['c_restrict'], True, 'course_restrictions__icontains'))
    listOfQObjects.append(generateQObject(paramDict['c_prereq'], True, 'course_prereq__icontains'))
    listOfQObjects.append(generateQObject(paramDict['c_info'], True, 'course_additional_info__icontains'))
    listOfQObjects.append(generateQObject(paramDict['c_crn'], True, 'course_crn__exact'))
    listOfQObjects = filter(None, listOfQObjects)
    
    qObjectCombine = None
    for qObject in listOfQObjects:
        qObjectCombine = qObject if qObjectCombine == None else qObjectCombine & qObject
    
    coursesRaw = Course.objects.all() if qObjectCombine == None else Course.objects.filter(qObjectCombine)
    coursesList = list(coursesRaw)
    
    courses = []
    
    datesQuery = paramDict['c_date']
    if (len(datesQuery) == 0):
        courses = coursesList
    else:
        for course in coursesList:
            courseDates = course.getDates()
            for date in datesQuery:
                if (courseDates == date):
                    courses.append(course)
                    break
    
    json_response = [
        {
            "course_subject": course.course_subject,
            "course_number": course.course_number,
            "course_name": course.course_name,
            "course_prof_name": course.course_prof_name,
            "course_gur": course.course_gur,
            "course_credits": course.course_credits,
            "course_fee": course.course_fee,
            "course_restrictions": course.course_restrictions,
            "course_prereq": course.course_prereq,
            "course_additional_info": course.course_additional_info,
            "course_crn": course.course_crn,
            "course_dates": [
                {
                    "time_start": courseDate.time_start,
                    "time_start_period": courseDate.time_start_period,
                    "time_end": courseDate.time_end,
                    "time_end_period": courseDate.time_end_period,
                    "time_days": courseDate.time_days,
                    "time_building": courseDate.time_building,
                    "time_room_number": courseDate.time_room_number,
                }
                for courseDate in course.course_dates.all()
            ]
        }
        for course in courses
    ]

    return JsonResponse(json_response, safe=False)
    
def generateQObject(values, combineByOr, param):
    qObject = None
    
    for value in values:
        evalString = 'global qNewObject\nqNewObject = Q({!s}={!r})'.format(param, value)
        exec(evalString)
        if qObject == None:
            qObject = qNewObject
        elif combineByOr:
            qObject = qObject | qNewObject
        else:
            qObject = qObject & qNewObject
    
    return qObject
    
def generateDictionary(queryString):
    defaultDict = {
        'c_subj': [],
        'c_num': [],
        'c_name': [],
        'c_prof': [],
        'c_gur': [],
        'c_credit_low': '',
        'c_credit_high': '',
        'c_credit': '',
        'c_flat': True,
        'c_fee_per_credit': True,
        'c_fee_max': 9999,
        'c_restrict': [],
        'c_prereq': [],
        'c_info': [],
        'c_crn': [],
        'c_date': [],
    }
    
    listOfParams = []
    
    for value in queryString.split('?'):
        listOfParams.append(value.split('='))
    
    for listParam in listOfParams:
        if listParam[0] in defaultDict:
            if type(defaultDict[listParam[0]]) is list:
                defaultDict[listParam[0]].append(listParam[1])
                print("Appending " + listParam[1] + " to list with key " + listParam[0])
            else:
                defaultDict[listParam[0]] = listParam[1]
                print("Assigning " + listParam[1] + " with key " + listParam[0])
    
    return defaultDict
