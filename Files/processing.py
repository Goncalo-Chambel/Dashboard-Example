import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from dateutil.relativedelta import relativedelta
import matplotlib.dates as mdates
import numpy as np
import math

def pie_chart(df):
	labels = list(df.index)
	values = list(df['Percentage'])

	fig, ax = plt.subplots()
	ax.pie(values,labels=labels, autopct='%1.1f%%')
	ax.axis('equal') 

	ax.spines['top'].set_visible(False) 
	ax.spines['right'].set_visible(False) 
	ax.spines['bottom'].set_visible(False) 
	ax.spines['left'].set_visible(False) 

	return fig

def generate_age_groups():
	groups = {}
	for i in range(0, 100):
		groups[i] = math.floor(i/10)

	return groups


def relate_data(data, key_variable, value_variable):

	keys = data[key_variable]
	values = data[value_variable]

	if key_variable == 'Age':
		groups = generate_age_groups()

	info = {}
	aux = {} # to hold all the values to compute the mean
	for key, value in zip(keys, values):
		if key_variable != 'Age':
			if key in info:
				aux[key].append(value)
				info[key][0] = np.around(np.mean(aux[key]),2)

			else:
				info[key] = [[]]
				aux[key] = []

		else:
			if groups[key] in info:
				aux[groups[key]].append(value)
				info[groups[key]][0] = np.around(np.mean(aux[groups[key]]),2)
			else:				
				info[groups[key]] = [[]]
				aux[groups[key]] = []

	df = pd.DataFrame.from_dict(info,orient='index')	
	df = df.rename(columns = {0:'Average ' + value_variable})
	if key_variable == 'Age':
		df = df.sort_index()
		df = df.rename(index={0:'0-9',1:'10-19', 2:'20-29', 3:'30-39', 4:'40-49', 5:'50-59', 6:'60-69', 7:'70-79', 8:'80-89', 9:'90-99'})
	return df


def get_distribution(data, column_name):

	values = data[column_name].tolist()

	distribution = {}

	if column_name == 'Age':
		groups = generate_age_groups()

	total = 0
	for value in values:
		total = total + 1
		if column_name != 'Age':
			if value not in distribution:
				distribution[value] = 1
			else:
				distribution[value] = distribution[value] + 1
		else:
			if groups[value] not in distribution:
				distribution[groups[value]] = 1
			else:
				distribution[groups[value]] = distribution[groups[value]] + 1


	for key in distribution:
		distribution[key] = distribution[key] / total * 100

	df = pd.DataFrame.from_dict(distribution,orient='index')	
	df = df.rename(columns = {0:'Percentage'})
	if column_name == 'Age':
		df = df.sort_index()
		df = df.rename(index={0:'0-9',1:'10-19', 2:'20-29', 3:'30-39', 4:'40-49', 5:'50-59', 6:'60-69', 7:'70-79', 8:'80-89', 9:'90-99'})

	return df	

def get_signups(data, start, end):

	dates = []

	delta = relativedelta(end, start)
	nr_months =  delta.months + delta.years * 12
	current_date = start
	for i in range(nr_months):
		dates.append(current_date)
		current_date = current_date + relativedelta(months=1)

	count = np.zeros_like(dates,dtype=int)
	for date_str in data['Sign Up Date'].tolist():
		date = dt.datetime.strptime(date_str, '%Y-%m-%d')
		for i in range(len(dates)):
			if date.month == dates[i].month and date.year == dates[i].year:
				count[i] = count[i] + 1

	df = pd.DataFrame({'Dates':dates, 'Count':count})
	df = df.set_index('Dates')

	return df

def accumulated_signups(df):
	
	new_df = df.copy()
	total = 0
	for index, row in df.iterrows():
		total = total + row['Count']
		new_df.at[index, 'Count'] = total

	new_df = new_df.rename(columns = {'Count':'Accumulated count'})
	return new_df

def search(data, column, search_term):
	if column == 'Age':
		search_term = int(search_term)
	indexes = data.loc[data[column].isin([search_term])].index
	if indexes.size > 0:
		return data.iloc[indexes]
	else:
		return pd.DataFrame()


if __name__ == "__main__":

	data = pd.read_csv('data.csv')
	#print(data.head())

	gender_distribution = get_distribution(data, 'Gender')
	#print(gender_distribution)

	age_distribution = get_distribution(data, 'Age')
	#print(age_distribution)

	profession_distribution = get_distribution(data, 'Profession')
	#print(profession_distribution)

	signups = get_signups(data, dt.datetime(2020, 1, 1), dt.datetime(2022,1,1))
	#print(signups)

	accumulated_signups = accumulated_signups(signups)
	#print(accumulated_signups)

	salaries_by_profession = relate_data(data, 'Profession', 'Salary')
	#print(salaries_by_profession)
	
	salaries_by_age = relate_data(data, 'Age', 'Salary')
	#print(salaries_by_age)

	search_result = search(data, 'Sign Up Date', '2022-11-20')
	#print(search_result)