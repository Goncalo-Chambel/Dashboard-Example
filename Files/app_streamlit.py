import streamlit as st
from processing import *
import pandas as pd
from pathlib import Path

data = pd.read_csv(Path(__file__).parents[0]/'data.csv')

df = pd.DataFrame()
st.set_page_config(page_title="Dashboard",layout='wide')

st.markdown("<h1 style='text-align: center; color: black;'>My Dashboard</h1>", unsafe_allow_html=True)


buffer, col2, col3 = st.columns([1, 5, 15])

with col2:
    key = st.selectbox("Key",['Name','Email','Age','Gender','Country','Sign Up Date', 'Profession','Salary'])

with col3:
    search_term = st.text_input("Search")
    if key != '' and search_term != '':
        df = search(data, key, search_term)

buffer, col2 = st.columns([1, 20])
with col2:
    if not df.empty:
        st.dataframe(df)
    else:
        st.write('Did not find any person matching the criteria')

st.markdown('***') #separator

buffer, col2, col3, col4 = st.columns([1,7,7,7])

with col2:
    st.markdown("<h5 style='text-align: center; color: black;'>Gender Distribution</h1>", unsafe_allow_html=True)
    st.pyplot(pie_chart(get_distribution(data, 'Gender')))

with col3:
    st.markdown("<h5 style='text-align: center; color: black;'>Age Distribution</h1>", unsafe_allow_html=True)
    st.bar_chart(get_distribution(data, 'Age'))

with col4:
    st.markdown("<h5 style='text-align: center; color: black;'>Country Distribution</h1>", unsafe_allow_html=True)
    st.pyplot(pie_chart(get_distribution(data, 'Country')))

st.markdown('***') #separator

buffer, col2, col3 = st.columns([1, 10, 10])

with col2:
    st.markdown("<h5 style='text-align: center; color: black;'>Average salary per profession</h1>", unsafe_allow_html=True)
    st.bar_chart(relate_data(data, 'Profession', 'Salary'))

with col3:
    st.markdown("<h5 style='text-align: center; color: black;'>Average salary per age group</h1>", unsafe_allow_html=True)
    st.bar_chart(relate_data(data, 'Age', 'Salary'))


st.markdown('***') #separator

buffer, col2 = st.columns([1, 20])

with col2:
    st.markdown("<h5 style='text-align: center; color: black;'>Accumulated signups over time</h1>", unsafe_allow_html=True)
    st.line_chart(accumulated_signups(get_signups(data, dt.datetime(2020, 1, 1), dt.datetime(2022,12,31))))