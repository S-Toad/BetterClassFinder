from django.http import JsonResponse
from BetterClassFinder.models import Term, Course, CourseDate
from django.db.models import Q
import copy

def get_courses(request):    
    paramDicts = generateDictionary(request.META['QUERY_STRING'])
    listOfCourses = []
    
    if (not paramDicts):
        listOfCourses = Course.objects.all()
    else:
        for paramDict in paramDicts:
            q = Course.objects
            q = generateQObject(paramDict['c_subj'], 'course_subject__iexact', q)
            q = generateQObject(paramDict['c_num'], 'course_number__iexact', q)
            q = generateQObject(paramDict['c_name'], 'course_name__icontains', q)
            q = generateQObject(paramDict['c_prof'], 'course_prof_name__icontains', q)
            q = generateQObject(paramDict['c_gur'], 'course_gur__icontains', q)
            q = generateQObject(paramDict['c_restrict'], 'course_restrictions__icontains', q)
            q = generateQObject(paramDict['c_prereq'], 'course_prereq__icontains', q)
            q = generateQObject(paramDict['c_info'], 'course_additional_info__icontains', q)
            q = generateQObject(paramDict['c_crn'], 'course_crn__exact', q)
            
            courses = list(q)
            listOfCourses.extend(courses)
    
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
        for course in listOfCourses
    ]

    return JsonResponse(json_response, safe=False)
    
def generateQObject(values, param, q):
    qObject = None
    i = 1
    for value in values:
        exclude = False
        if '!' in value:
            exclude = True
            value = value.replace('!', '')
        # TODO: Eric thinks this is gross, how to do better?
        evalString = 'global qNewObject\nqNewObject = Q({!s}={!r})'.format(param, value)
        exec(evalString)
        
        if exclude:
            q = q.exclude(qNewObject)
        elif qObject == None:
            qObject = qNewObject
        else:
            qObject = qObject | qNewObject
      
    if (qObject != None):
        return q.filter(qObject)
    else:
        return q
    
def generateDictionary(queryString):
    defaultDict = {
        'c_subj': [],
        'c_num': [],
        'c_name': [],
        'c_prof': [],
        'c_gur': [],
        'c_credit_min': None,
        'c_credit_max': None,
        'c_credit': None,
        'c_fee': True,
        'c_restrict': [],
        'c_prereq': [],
        'c_info': [],
        'c_crn': [],
        'c_time_days': [],
        'c_time_start': [],
        'c_time_end': [],
        'c_time_building': [],
        'c_time_nroom': [],
        'c_ptime_days': [],
        'c_ptime_start': [],
        'c_ptime_end': [],
        'c_ptime_building': [],
        'c_ptime_nroom': [],
        'c_stime_days': [],
        'c_stime_start': [],
        'c_stime_end': [],
        'c_stime_building': [],
        'c_stime_nroom': [],
    }
    
    if (queryString == ''):
        return None
    
    listOfQueryStrings = []
    for query in queryString.split('&'):
        listOfQueryStrings.append(query)
    if not listOfQueryStrings:
        listOfQueryStrings.append(queryString)
    
    listOfParams = []
    for query in listOfQueryStrings:
        emptyList = []
        for paramValue in query.split('?'):
            emptyList.append(paramValue.split('='))
        listOfParams.append(emptyList)
    
    listOfDict = []
    for listOfParam in listOfParams:
        copyDict = copy.deepcopy(defaultDict)
        for param in listOfParam:
            if param[0] in copyDict:
                if type(copyDict[param[0]]) is list:
                    copyDict[param[0]].append(param[1])
                else:
                    copyDict[param[0]] = param[1]
        listOfDict.append(copyDict)
    return listOfDict
