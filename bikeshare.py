import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?').lower()
        try:
            if city not in CITY_DATA.keys():
                print('\nSorry, {} is not a valid city.'.format(city))
            else:
                break
        except ValueError as error:
            print('Exception occurred: {}'.format(error))


    while True:
        want_date = input('Would you like to filter by month, day, both, or not at all? Type "none" for no time filter.').lower()
        try:
            if want_date not in ['month', 'day', 'both', 'none']:
                print('\nSorry, that input didn\'t seem right.')
            else:
                break
        except ValueError as error:
            print('Exception occurred: {}:'.format(error))
    
    if want_date in ['month', 'both']:
        while True:
            month = input("What month would you like to see the data for?").title()
            try:
                if month not in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
                    print('\nSorry, {} is not a month'.format(month))
                else:
                    break
            except ValueError as error:
                print('Exception occurred: {}'.format(error))
    else:
        month = 0

            
    if want_date in ['day', 'both']:
        while True:
            day = input("What day of the week would you like to see the data for?").title()
            try:
                if day not in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
                    print('\nSorry, {} is not a day of the week.'.format(day))
                else:
                    break
            except ValueError as error:
                print('Exception occurred: {}'.format(error))
    else:
        day = 0

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour
    
    if month == 0:
        month = 0
    else:
        month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'].index(month) + 1

    if month != 0 and day != 0:
        df = df[(df['Month'] == month) & (df['Day of Week'] == day)].reset_index()
    elif month != 0 and day == 0:
        df = df[df['Month'] == month].reset_index()
    elif month == 0 and day != 0:
        df = df[df['Day of Week'] == day].reset_index()
    else:
        df = df

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    popular_month = df['Month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    popular_month = months[popular_month - 1]

    popular_day = df['Day of Week'].mode()[0]

    popular_hour = df['Hour'].mode()[0]

    print('The most popular month to travel was {}.'.format(popular_month))
    print('The most popular day of the week to travel was {}.'.format(popular_day))
    print('The most common start hour was {}.'.format(popular_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_stations = {}
    for station in df['Start Station']:
        if station in start_stations.keys():
            start_stations[station] += 1
        else:
            start_stations[station] = 1
    
    popular_start_station = [station for station in start_stations.keys() if start_stations[station] == max(start_stations.values())][0]


    end_stations = {}
    for station in df['End Station']:
        if station in end_stations.keys():
            end_stations[station] += 1
        else:
            end_stations[station] = 1
    
    popular_end_station = [station for station in end_stations.keys() if end_stations[station] == max(end_stations.values())][0]

    popular_trip = df.loc[:, ['Start Station', 'End Station']].mode()
    start_trip = popular_trip.iloc[0][0]
    end_trip = popular_trip.iloc[0][1]

    print('The most commonly used start station was {}.'.format(popular_start_station))
    print('The most commonly used end station was {}'.format(popular_end_station))
    print('The most common trip was {} to {}'.format(start_trip, end_trip))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Travel Time'] = df['End Time'] - df['Start Time']
    total_travel = df['Travel Time'].sum()


    mean_travel = df['Travel Time'].mean()

    
    print('The total travel time for all trips was {}.'.format(total_travel))
    print('The mean trip travel time was {}'.format(mean_travel))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    def col_counts(col_name):
        counts = {}
        for item in df[col_name]:
            if item in counts.keys():
                counts[item] += 1
            else:
                counts[item] = 1
        return counts
        
    print('User types: {}'.format(col_counts('User Type')))

    if 'Gender' not in df.columns:
        print('\nSorry, this bikeshare data does not include gender.')
    else:
        print('\nGender: {}'.format(col_counts('Gender')))

    if 'Birth Year' not in df.columns:
        print('\nSorry, this bikeshare data does not include birth year.')
    else:
        earliest_birth = int(df['Birth Year'].min())
        latest_birth = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode())

        print('Earliest birth year: {}.'.format(earliest_birth))
        print('Most recent birth year: {}.'.format(latest_birth))
        print('Most common year of birth: {}.'.format(common_birth))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def raw_data(df):
    """Displays raw data upon based upon how many rows the user inputs."""
    
    try:
        want_data = input('Would you like to see 5 rows of raw data? Please enter Y or N.').lower()
        while True:
            if want_data not in ['y', 'n']:
                print('I\'m sorry, that\'s not an acceptable input.')
            else:
                break
    except ValueError as error:
        print('Exception occurred: {}'.format(error))
        
        
    if want_data == 'y':
        x = 0
        y = 5
        print(df.iloc[x:y])
        
        want_more = 'y'
        while want_more == 'y':
            want_more = 'y'
            while True:
                try:
                    want_more = input('Would you like to see 5 more rows of data? Please enter Y or N.').lower()
                    if want_more not in ['y', 'n']:
                        print('I\'m sorry, that\'s not an acceptable input.')
                    else:
                        break
                except ValueError as error:
                    print('Exception occurred: {}'.format(error))

            if want_more == 'y':
                x += 5
                y += 5
                print(df.iloc[x:y])
        
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
