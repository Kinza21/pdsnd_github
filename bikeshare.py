import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():

    """
    Asks user to specify a city, month, and day to filter data and analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day - name of the day of week to filter by, or "none" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    city = ()
    month = ()
    day = ()

    # get user input for city (chicago, new york city, washington).
    city_options = ['chicago', 'washington', 'new york city']

    while city not in city_options:
        city = input('Which city would you like to see the data for? Chicago, New York City or Washington?\n').lower()
        if city not in city_options:
            print('Please choose from Chicago, New York City and Washington!')

    # get user input for month (all, january, february, ... , june)
    month_options = ['None', 'January', 'February', 'March', 'April', 'May', 'June']

    while month not in month_options:
        month = input('Would you like to filter the data by month? Choose from January to June or type None\n').title()
        if month not in month_options:
            print('Please select from January to June only or type None.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_options = ['None', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    while day not in day_options:
        day = input('Select the day of the week to see data. Choose from Monday to Sunday or type None\n').title()
        if day not in day_options:
            print('Please select day from Monday to Saturday.')

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
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['day'] = pd.DatetimeIndex(df['Start Time']).dayofweek

    #filter according to month and day

    if month != 'None':
        month_options = ['None', 'January', 'February', 'March', 'April', 'May', 'June']
        month = month_options.index(month)
        df = df[df['month'] == month]


    if day != 'None':
        day_options = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        day = day_options.index(day)
        df = df[df['day'] == day]

    print(df)

    return df


#Calculating stats
def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month for selected day or no day filter
    if month == 'None':
        months_dict = {'1':'January', '2': 'February', '3': 'March', '4': 'April','5': 'May','6': 'June'}
        comm_month = months_dict[str(df['month'].mode()[0])]
        if day != 'None':
            print('The most common month for travel on {}s is {}. Close chart to continue.'.format(day, comm_month))
        else:
            print('The most common month for travel is {}. Close chart to continue.'.format(comm_month))

        #plot chart
        df['month'].value_counts().plot(kind='pie')
        plt.title('Distribution of Travel by Month')
        plt.show()

    # display the most common day of week for selected month or no month filter
    if day == 'None':
        days_dict = {'0': 'Sunday','1': 'Monday', '2': 'Tuesday', '3': 'Wednesday', '4':'Thursday', '5':'Friday', '6': 'Saturday'}
        comm_day = days_dict[str(df['day'].mode()[0])]
        if month != 'None':
            print('The most common day for travel during the month of {} is {}. Close chart to continue.'.format(month, comm_day))
        else:
            print('The most common day is {}. Close chart to continue.'.format(comm_day))

        #plot chart
        df['day'].value_counts().plot(kind='pie')
        plt.title('Distribution of Travel by Day')
        plt.show()

    # display the most common start hour for selected day and/or month or no filter
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour
    comm_hour = df['hour'].mode()[0]
    print('The most common start hour is {}:00. Close chart to continue.'.format(comm_hour))

    # plot chart
    df['hour'].value_counts().plot(kind='pie')
    plt.title('Distribution of Travel by Starting Hour')
    plt.show()

    print('\nThis took {} seconds.'.format(time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations...\n')
    start_time = time.time()

    # display most commonly used start station
    comm_start_station = df['Start Station'].mode()[0]
    count_start = df.groupby(['Start Station']).size().sort_values(ascending=False)
    print('The most commonly used start station is {}.'.format(comm_start_station), 'Count: ', count_start[0], '\nClose graph to continue.')

    # plot graph
    s=pd.Series(count_start[:20])
    s.plot(kind='bar')
    plt.show()


    # display most commonly used end station
    comm_end_station = df['End Station'].mode()[0]
    count_end = df.groupby(['End Station']).size().sort_values(ascending=False)
    print('The most commonly used end station is {}.'.format(comm_end_station), 'Count: ', count_end[0], '\nClose graph to continue.')

    # plot graph
    s=pd.Series(count_end[:20])
    s.plot(kind='bar')
    plt.show()

    # display most frequent combination of start station and end station trip
    combinations_stations = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    comb_station = combinations_stations.index[0]
    print('The most most frequent combination of start and end station trip is from {} to {}.'.format(comb_station[0], comb_station[1]), 'Count: ', combinations_stations[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    travel_times = df['End Time'] - df['Start Time']
    total_travel_time = travel_times.sum()
    print('The total travel time is {}.'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = travel_times.mean()
    print('The mean travel time is {}.'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count = df['User Type'].value_counts()
    print('User Type Count:\n{}'.format(count), '\n')

    # Display counts of gender
    gen_count = df['Gender'].value_counts()
    print('Gender Count:\n{}'.format(gen_count),'\n')

    # Display earliest, most recent, and most common year of birth
    earliest_dob = int(df['Birth Year'].min())
    recent_dob = int(df['Birth Year'].max())
    comm_dob = int(df['Birth Year'].mode())

    print('The earliest year of birth is {}.'.format(earliest_dob),'\n','The most recent year of birth is {}.'.format(recent_dob),'\n','The most common year of birth is {}.'.format(comm_dob))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def row_data(df):
    """Asks users if they would like to view data for each trip and returns accordingly"""

    start_time = time.time()
    question = input('\nWould you like to see data for the first ten individual trip? Enter yes or no\n')
    if question == 'yes':
        for i in range(0,10):
            print('Trip Number {}:'.format(i+1))
            print(df.iloc[i], '\n')
        print("\nThis took %s seconds." % (time.time() - start_time))

#    print('problem is =', df.iloc[43])

    if question == 'yes':
        check = ('yes')
        while check == 'yes':
            for a in range(10, df.shape[0], 10):
                start_time = time.time()
                check = input('\nWould you like to continue for the next ten trips? Type yes or no.\n')

                if check == 'yes':
                    for i in range(a,a+10):
                        print('Trip Number {}:'.format(i+1))
                        print(df.iloc[i],'\n')

                        print("\nThis took %s seconds." % (time.time() - start_time))
                else:
                    break



def main():
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)


            time_stats(df, month, day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)


        except:
            pass

        row_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
