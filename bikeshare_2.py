import time
import pandas as pd
import numpy as np
import calendar as ca # will be used to make month from a number to a name 

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
    # get user input for city (chicago, new york city, washington).
    while True:
         city= input("Would you like to see data for Chicago, New York City, or Washington? ").lower()# get the user input in iowr case by .lower()
         city_name = ['chicago', 'new york city', 'washington']
         if city not in city_name:
            print("Invalid city. Please enter Chicago, New York City, or Washington.")
         else:
              break
        

    # get user input for month (all, january, february, ... , june)
    while True:
         month = input("Which month? January, February, March, April, May, June, or All? ").lower() # get the user input in iowr case by .lower()
         months = "all"
         month_name = ["january", "february", "march", "april", "may", "june"]
         if month not in months and month not in month_name:
            print("Invalid month. Enter a month or All to display all months (January, February, March, April, May, June):")
         else:
              break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter a day or All to display all days of the week: ").lower()# get the user input in iowr case by .lower()
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        week = "all"
        if day not in days and day not in week:
            print("Invalid day. Enter a day or All to display all week (monday, tuesday, wednesday, thursday, friday, saturday,sunday. ):")
           
        else:
             break

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
    # load data to dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # creat new colume for mmonth and day from start time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month 
    if month != 'all':
       # if not all we convort the month name to numbers , +1 because index start from 0
       month_name = ["january", "february", "march", "april", "may", "june"]
       month = month_name.index(month) + 1
       # filter by month
       df = df[df['month'] == month]
    # filter by day of week
    if day != 'all':
       df = df[df['day_of_week'] == day.title()] # title to capitalized the first letter 

    return df

def raw_data(df):
    """
    displaying raw data depending on the user reply
    """
    n = 0
    reply = input('do you want to display the data in the first 5 rows ? yes/no: ' ).lower() # get the user input in iowr case by .lower()
    pd.set_option("display.max_rows", None) # make the display rows to max.

    while True:
          if reply == 'no':
               break
          print(df[n:n+5]) # display next 5 rows
          reply = input('do you wnat to display more 5 rows of data? yes/no: ').lower() # get the user input in iowr case by .lower()
          n += 5
   
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0] # get month number
    print("Most Common Month: ", ca.month_name[common_month]) # convert monthe number to a month name

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("Most Common Day: ", common_day)

    # display the most common start hour
    df["hour"] = df["Start Time"].dt.hour # get hour from start time.
    common_hour = df["hour"].mode()[0]
    print("Most Common Start Hour:", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("Most Common Used Start Station : ", common_start)


    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("Most Common Used End Station : ", common_end)


    # display most frequent combination of start station and end station trip
    common_end_start = (df['Start Station'] + ' - ' + df['End Station']).mode()[0] # combining start and end station to get the most freequnt with .mod().
    print("Most Frequent Combination of Start Station and End Station Trip: ", common_end_start)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print("Total Travel Time:", travel_time/3600, "Hours")



    # display mean travel time
    avg_time = df['Trip Duration'].mean()
    print("Average Travel Time:", avg_time/3600, "Hours")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of User Types:\n", df['User Type'].value_counts())



    # Display counts of gender
    if 'Gender' in df:
       print("\nCounts of Gender:\n", df['Gender'].value_counts())


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df: # use this condition because washington data does not have a birth year.
       earliest_birth = int(df['Birth Year'].min())
       print("\nEarliest Year of Birth:\n", earliest_birth)
       recent_birth = int(df['Birth Year'].max())
       print("\nRecent Year of Birth:\n", recent_birth)
       common_birth = int(df['Birth Year'].mode())
       print("\nCommon Year of Birth:\n", common_birth)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
