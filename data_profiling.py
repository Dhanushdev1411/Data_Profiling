import streamlit as st
import pandas as pd
from io import StringIO
import os
import ydata_profiling
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(layout="wide")

def load_data(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
        return pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file type!")
        return None

def object_wise_profiling(df, object_column):
    unique_objects = df[object_column].unique()
    object_choice = st.selectbox("Select an Object", unique_objects)
    object_data = df[df[object_column] == object_choice]
    
    st.write(f"### Profiling Report for {object_choice}")
    error_columns = ['Length_error', 'Width_error', 'Height_error']
    data_report = object_data[error_columns].profile_report(correlations=None, duplicates=None, missing_diagrams=None)
    st_profile_report(data_report)

    st.write(f"### Error Analysis for {object_choice}")
    st.dataframe(object_data[error_columns].describe())

def position_wise_profiling(df, position_column):
    unique_positions = df[position_column].unique()
    position_choice = st.selectbox("Select an position", unique_positions)
    position_data = df[df[position_column] == position_choice]
    
    st.write(f"### Profiling Report for {position_choice}")
    error_columns = ['Length_error', 'Width_error', 'Height_error']
    data_report = position_data[error_columns].profile_report(correlations=None, duplicates=None, missing_diagrams=None)
    st_profile_report(data_report)

    st.write(f"### Error Analysis for {position_choice}")
    st.dataframe(position_data[error_columns].describe())

def pallet_wise_profiling(df, pallet_column):
    unique_pallets = df[pallet_column].unique()
    pallet_choice = st.selectbox("Select an pallet", unique_pallets)
    pallet_data = df[df[pallet_column] == pallet_choice]
    
    st.write(f"### Profiling Report for {pallet_choice}")
    error_columns = ['Length_error', 'Width_error', 'Height_error']
    data_report = pallet_data[error_columns].profile_report(correlations=None, duplicates=None, missing_diagrams=None)
    st_profile_report(data_report)

    st.write(f"### Error Analysis for {pallet_choice}")
    st.dataframe(pallet_data[error_columns].describe())

with st.sidebar:
    nav_choice = st.radio(
        "Pallet Data Profiling",
        ['Uploading', 'Profiling', 'Pallet Wise Profiling', 'Object Wise Profiling', 'Position Wise Profiling']
    )

if nav_choice == "Uploading":
    st.write("## Upload your Data for Profiling")
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx', 'xls'])
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.dataframe(df)
            df.to_csv('model_data.csv', index=False)

source_data_exists = os.path.exists("model_data.csv")
if source_data_exists:
    df = pd.read_csv('model_data.csv', index_col=None)

if nav_choice == "Profiling":
    st.write("## Automated Exploratory Data Analysis")
    if source_data_exists:
        with st.container():
            data_report = df.profile_report(missing_diagrams=None)
            st_profile_report(data_report)
    else:
        st.write("Please upload your data in the uploading page")

if nav_choice == "Pallet Wise Profiling":
    st.write("## Pallet Wise Profiling")
    if source_data_exists:
        pallet_wise_profiling(df, 'Pallet')
    else:
        st.write("Please upload your data in the uploading page")

if nav_choice == "Object Wise Profiling":
    st.write("## Object Wise Profiling")
    if source_data_exists:
        object_wise_profiling(df, 'Object')
    else:
        st.write("Please upload your data in the uploading page")

if nav_choice == "Position Wise Profiling":
    st.write("## Position Wise Profiling")
    if source_data_exists:
        position_wise_profiling(df, 'Position')
    else:
        st.write("Please upload your data in the uploading page")