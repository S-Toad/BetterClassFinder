import copy
from django.http import JsonResponse
from django.db.models import Q
from BetterClassFinder.models import Term
from BetterClassFinder.models import Course
from BetterClassFinder.models import CourseDate

def get_courses(request):
    """ Returns a JSON of all courses found in a query"""
    parameter_dictionary = generate_param_dict(request)
    list_of_courses = []

    if not parameter_dictionary:
        # pylint: disable=E1101
        list_of_courses = []
    else:
        query_set = None

        if parameter_dictionary['c_term']:
            query_set = Term.objects
            query_set = generate_query_set(
                parameter_dictionary['c_term'],
                'name__iexact', query_set)

            # TODO: This is gross because of the weird relationship between term
            # and courses. This query wont ever return more than 1 term, but it
            # shouldn't need to be told that.
            query_set = query_set[0].courses
        else:
            query_set = Course.objects

        query_set = generate_query_set(
            parameter_dictionary['c_subj'],
            'course_subject__iexact', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_num'],
            'course_number__iexact', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_name'],
            'course_name__icontains', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_prof'],
            'course_prof_name__icontains', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_gur'],
            'course_gur__icontains', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_restrict'],
            'course_restrictions__icontains', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_prereq'],
            'course_prereq__icontains', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_info'],
            'course_additional_info__icontains', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_crn'],
            'course_crn__exact', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_ptime_days'],
            'primary_course_date__iexact', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_ptime_start'],
            'primary_course_date__time_start__gte', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_ptime_end'],
            'primary_course_date__time_end__lte', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_ptime_building'],
            'primary_course_date__icontains', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_ptime_nroom'],
            'primary_course_date__iexact', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_stime_days'],
            'secondary_course_date__iexact', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_stime_start'],
            'secondary_course_date__time_start__gte', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_stime_end'],
            'secondary_course_date__time_end__lte', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_stime_building'],
            'secondary_course_date__icontains', query_set)
        query_set = generate_query_set(
            parameter_dictionary['c_stime_nroom'],
            'secondary_course_date__iexact', query_set)

        if parameter_dictionary['c_credit']:
            query_set = generate_query_set(
                parameter_dictionary['c_credit'],
                'course_credits_min__gte', query_set)
            query_set = generate_query_set(
                parameter_dictionary['c_credit'],
                'course_credits_max__lte', query_set)
        else:
            query_set = generate_query_set(
                parameter_dictionary['c_credit_min'],
                'course_credits_min__gte', query_set)
            query_set = generate_query_set(
                parameter_dictionary['c_credit_max'],
                'course_credits_max__lte', query_set)

        if parameter_dictionary['c_fee'] != None:
            fee_query_set = Q(course_fee__iexact='')
            if parameter_dictionary['c_fee']:
                query_set = query_set.exclude(fee_query_set)
            else:
                query_set = query_set.filter(fee_query_set)

        list_of_courses = list(query_set)

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
            "course_term": course.term_set.all()[0].name,  # TODO: This is sloppy, need to do a one-to-one relationship
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
        for course in list_of_courses
    ]

    return JsonResponse(json_response, safe=False)

def generate_query_set(param_values, param, original_query_set):
    """Generates a Query Set Object from 2 strings

    Args:
        * param_values - List | List containing the values of a parameter
        * param - String | Query String containing what we're querying for
        * q - QuerySet | QuerySet Object to be updated against
    Returns:
        QuerySet Object"""
    query_set_object = None
    for param_value in param_values:
        exclude = False
        if '!' in param_value:
            exclude = True
            param_value = param_value.replace('!', '')
        # TODO: Eric thinks this is gross, how to do better?
        eval_string = 'global new_query_object\nnew_query_object = Q({!s}={!r})'.format(
            param,
            param_value)
        exec(eval_string)

        if exclude:
            # pylint: disable=E0602
            original_query_set = original_query_set.exclude(new_query_object)
        elif query_set_object is None:
            # pylint: disable=E0602
            query_set_object = new_query_object
        else:
            # pylint: disable=E0602
            query_set_object = query_set_object | new_query_object

    if query_set_object:
        return original_query_set.filter(query_set_object)
    return original_query_set

def generate_param_dict(request):
    """Interprets a meta query string into a dictionary

    Args:
        Meta Query String
    Returns:
        Dictionary"""

    if request.GET == {}:
        return None

    default_dict = {
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
        'c_term': [],
    }

    for key in default_dict:
        get_value = request.GET.get(key)
        if get_value:
            if key == 'c_fee':
                default_dict[key] = get_value.lower() == 'true'
            else:
                default_dict[key] = get_value.split(',')
    return default_dict
