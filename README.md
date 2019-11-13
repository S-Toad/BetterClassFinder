# Better Classfinder

TODO: General details should go here 

## Files of Interest

### [DatabaseFetcher.py](https://github.com/S-Toad/BetterClassFinder/blob/master/util/DatabaseFetcher.py)
Handles scraping of the classfinder database. Utilized by our [main class](https://github.com/S-Toad/BetterClassFinder/blob/master/ClassFinder.py) directly to gather information about each term.

### [api.py](https://github.com/S-Toad/BetterClassFinder/blob/master/api.py)
Handles the API of this project utilizing Django's database models.


## API Documentation
The API for Better Classfinder is very powerful and the main website for Better Classfinder won't utilize all these features! The API for Better Classfinder contains data for all courses and given POST params, can filter this data for you.

## JSON Result

    [  
        {  
            "course_subject":"MATH",
            "course_number":"124",
            "course_name":"Calculus & Analytic Geometry I",
            "course_prof_name":"Ryan, Connor Keith",
            "course_gur":"QSR ",
            "course_credits_min":5.0,
            "course_credits_max":5.0,
            "course_fee":"",
            "course_restrictions":"",
            "course_prereq":"MATH 115 or MATH 118 with a C- or better or a grade of 2.5 or higher in a culminating college precalculus course or suitable math assessment score.",
            "course_additional_info":"",
            "course_crn":"20016",
            "course_term":"SPRING_2018",
            "primary_date":[  
                {  
                    "time_start":800,
                    "time_end":850,
                    "time_days":"MTWRF",
                    "time_building":"BH",
                    "time_room_number":"225"
                }
            ],
            "secondary_date":[]
        },
        {
            # Additional course
        },
        ...
    ]

## GET Params
#### Tags
* **O** - Supports multiple variables to be stranded into a OR statement
* **X** - Supports negation of the variable
* **iexact** - Filters DB by the exact value (case insenstive)
* **icontains** - Filters DB by substring (case insenstive)
* **exact** - Filters DB by exact value
* **gte** - Filters DB by 'Greater Than or Equal'
* **lte** Filters DB by 'Less Than or Equal'


#### c_subj (O, X, iexact):
c_subj (Course Subject) is used to filter courses based on its subject.

Example Stored Data: "MATH"

	EX 1) c_subj=MATH # Returns all MATH courses
    EX 2) c_subj=!MATH # Returns all courses excluding MATH
    EX 3) c_subj=MATH,CHEM # Returns all MATH and CHEM courses
	

#### c_num (O, X, iexact):
c_num (Course Number) is used to filter courses based on its  number.

Example Stored Data: "124"

    EX 1) c_num=101 # Returns all 101 courses
	EX 2) c_subj=MATH&c_num=124,125 # Returns all MATH 124 and 125 courses
    EX 3) c_subj=MATH&c_num=!124,!125 # Returns all MATH courses excluding MATH 124 and 125

#### c_name (O, X, icontains):
c_name (Course Name) is used to filter courses based on its name.

Example Stored Data: "Calculus & Analytic Geometry I"

    EX 1) c_name=Calculus # Returns all courses containing 'Calculus' in its name. Would include Precalculus as well
    EX 2) c_name=intro,advanced # Return all courses containing 'intro' OR 'advanced'.
    EX 3) c_name=!intro # Returns all courses not containing the substring into in its name.

#### c_prof (O, X, icontains):
c_prof (Course Professor) is used to filter courses based on its professor. 

Example Stored Data: "Stables, Katie"

