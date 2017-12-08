from DatabaseFetcher import DatabaseFetcher
from TimeRange import TimeRange

def main():
    WINTER_TERM_2018 = '201810'
    SPRING_TERM_2018 = '201820'
    
    databaseFetcher = DatabaseFetcher(
        term=WINTER_TERM_2018,
        subjects=['MATH'],
        timeRange=TimeRange(0, 'A', 0, 'A'),
    )
    
    databaseFetcher.query()

if __name__ == '__main__':
    main()
