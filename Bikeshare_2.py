# coding: utf-8
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
	"""
	Asks user to specify a city, month, and day to analyze.
	Returns:
	(str) city - name of the city to analyze
	(str) month - name of the month to filter by, or "all" to apply no month filter
	(str) day - name of the day of week to filter by, or "all" to apply no day filter
	"""
	print('Hello! Let\'s explore some US bikeshare data!')
	city_list = [ "Chicago", "New York City", "Washington" ]
	months = ('All', 'January', 'Febuary', 'March', 'April', 'May', 'June')
	days = ('All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
	while True:
		# get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
		city = input('Select city from list: Chicago, New York City, Washington\nCity Name: ')
		# get user input for month (all, january, february, ... , june)
		month = input('Select a specific month between January and June or type "all" for the entire year\nMonth: ')
		# get user input for day of week (all, monday, tuesday, ... sunday)
		day = input('Select a specific day, or type all for the entire week\nDay: ')
		if city.title() in city_list:  
			if  month.title() in months:
				if day.title() in days:
					break
				else:
					print('Invalid day entry: "{}". please enter a valid day!'.format(day))
			else:
				print('Invalid month entry: "{}". Please enter a valid month!'.format(month))
		else:
			print('Oups! Please enter a valid city, month and day\nYou have entered: city: {0}, month: {1}, day: {2}'.format(city, month, day)) 
	print('-'*40)
	return city, month, day
#---------------------------
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
	df = pd.read_csv(CITY_DATA[city.title()])
	#print(CITY_DATA[city])
	#print(df)
	#--- clean NaNs 
	df.dropna(axis=0, inplace=True)
	# convert the Start Time column to datetime
	df['Start Time'] = pd.to_datetime(df['Start Time'])
	# extract month and day of week from Start Time to create new columns
	df['month'] = df['Start Time'].dt.month_name()
	df['day_of_week'] = df['Start Time'].dt.day_name()
	#-- get hour 
	df['hour'] = df['Start Time'].dt.hour
    #print(df.head())
    # filter by month if applicable
	if month != 'all':
        # use the index of the months list to get the corresponding int
		months = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		month = months[months.index(month.title())]
        # filter by month to create the new dataframe
		df = df[df.month == month]
    # filter by day of week if applicable
	if day != 'all':
        # filter by day of week to create the new dataframe
		days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
		day = days[days.index(day.title())]
		df = df[df.day_of_week == day]
	return df

#---------------------------
def time_stats(df):
	"""Displays statistics on the most frequent times of travel."""
	print('\nCalculating The Most Frequent Times of Travel...\n')
	start_time = time.time()
	# display the most common month
	top_month = df['month'].mode()[0]
	print('---> The most common month: {}'.format(top_month))
	#
	# display the most common day of week
	top_week = df['day_of_week'].mode()[0]
	print('---> The most common week: {}'.format(top_week))
	# display the most common start hour
	#
	top_hour = df['hour'].mode()[0]
	print('---> The most common start hour: {}'.format(top_hour))
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)
#---------------------------
def station_stats(df):
	"""Displays statistics on the most popular stations and trip."""
	print('\nCalculating The Most Popular Stations and Trip...\n')
	start_time = time.time()
	# display most commonly used start station
	top_start_station = df['Start Station'].mode()[0]
	print('---> The most commonly used start station: {}'.format(top_start_station))
	# display most commonly used end station
	top_end_station = df['End Station'].mode()[0]
	print('---> The most commonly used end station: {}'.format(top_end_station))
	# display most frequent combination of start station and end station trip
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)
#---------------------------
def trip_duration_stats(df):
	"""Displays statistics on the total and average trip duration."""
	print('\nCalculating Trip Duration...\n')
	start_time = time.time()
	# display total travel time
	total_travel_time = df['Trip Duration'].sum()
	print('---> Total travel time in seconds: {}'.format(total_travel_time))
	# display mean travel time
	mean_travel_time = df['Trip Duration'].mean()
	print('---> The mean of travel time in seconds: {}'.format(mean_travel_time))
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)
#---------------------------
def user_stats(df):
	"""Displays statistics on bikeshare users."""
	print('\nCalculating User Stats...\n')
	start_time = time.time()
	# Display counts of user types
	try:
		user_type_count = df['User Type'].value_counts() 
		print('\n\tUser Types: \n{0}'.format(user_type_count))
		# Display counts of gender
		gender_count = df['Gender'].value_counts()
		print('\n\tCount by gender: \n{0}'.format(gender_count))
		# Display earliest, most recent, and most common year of birth
		earliest = df['Birth Year'].min().astype(int)
		most_recent = df['Birth Year'].max().astype(int)
		most_common = df['Birth Year'].mode()[0].astype(int)
		print('\n\tYear of Birth Stats:\nEarliest: {0}\nMost Recent: {1}\nMost Common: {2}\n'.format(earliest, most_recent, most_common))
	except KeyError as e:
		print('Oups...Unable to get report due to following error: \n{0}'.format(e))
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)
#---------------------------
def main():
	while True:
		city, month, day = get_filters()
		df = load_data(city, month, day)

		time_stats(df)
		station_stats(df)
		trip_duration_stats(df)
		user_stats(df)

		restart = input('\nWould you like to restart? Enter yes or no.\n')
		if restart.lower() != 'yes':
			break


if __name__ == "__main__":
	main()
