import pandas as pd
import boto3
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title='AWS Login', page_icon='aws.png', layout="wide", initial_sidebar_state="collapsed", menu_items=None)

sbar = st.markdown("""
<style>
[data-testid="stSidebarNav" ] (
display: none;

</style>""",unsafe_allow_html=True)
with st.sidebar:
    # st.image("aws.jpg")
    st.markdown("<h1 style = 'text-align: center; color: #FF9900 ;'>BOOLEAN</h1>", unsafe_allow_html = True)


c1,c2 = st.columns([3.7,5])
with c1:
    st.markdown('')
    st.image("aws.png", width=200)
with c2:
    st.markdown(f"<h1 style = 'text-align: left; color: #F29900 ;'><b>DATA MIGRATOR</b></h1>", unsafe_allow_html = True)
st.markdown('___')
st.markdown('')
st.markdown('')
st.markdown('')

st.markdown("<h3 style = 'text-align: left; color: #FF9900 ;'><u>ENTER YOUR AWS AUTHENTICATION DETAILS</u></h3>", unsafe_allow_html = True)
st.markdown('')
st.markdown('')
c1,c2,c3 = st.columns([1.1,4,6])
with c1:
    st.markdown('')
    st.markdown('')
    st.markdown("<h3 style = 'text-align: left; color: #FF9900 ;'>Access Key :</h3>", unsafe_allow_html = True)
    st.markdown('')
    st.markdown("<h3 style = 'text-align: left; color: #FF9900 ;'>Secret Key :</h3>", unsafe_allow_html = True)
    st.markdown('')
    st.markdown('')
    st.markdown("<h3 style = 'text-align: left; color: #FF9900 ;'>Region :</h3>", unsafe_allow_html = True)

with c2:
    access_key = st.text_input('')
    secret_key = st.text_input('',type='password')
    region = st.selectbox(' ',('Please select a region','af-south-1','ap-east-1','ap-northeast-1','ap-northeast-2','ap-northeast-3','ap-south-1','ap-south-2','ap-southeast-1','ap-southeast-2','ap-southeast-3','ap-southeast-4','ca-central-1','cn-north-1','cn-northwest-1','eu-central-1','eu-central-2','eu-north-1','eu-south-1','eu-south-2','eu-west-1','eu-west-2','eu-west-3','me-central-1','me-south-1','sa-east-1','us-east-1','us-east-2','us-gov-east-1','us-gov-west-1','us-west-1','us-west-2'))

with c3:
    c1,c2,c3 = st.columns([2,3,2.9])
    with c2:
        st.image('aws-fc.png', width = 500)
if secret_key:
    if region:
        try:
            if not access_key or not secret_key or region == 'Please select a region':
                st.error("Please fill in all fields.")
            else:
                s3 = boto3.resource(
                    service_name='s3',
                    region_name=region,
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key
                )
        except boto3.exceptions.NoCredentialsError:
            st.error("Invalid credentials. Please check your access key and secret key.")
        except boto3.exceptions.InvalidRegionError:
            st.error("Invalid region. Please select a valid region.")
    bucket_names = []
    for bucket_name in s3.buckets.all():
        # st.write(bucket_name)
        bucket_names.append(bucket_name.name)
    buckets = st.selectbox('Bucket Name',bucket_names)
    if buckets:
        file_names = []
        for file_name in s3.Bucket(buckets).objects.all():
            file_names.append(file_name.key)

    files = st.selectbox('Select file', file_names)

    if files:
        obj = s3.Bucket(buckets).Object(files).get()
        file_type = files.split('.')[-1]

        if file_type == 'csv':
            df = pd.read_csv(obj['Body'])
        elif file_type == 'xlsx':
            df = pd.read_excel(obj['Body'])
        elif file_type == 'json':
            df = pd.read_json(obj['Body'])
        
        else:
            st.write('Unsupported file type.')
            df = None

        if df is not None:
            df.to_csv('Data.csv', index=False)
            st.dataframe(df)
            btn = st.button('Next')
            if btn:
                switch_page('Connect to Snowflake')


