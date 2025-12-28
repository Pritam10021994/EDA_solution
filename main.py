# Importing necessary libraries:
import io
import numpy as np
import pandas as pd
import streamlit as st
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Design the Front End:
st.set_page_config(page_title="EDA Dashboard", page_icon="📊", layout="wide")
st.title(":rainbow[Data Analysis Dashboard using] :streamlit:")
st.markdown("This dashboard allows you to upload a CSV/xlsx file and perform basic data analysis and visualization.")
# Sidebar Information:

st.sidebar.markdown("**Designed & Developed by:** :rainbow[_Pritam Singh Chauhan_]")
st.sidebar.markdown("Contact: _pritamchauhan@zohomail.in_")
st.sidebar.markdown("LinkedIn: [Pritam Singh Chauhan](https://www.linkedin.com/in/prit-singh-chauhan/)") 
# File Uploader:
st.subheader(":red[Upload your CSV file for analysis:]")
file=st.file_uploader("Choose a file", type=["csv", "xlsx"])

#Action on file upload:
if file is None:
    st.info("Awaiting for CSV/xlsx file to be uploaded.")
    st.stop()
else:
    
    try:
        if file.name.endswith(".csv"):
            df=pd.read_csv(file)
        else:
            df=pd.read_excel(file)
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()
    
    # Display the dataframe:
    st.success("File uploaded successfully!")
# Sidebar Info:
page=st.sidebar.selectbox("Select a Page to Navigate:", options=["Select an Option","Data Reading", "Data Cleaning", "Visualizations", "About"])
if page=="Data Reading":
    col=list(df.columns)
    st.subheader(f":red[***Name of columns in the dataframe:***]\n {col} ")
    st.subheader(f":red[***List of Columns with***] :blue[**_Object_**] :red[type data] :\n")
    col_len=len(col)
    obj_list=[]
    for i in col:
        data_type=df[i].dtype
        if data_type=='object':
            obj_list.append(i)
            continue
            #st.write(f"{i} : {data_type}")
    st.write(f":red[Total Columns in DataFrame with] :blue['Object'] :red[type:] {obj_list}")
    op1, op2= st.multiselect("Select Columns to see Grouping: ", obj_list, max_selections=2, default=[obj_list[0], obj_list[1]])
    try:
        if op1==None or op2==None:
            st.warning("Please select two columns to proceed.")
            st.stop()
        else:
            st.subheader(f"\n:red[***{op1} Vs {op2}:***]")
            st.write(df.groupby(op1)[op2].unique())
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()
    #st.write(df.head())
# Extracting basic Details:

    
    st.subheader(f":red[***Shape of the DataFrame***]:green[(Row,Col):]\t {df.shape} ")

# pandas.dataframe.info() gives 'None' output in streamlit, so using buffer to capture the output:
    st.subheader(f":red[Basic Info:]")
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.code(s)
# Checking for the duplicate rows in the Dataframe:
    st.subheader(f""":red[Count of Duplicate Rows in the DataFrame:] {df.duplicated().sum()}""")
#st.write(df.duplicated().sum(), size=200)

# Checking for the NullValues in the Dataframe:
    st.subheader(":red[Count of Null Values in the DataFrame:]")
    st.write(df.isnull().sum())

# Describing the statistics in the Dataframe:
    st.subheader(f":red[Statistical Data:]\n")
    st.write(df.describe())
    
    st.subheader(":red[Top 5 row:]")
    st.write(df.head())
    st.subheader(":red[Bottom 5 row:]")
    st.write(df.tail())

if page=="Data Cleaning":
    # Checking for the duplicate rows in the Dataframe:
    st.subheader(f""":red[Count of Duplicate Rows in the DataFrame:] {df.duplicated().sum()}""")
#st.write(df.duplicated().sum(), size=200)

# Checking for the NullValues in the Dataframe:
    st.subheader(":red[Count of Null Values in the DataFrame:]")
    st.write(df.isnull().sum())
    option=st.sidebar.selectbox("Data Cleaning Options:", options=["Select an Option","Remove Duplicates", "Handle Missing Values"])
    
    if option=="Remove Duplicates":
        df2=df.drop_duplicates(inplace=False)
        st.success("Duplicates removed successfully!")
        st.subheader(f":red[Count of Duplicate Rows in the DataFrame:] {df2.duplicated().sum()}")
        st.dataframe(df2)
    elif option=="Handle Missing Values":
        missing_value_col=list(df.columns[df.isnull().sum()>0])
        st.write(f":red[Columns with Missing Values:] {missing_value_col}")
        col1, col2, col3, col4=st.columns(4)
        with col1:
            method=st.selectbox("Select Method to Handle Missing Values:", options=["Select an Option","Drop Rows with Missing Values", "Fill Missing Values with Mean", "Fill Missing Values with 'Unknown'", "Fill Missing Values with -"])
            if method=='Drop Rows with Missing Values':
                df2=df.dropna()
                st.success("Missing values dropped successfully!")
                st.subheader(":red[Count of Null Values in the DataFrame:]")
                st.write(df2.isnull().sum())
                st.dataframe(df2)
            elif method=='Fill Missing Values with Mean':
                df2=df.fillna(df.mean())
                st.success("Missing values filled successfully!")
                st.subheader(":red[Count of Null Values in the DataFrame:]")
                st.write(df2.isnull().sum())
                st.dataframe(df2)
            elif method=="Fill Missing Values with 'Unknown'":
                df2=df.fillna('Unknown', inplace=True)
                st.success("Missing values filled successfully!")
                st.subheader(":red[Count of Null Values in the DataFrame:]")
                st.write(df2.isnull().sum())
                st.dataframe(df2)
            elif method=='Fill Missing Values with -':
                pass
    #     missing_option=st.selectbox("Select Missing Value Handling Method:", options=["Select an Option","Drop Rows with Missing Values", "Fill Missing Values with Mean"])
    #     if missing_option=="Drop Rows with Missing Values":
    #         df2=df.dropna()
    #         st.success("Missing values dropped successfully!")
    #         st.subheader(":red[Count of Null Values in the DataFrame:]")
    #         st.write(df2.isnull().sum())
    #         st.dataframe(df2)
    #     elif missing_option=="Fill Missing Values with Mean":
    #         df2=df.fillna(df.mean())
    #         st.success("Missing values filled successfully!")
    #         st.subheader(":red[Count of Null Values in the DataFrame:]")
    #         st.write(df2.isnull().sum())
    #         st.dataframe(df2)
    # # Checking for the duplicate rows in the Dataframe:
        
    #st.write(df.duplicated().sum())

# Checking for the NullValues in the Dataframe:
    #st.subheader(":red[Count of Null Values in the DataFrame:]")
    #st.write(df2.isnull().sum())