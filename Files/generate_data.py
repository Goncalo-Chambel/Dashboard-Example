import pandas as pd
import random 
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

seed = 1 # remove this if you want random data every time
nr_rows = 2000
filename = 'data.csv'



def random_date_in_range(start_date, end_date):

	time_between_dates = end_date - start_date
	days_between_dates = time_between_dates.days
	random_number_of_days = random.randrange(days_between_dates)
	random_date = start_date + datetime.timedelta(days=random_number_of_days)
	return random_date


gender_options = ['Male', 'Female']
country_options = ['Portugal', 'United States', 'Brazil', 'France', 'Denmark', 'Mexico', 'Germany', 'Japan', 'Spain']
first_name_options = ['Bridie','Bryson','Reginald','Daanyal','Aeryn','Nettie','Dawn','Katelyn','Mujtaba','Stan']
last_name_options = ['Lucas','Tait','Maxwell','Levine','Hook','Mcgregor','Stephenson','Lord','Delgado','Barnett']
profession_options = ['Professional athlete','Massage Therapist','Secretary','High School Teacher','Environmental scientist','Social Worker','Accountant','Epidemiologist','Market Research Analyst','Dentist','Construction Manager','Substance Abuse Counselor']
email_domain_options = ['@gmail.com', '@hotmail.com', '@webmail.com', '@yahoo.com', '@outlook.com']

data = []
gender_data = []
country_data = []
name_data = []

age_distribution = np.random.normal(45, 15, nr_rows)
salary_distribution = np.random.normal(2000, 500, nr_rows)

start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2022, 12, 31)
for i in range(nr_rows):
	random_gender = random.choice(gender_options)
	random_country = random.choice(country_options) 
	random_first_name = random.choice(first_name_options)
	random_last_name = random.choice(last_name_options)
	random_name =  random_first_name + " " + random_last_name 
	random_email = random_first_name.lower() + "." + random_last_name.lower() + str(random.choice(range(100))) + random.choice(email_domain_options)
	random_profession = random.choice(profession_options)
	age = min(max(0,int(age_distribution[i])),99)
	salary = max(1000,int(salary_distribution[i]))
	salary = int(salary + age ** random.choice(np.linspace(1.1, 2, 10)))
	signup_date = random_date_in_range(start_date, end_date)
	if relativedelta(end_date, start_date).months + relativedelta(end_date, start_date).years * 12 >= 3:
		start_date = start_date + relativedelta(days=1) #just to force the exponential growth

	row = [random_name, random_email, age, random_gender, random_country, signup_date, random_profession, salary]

	data.append(row)



df = pd.DataFrame(data, columns=['Name','Email','Age','Gender','Country','Sign Up Date', 'Profession','Salary'])
print(df)
df.to_csv(filename, index=False)


