import time
import pandas as pd
# import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }
# used for error checking
MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'None')
DAYS = ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday', 'None')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!\n')
    
    # get user input for city (chicago, new york city, washington). 
    city = input('\nWould you like to see data for Chicago, New York, or Washington.\n').title()

    # get  filter requirements
    filter = input('\nWould you like to filter by month, day, both or not at all? Type "none" for no time filter\n' ).title()
    
    # assign the variables based on the filter selection. If the user input is not found. the value 'err' gets assigned to day and month
    # The error will get processed in main()
    if filter == 'Month':
           month = input('\nWhich month would you like to see data for? January, February, March, April, May, or June?\n').title()
           day = 'None'
    elif filter == 'Day':
           day = input('\nWhich day would you like to filter by?\nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n').title()
           month = 'None'
    elif filter == 'Both':
           month = input('\nWhich month would you like to see data for? January, February, March, April, May, or June?\n').title()
           day = input('\nWhich day would you like to filter by?\n Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday \n').title()
    elif filter == 'None':
           day = 'None'
           month = 'None'
    else :
            day = 'err'
            month = 'err'


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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] =  pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'None':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'None':
        # filter by day of week to create the new dataframe
        df = df[day.title() == df['day_of_week']]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most Common Month: ', MONTHS[most_common_month - 1])

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most Common Day Of Week: ', most_common_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour: ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_sta = df['Start Station'].mode()[0]
    print('Most Common Start Station: ', most_common_start_sta)

    # display most commonly used end station
    most_common_end_sta = df['End Station'].mode()[0]
    print('Most Common End Station: ', most_common_end_sta)

    # display most frequent combination of start station and end station trip
    df['Start Stop Combination'] = df['Start Station'] + " --->  " + df['End Station']
    most_common_combination =  df['Start Stop Combination'].mode()[0]
    print('Most Common Start Stop Combo: ', most_common_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Trip Durations: ', df['Trip Duration'].sum())


    # display mean travel time
    print('Average Trip Durations: ', df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nUser types:\n", df['User Type'].value_counts())

    if city != 'Washington':
        # Display counts of gender
        print("\nGender Types:\n", df['Gender'].value_counts())
        # Display earliest, most recent, and most common year of birth
        print("\nEarliest Birth Year: \n", df['Birth Year'].min())
        print("\nMost Recent  Birth Year: \n", df['Birth Year'].max())
        print("\nMost Common  Birth Year: \n", df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def validate_entry(city, month, day) :
    """Validates user input which was acquired in the get_filters() method"""

    passed_test = True

    if city.title() not in CITY_DATA :
            print('Looks like your filter for city is not available\n\n')
            passed_test = False
    if month not in MONTHS  or month == 'err':
            print('Looks like your filter for month is not available\n\n')
            passed_test = False
    if day not in DAYS or day == 'err':
            print('Looks like your filter for day is not available\n\n')
            passed_test = False
    
    return passed_test

def main():
    while True:
        city, month, day = get_filters()

        if validate_entry(city, month, day) == False :
            print('************* Resetting User Entry ***********************')
            continue

        print('Applying the following filters: city = ', city.upper(), ' month = ', month.upper(), ' day = ', day.upper(),'\n')
        print('-'*40)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        raw_data = input('Would you like to see the raw data? Enter yes or no.\n')
        if raw_data.title() == 'Yes':
           print(df.head())

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.title() != 'Yes':
            break


if __name__ == "__main__":
	main()
