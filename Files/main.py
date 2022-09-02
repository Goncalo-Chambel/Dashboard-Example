import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import datetime as dt
from dateutil.relativedelta import relativedelta
import matplotlib.dates as mdates
import numpy as np


def relate_data(data, key_variable, value_variable):
	keys = data[key_variable]
	values = data[value_variable]

	info = {}
	aux = {} # to hold all the values to compute the mean
	for key, value in zip(keys, values):
		if key in info:
			aux[key].append(value)
			info[key][0] = np.mean(aux[key])

		else:
			info[key] = [[]]
			aux[key] = []


	df = pd.DataFrame.from_dict(info,orient='index')	
	df = df.rename(columns = {0:value_variable})

	return df


def get_distribution(data, column_name):
	values = data[column_name].tolist()

	distribution = {}
	total = 0
	for value in values:
		total = total + 1
		if value not in distribution:
			distribution[value] = 1
		else:
			distribution[value] = distribution[value] + 1

	for key in distribution:
		distribution[key] = distribution[key] / total

	return distribution	

def get_signups(data, start, end):

	dates = []

	delta = relativedelta(end, start)
	nr_months =  delta.months + delta.years * 12
	current_date = start
	for i in range(nr_months):
		#dates.append(mdates.date2num(current_date))
		dates.append(current_date)
		current_date = current_date + relativedelta(months=1)

	count = np.zeros_like(dates,dtype=int)
	for date_str in data:
		date = dt.datetime.strptime(date_str, '%Y-%m-%d')
		for i in range(len(dates)):
			if date.month == dates[i].month and date.year == dates[i].year:
				count[i] = count[i] + 1

	
	return dates, count



data = pd.read_csv('data.csv')
gender_distribution = get_distribution(data, 'Gender')
country_distribution = get_distribution(data, 'Country')
dates, signups_distribution = get_signups(data['Sign Up Date'].tolist(), dt.datetime(2020, 1, 1), dt.datetime(2022,1,1))
accumulative_signups = np.zeros_like(signups_distribution, dtype=int)
salaries_by_profession = relate_data(data, 'Profession', 'Salary')
salaries_by_ages = relate_data(data, 'Age', 'Salary')


#plt.plot(list(mean_salaries_by_profession.keys()), list(mean_salaries_by_profession.values()))
#plt.show()

'''
accumulative_signups[0] = signups_distribution[0]
for i in range(1, len(signups_distribution)):
	accumulative_signups[i] = accumulative_signups[i-1] + signups_distribution[i]

fig, ax = plt.subplots()
#plt.pie(list(country_distribution.values()), labels=list(country_distribution.keys()), autopct='%1.2f%%')

fig, ax = plt.subplots()

width = np.diff(dates).min()

ax.bar(dates, accumulative_signups, align='center', width=width)
ax.xaxis_date()

# Make space for and rotate the x-axis tick labels
fig.autofmt_xdate()
#ax.set_xticklabels(list(signups_distribution.keys()),rotation=45, rotation_mode="anchor", ha="right")

plt.show()
'''
#st.set_page_config(page_title="Dashboard Interna - Clynx", layout="wide")
#st.write('Hello world')
st.line_chart(salaries_by_profession)
	