**NOTE**: Professor names are stored as `<last_name>, <first_name> <middle_name>'. It's best to filter professors upon their last name. 

    EX 1) c_prof=ragsdale # Returns all courses containing the substring 'ragsdale' in its professor name
    EX 2) c_prof=!ragsdale # Returns all courses not containing the substring 'ragsdale' in its professor name
    EX 3) c_prof=ragsdale,johnson # Returns all courses containing the substring 'ragsdale' OR 'johnson' in its professor name

#### c_gur (O, X, icontains):
c_gur (Course GUR) is used to filter courses based on its GUR.

Example Stored Data: "QSR"

    EX 1) c_gur=acom # Returns courses containing the ACOM attribute
    EX 2) c_gur=acgm,bcgm # Return courses containing the substring 'ACOM' OR 'BCGM' attribute
    EX 3) c_gur=!acgm # Return courses not containing the substring 'ACGM' attribute

#### c_restrict (O, X, icontains):
c_restrict (Course Restrictions) is used to filter courses based on its restriction.

Example Stored Data: "GR MJ GR PB PM BU"

    EX 1) c_restrict=gr # Return courses containing the GR restriction attribute
    EX 2) c_restrict=!mj # Return courses not containing the MJ restriction
    EX 3) c_restrict=!mj,!gr # Return courses not containing the MJ OR GR restriction

#### c_prereq (O, X, icontains):
c_prereq (Course Prerequisites) is used to filter courses based on its prerequisites

**NOTE**: Only takes single words currently

Example Stored Data: "MATH 115 or MATH 118 with a C- or better or a grade of 2.5 or higher in a culminating college precalculus course or suitable math assessment score."

    EX 1) c_prereq=math # Returns courses containing math in its prereq string
    EX 2) c_prereq=math,phys # Returns courses containing math or phys in its prereq string
    EX 3) c_prereq=!math # Return courses not containing math in its prereq string

#### c_info (O, X, icontains):
c_info (Course Information) is used to filter courses based on its additional info. 

**NOTE**: Only takes single words currently

Example Stored Data: "Note: If you have passed the AP Calculus Exam with a minimum score of "3" or have college calcuuls credit, please contact CBE before registering for this class."

    EX 1) c_info=new # Return courses containing new in its additional info

#### c_crn (O, X, iexact):
c_crn (Course CRN) is used to filter courses based on its crn.

Example Stored Data: "10019"

    EX 1) c_crn=10019 # Return courses (A course really) containing 10019 as its crn
    EX 2) c_crn=10019,10020 # Return the two courses with the crns 10019 and 10020
    EX 3) c_crn=!10019 # Returns all courses excluding the course with a crn of 10019

#### c_ptime_days (O, X, iexact):
c_ptime_day (Course Primary Time Days) is used to filter courses based on its primary time days. If a class has a primary time slot and a lab time slot, this will filter based on the primary time slot

Example Stored Data: "MWF"

    EX 1) c_ptime_days=mwf # Returns all courses scheduled on mondays, wednesdays, and fridays
    EX 2) c_ptime_days=!mwf # Return all courses not scheduled primarily on mondays, wednesdays, or fridays
    EX 3) c_ptime_days=mwf,tr # Return all courses scheduled on mondays, wednesdays, and fridays OR scheduled on tuesdays and thursdays. Will not display MTRF or MTWRF classes

#### c_ptime_start (X, gte):
c_ptime_start (Course Primary Time Start) is used to filter courses based on the time it primarily starts on.

Example Stored Data: "1400" (2:00pm)

    EX 1) c_ptime_start=800 # Return all courses that primarily begin past and including 8am
    EX 2) c_ptime_start=!1000 # Return all courses that primarily DONT begin past and including 8am. You should used c_ptime_end instead

#### c_ptime_end (X, lte):
See c_ptime_start 

#### c_ptime_building (O, X, icontains):
c_ptime_building (Course Primary Time Building) is used to filter courses based on which building it primarily is in.

Example Stored Data: "BH"

    EX 1) c_ptime_building=BH # Return all courses taught primarily in Bond Hall
    EX 2) c_ptime_building=BH,AW # Return all courses taught in Academic West OR Bond Hall. 
    EX 3) c_ptime_building=!BH # Return all courses not taught in Bond Hall

#### c_ptime_nroom (O, X, icontains):
c_ptime_nroom (Course Primary Time Room Number) is used to filter courses based on what room number it primarily is taught in.

Example Stored Data "403"

    EX 1) c_ptime_nroom=403 # Return all courses taught in room 403
    EX 2) c_ptime_building=BH&c_ptime_nroom=104 # Return all courses taught in Bond Hall 104
    Ex 3) c_ptime_building=BH&c_ptime_nroom=104,105 # Return all courses taught in Bond Hall 104 OR 105
    Ex 4) c_ptime_nroom=!13 # Return all courses NOT taught in room 13 (Bad luck!)

#### c_stime_days (O, X, iexact):
See c_ptime_days. This is used for secondary class times, such as labs for example.


#### c_stime_start (X, gte):
See c_ptime_start. This is used for secondary class times, such as labs for example.

#### c_ptime_end (X, lte):
See c_ptime_end. This is used for secondary class times, such as labs for example.

#### c_stime_building (O, X, icontains):
See c_ptime_building. This is used for secondary class times, such as labs for example.

#### c_stime_nroom (O, X, icontains):
See c_stime_nroom. This is used for secondary class times, such as labs for example.

#### c_credit_min (X, gte):
c_credit_min (Course Minimum Credits) is used to filter courses based on its credit.

Example Stored Data: "1"

    EX 1) c_credit_min=1 # Return all courses with at least 1 credits

#### c_credit_max (X, lte):
See c_credit_min, used for the upper bound.

#### c_credit (O, X, ltw):
c_credit (Course Credits) overrides c_credit_min and c_credit_max. It filters courses based on its exact credits. Behind the scenes, it essentially does c_credit_min=c_credit_max=c_credit.

    EX 1) c_credit=4 # Return all 4 credit courses
    EX 2) c_credit=4,5 # Return all 4 or 5 credit courses
    EX 3) c_credit=!5 # Return all courses excluding 5 credit courses

#### c_fee (iexact):
c_fee (Course Fee) is used to filter courses based on whether it has a fee associated with it or not. 

    EX 1) c_fee=true # Returns all courses containing some sort of fee
    EX 2) c_fee=false # Returns all courses without any fees

