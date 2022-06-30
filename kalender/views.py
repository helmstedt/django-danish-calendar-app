from django.shortcuts import render
import datetime
from workalendar.europe import Denmark	# Module containing most Danish holidays
from django.http import Http404

# Function to return all calendar dates and other context data
def get_dates(year, period, now):
	now_isocalendar = now.isocalendar()
	
	### HOLIDAY LIST FOR YEAR IS GENERATED ###
		
	# Create dictionary with all holidays of the year
	holidays = Denmark().holidays(year)
	
	all_holidays = {}
	all_holidays[datetime.date(year,5,1)] = ["Første maj", "Særlig dag"]
	all_holidays[datetime.date(year,6,5)] = ["Grundlovsdag", "Særlig dag"]
	all_holidays[datetime.date(year,12,31)] = ["Nytårsaften", "Særlig dag"]

	holiday_lookup = {
						"New year": ["Nytårsdag", "Helligdag"],
						"Holy Thursday": ["Skærtorsdag", "Helligdag"],
						"Good Friday": ["Langfredag", "Helligdag"],
						"Easter Sunday": ["Påskedag", "Helligdag"],
						"Easter Monday": ["2. påskedag", "Helligdag"],
						"Store Bededag": ["Store bededag", "Helligdag"],
						"Ascension Thursday": ["Kr. himmelfart", "Helligdag"],
						"Pentecost Sunday": ["Pinsedag", "Helligdag"],
						"Pentecost Monday": ["2. pinsedag", "Helligdag"],
						"Christmas Eve": ["Juleaften", "Særlig dag"],
						"Christmas Day": ["1. juledag", "Helligdag"],
						"Second Day of Christmas": ["2. juledag", "Helligdag"],
					}
	
	for holiday in holidays:
		# Check for two holidays on same day
		if holiday[0] not in all_holidays:
			all_holidays[holiday[0]] = (holiday_lookup[holiday[1]][0], holiday_lookup[holiday[1]][1])
		# If two on the same day, names are concenated
		else:
			all_holidays[holiday[0]] = (holiday_lookup[holiday[1]][0] + "/" + all_holidays[holiday[0]][0] , holiday_lookup[holiday[1]][1])
	
	### DATES FOR YEAR ARE GENERATED IN A DAY AND MONTH DIMENSION ###
	
	# First dimension is maximum number of days in a month
	dates_in_year = {}
	for day in range(1,32):
		dates_in_year[day] = []
	
	# Second dimension is that date for each month
	for day in range(1,32):
		for month in period:
			# If the generated day actually is a valid date, day is added to dates_in_year dictionary
			try:
				date_to_add = datetime.date(year,month,day)
				date_isocalendar = date_to_add.isocalendar()
								
				# HOLIDAY LOGIC #
				# If day is special, get type of day and name of day
				if date_to_add in all_holidays:
					type_of_day = all_holidays[date_to_add][1]
					name_of_day = all_holidays[date_to_add][0]
				# If not, type of day is normal and no name
				else:
					type_of_day = "Normal dag"
					name_of_day = "Intet navn"
				
				# HTML BORDER CLASS LOGIC #
				html_class = ""
				
				# Year of date must be the same as year of current date
				if date_isocalendar[0] == now_isocalendar[0]:
					# Week number is the same as current week number
					if date_isocalendar[1] == now_isocalendar[1]:
						# All days get a red right and red left class
						html_class = "redleft redright"
						# Sunday also gets a red bottom class
						if date_isocalendar[2] == 7:
							html_class += " redbottom"
					# Date is Sunday in the week before current
					elif date_isocalendar[1] == now_isocalendar[1] - 1 and date_isocalendar[2] == 7:
						html_class += " redbottom"
					# Same date next month is in current week
					try:
						date_next_month = datetime.date(year,month + 1,day)
						date_next_month_isocalendar = date_next_month.isocalendar()
						# Week number is the same as current week number
						if date_next_month_isocalendar[1] == now_isocalendar[1]:
							html_class = "redright"
					except ValueError:
						pass
				date_data = (date_to_add, type_of_day, name_of_day, html_class)
				dates_in_year[day].append(date_data)
			# Except when that dates does not exist, e.g. february 30
			except ValueError:
				dates_in_year[day].append("NON-EXISTING DATE")
	
	context = {'year': str(year), 'next': year+1, 'previous': year-1, 'dates_in_year': dates_in_year, 'period': period, 'now': now}
	return context
	
# Main page
def kalindex(request):
	now = datetime.datetime.now()
	year = now.year
	month = now.month
	if month < 7:
		period = range(1,7)
	else:
		period = range(7,13)
	# Run function to get calendar dates
	context = get_dates(year, period, now)
	return render(request, 'kalender/index.html', context)

# Earlier or future year page
def kalyear(request, year):
	# If year is not an integer, a 404 error is thrown
	try:
		year = int(year)
	except ValueError:
		raise Http404
	# If year is between 1 and 10000, a calendar is rendered
	if year > 0 and year < 10000:
		now = datetime.datetime.now()
		period = range(1,13)
		# Run function to get calendar dates
		context = get_dates(year, period, now)
		return render(request, 'kalender/index.html', context)
	# If not, a 404 error is thrown
	else:
		raise Http404
	
# Earlier or future year page
def kalperiod(request, year, period):
	# If year is not an integer, a 404 error is thrown
	try:
		year = int(year)
	except ValueError:
		raise Http404
	# If year is between 1 and 10000, a calendar is rendered
	if year > 0 and year < 10000 and (period == "1" or period == "2"):
		if period == "1":
			period = range(1,7)
		elif period == "2":
			period = range(7,13)
		now = datetime.datetime.now()
		# Run function to get calendar dates
		context = get_dates(year, period, now)
		return render(request, 'kalender/index.html', context)
	# If not, a 404 error is thrown
	else:
		raise Http404	