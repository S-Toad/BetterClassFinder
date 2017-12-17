from django.http import JsonResponse
from BetterClassFinder.models import Term, Course, CourseDate
from django.db.models import Q

def get_courses(request):    
    paramDict = generateDictionary(request.META['QUERY_STRING'])
    
    listOfQObjects = []
    listOfQObjects.append(generateQSubject(paramDict))
    listOfQObjects.append(generateQNum(paramDict))
    listOfQObjects.append(generateQName(paramDict))
    listOfQObjects.append(generateQProf(paramDict))
    listOfQObjects.append(generateQGUR(paramDict))
    # qCreditObject = generateQCredit(paramDict)
    # qFeeObject
    listOfQObjects.append(generateQRestriction(paramDict))
    listOfQObjects.append(generateQPrereq(paramDict))
    listOfQObjects.append(generateQAdditionalInfo(paramDict))
    listOfQObjects.append(generateQCRN(paramDict))
    
    qObjectCombine = None
    
    for qObject in listOfQObjects:
        if qObject == None:
            continue
        elif qObjectCombine == None:
            qObjectCombine = qObject
            continue
        qObjectCombine = qObjectCombine & qObject
    
    courses = Course.objects.all() if qObjectCombine == None else Course.objects.filter(qObjectCombine)
    
    
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

def generateQSubject(paramDict):
    qSubjObject = None
    for subject in paramDict['c_subj']:
        newQSubjObject = Q(course_subject__iexact=subject)
        if (qSubjObject == None):
            qSubjObject = newQSubjObject
            continue
        qSubjObject = qSubjObject | newQSubjObject

    return qSubjObject

def generateQNum(paramDict):
    qNumObject = None
    for number in paramDict['c_num']:
        newQNumObject = Q(course_number__iexact=number)
        if (qNumObject == None):
            qNumObject = newQNumObject
            continue
        qNumObject = qNumObject | newQNumObject

    return qNumObject

def generateQName(paramDict):
    qNameObject = None
    for name in paramDict['c_name']:
        newQNameObject = Q(course_name__icontains=name)
        if (qNameObject == None):
            qNameObject = newQNameObject
            continue
        qNameObject = qNameObject | newQNameObject

    return qNameObject

def generateQProf(paramDict):
    qProfObject = None
    for prof in paramDict['c_prof']:
        newQProfObject = Q(course_prof_name__icontains=prof)
        if (qProfObject == None):
            qProfObject = newQProfObject
            continue
        qProfObject = qProfObject | newQProfObject

    return qProfObject

def generateQGUR(paramDict):
    qGURObject = None
    for gur in paramDict['c_gur']:
        newQGURObject = Q(course_gur__icontains=gur)
        if (qGURObject == None):
            qGURObject = newQGURObject
            continue
        qGURObject = qGURObject | newQGURObject

    return qGURObject

def generateQRestriction(paramDict):
    qRestrictionObject = None
    for restriction in paramDict['c_restrict']:
        newQRestrictionObject = Q(course_restrictions__icontains=restriction)
        if (qRestrictionObject == None):
            qRestrictionObject = newQRestrictionObject
            continue
        qRestrictionObject = qRestrictionObject | newQRestrictionObject

    return qRestrictionObject

def generateQPrereq(paramDict):
    qPrereqObject = None
    for prereq in paramDict['c_prereq']:
        newQPrereqObject = Q(course_prereq__icontains=prereq)
        if (qPrereqObject == None):
            qPrereqObject = newQPrereqObject
            continue
        qPrereqObject = qPrereqObject | newQPrereqObject

    return qPrereqObject
    
def generateQAdditionalInfo(paramDict):
    qAdditionalInfoObject = None
    for additional_info in paramDict['c_info']:
        newQAdditionalInfoObject = Q(course_additional_info__icontains=additional_info)
        if (qAdditionalInfoObject == None):
            qAdditionalInfoObject = newQAdditionalInfoObject
            continue
        qAdditionalInfoObject = qAdditionalInfoObject | newQAdditionalInfoObject

    return qAdditionalInfoObject

def generateQCRN(paramDict):
    qCRNObject = None
    for crn in paramDict['c_crn']:
        newQCRNObject = Q(course_crn__exact=crn)
        if (qCRNObject == None):
            qCRNObject = newQCRNObject
            continue
        qCRNObject = qCRNObject | newQCRNObject

    return qCRNObject
    
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
