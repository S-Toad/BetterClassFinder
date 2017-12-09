from DatabaseFetcher import DatabaseFetcher
from TimeRange import TimeRange

def main():
    WINTER_TERM_2018 = '201810'
    SPRING_TERM_2018 = '201820'
    
    databaseFetcher = DatabaseFetcher(
        term=WINTER_TERM_2018,
        timeRange=TimeRange(11, 'A', 2, 'P'),
        subjects=['MATH']
    )
    
    databaseFetcher.query()

if __name__ == '__main__':
    main()
