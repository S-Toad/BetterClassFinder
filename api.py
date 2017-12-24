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
            q = generateQObject(paramDict['c_ptime_days'], 'primary_course_date__iexact', q)
            q = generateQObject(paramDict['c_ptime_start'], 'primary_course_date__time_start__gte', q)
            q = generateQObject(paramDict['c_ptime_end'], 'primary_course_date__time_end__lte', q)
            q = generateQObject(paramDict['c_ptime_building'], 'primary_course_date__icontains', q)
            q = generateQObject(paramDict['c_ptime_nroom'], 'primary_course_date__iexact', q)
            q = generateQObject(paramDict['c_stime_days'], 'secondary_course_date__iexact', q)
            q = generateQObject(paramDict['c_stime_start'], 'secondary_course_date__time_start__gte', q)
            q = generateQObject(paramDict['c_stime_end'], 'secondary_course_date__time_end__lte', q)
            q = generateQObject(paramDict['c_stime_building'], 'secondary_course_date__icontains', q)
            q = generateQObject(paramDict['c_stime_nroom'], 'secondary_course_date__iexact', q)
            
            if paramDict['c_credit']:
                print(1)
                q = generateQObject(paramDict['c_credit'], 'course_credits_min__gte', q)
                q = generateQObject(paramDict['c_credit'], 'course_credits_max__lte', q)
            else:
                q = generateQObject(paramDict['c_credit_min'], 'course_credits_min__gte', q)
                q = generateQObject(paramDict['c_credit_max'], 'course_credits_max__lte', q)
            
            if paramDict['c_fee'] != None:
                feeQ = Q(course_fee__iexact='')
                print(paramDict['c_fee'])
                if paramDict['c_fee']:
                    q = q.exclude(feeQ)
                else:
                    q = q.filter(feeQ)

            courses = list(q)
            listOfCourses.extend(courses)
    
    json_response = [
        {
            "course_subject": course.course_subject,
            "course_number": course.course_number,
            "course_name": course.course_name,
            "course_prof_name": course.course_prof_name,
            "course_gur": course.course_gur,
            "course_credits_min": course.course_credits_min,
            "course_credits_max": course.course_credits_max,
            "course_fee": course.course_fee,
            "course_restrictions": course.course_restrictions,
            "course_prereq": course.course_prereq,
            "course_additional_info": course.course_additional_info,
            "course_crn": course.course_crn,
            "primary_date": [
                {
                    "time_start": course.primary_course_date.time_start,
                    "time_end": course.primary_course_date.time_end,
                    "time_days": course.primary_course_date.time_days,
                    "time_building": course.primary_course_date.time_building,
                    "time_room_number": course.primary_course_date.time_room_number,
                }
            ],
            "secondary_date": [
                {
                    "time_start": course.secondary_course_date.time_start,
                    "time_end": course.secondary_course_date.time_end,
                    "time_days": course.secondary_course_date.time_days,
                    "time_building": course.secondary_course_date.time_building,
                    "time_room_number": course.secondary_course_date.time_room_number,
                }
            ] if course.secondary_course_date else [],
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
        'c_credit_min': [],
        'c_credit_max': [],
        'c_credit': [],
        'c_fee': None,
        'c_restrict': [],
        'c_prereq': [],
        'c_info': [],
        'c_crn': [],
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
                elif param[0] == 'c_fee': # Edge casio
                    boolio = param[1].lower() =="true" 
                    copyDict[param[0]] = boolio
                else:
                    copyDict[param[0]] = param[1]
        listOfDict.append(copyDict)
    return listOfDict
