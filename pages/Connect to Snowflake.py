import snowflake.connector
import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import time

st.snow()
c1,c2,c3 = st.columns([4,2,4])
with c2:
    st.image('snowflake.png',width=360)
st.markdown(f"<h1 style = 'text-align: left; color: #29B5E8 ;'><b><u>Connect to Snowflake</u></b></h1>", unsafe_allow_html = True)
c1,c2 = st.columns([3,4])
with c1:
    st.markdown(' ')
    st.markdown(' ')
    st.markdown(' ')
    snowflake_account = st.text_input('Account')
    snowflake_user = st.text_input('Username')
    snowflake_password = st.text_input('Password', type='password')
with c2:
     c1,c2,c3 = st.columns([1,3,1])
     with c2:
        st.image('/Users/himanshutipirneni/Streamlit/Project2/sf-fc.png', width=750)

if snowflake_account and snowflake_user and snowflake_password:
    try:
        connection = snowflake.connector.connect(
            user=snowflake_user,
            password=snowflake_password,
            account=snowflake_account
        )
        st.success("Successfully Connected To Snowflake")
        
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        database_names = [row[1] for row in cursor]
        selected_database = st.selectbox("Select Database", database_names)
        
        if selected_database:
            cursor.execute(f"USE DATABASE {selected_database}")
            cursor.execute("SHOW SCHEMAS")
            schema_names = [row[1] for row in cursor]
            selected_schema = st.selectbox("Select Schema", schema_names)
            
            df = pd.read_csv('/Users/himanshutipirneni/Streamlit/Project2/Data.csv')
            st.dataframe(df)
            file_name = st.text_input('Enter the table name for snowflake')
            push = st.button('Push Data to Snowflake')
            if push:
                if selected_schema:
                        engine = create_engine(f"snowflake://{snowflake_user}:{snowflake_password}@{snowflake_account}/{selected_database}/{selected_schema}")
                        df.to_sql(file_name, engine, index=False, if_exists='replace')
                        with st.spinner('Uploading table to database '+selected_database + ' in Snowflake'):
                            time.sleep(10)
                        st.success("File uploaded to Snowflake successfully!")
                
    except Exception as e:
        st.error("Could not connect to Snowflake. Error: {}".format(e))
