import streamlit as st 
import pandas as pd 
from ydata_profiling import ProfileReport
from streamlit.components.v1 import html
from ydata_profiling.config import Settings
import sys
import os
import json
st.set_page_config(page_title='Data Profile App',layout='wide', initial_sidebar_state = "expanded")

#File Size function
def get_filesize(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes / (1024**2)
    return size_mb

#File Type function
def validate_file(file):
    filename = file.name
    name, ext = os.path.splitext(filename)
    if ext in ('.csv','.xlsx'):
        return ext
    else:
        return False
    

# sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Upload .csv, .xlsx files not exceeding 10 MB")
    
    if uploaded_file is not None:
            ext = validate_file(uploaded_file)
            if ext:
                st.write("Modes of Operation")
                minimal = st.checkbox('Activate minimalistic report type')
        
        
        
# Main Body    
if uploaded_file is not None:
    # ext = validate_file(uploaded_file)
    
    # Check if "CSV" or "XLSX"
    if ext:
        filesize = get_filesize(uploaded_file)

        # Check the Filesize (max 10MB)
        if filesize <= 10:

            if ext == ".csv":
                # load csv file type
                df = pd.read_csv(uploaded_file)
            else:
                # load xlsx file type
                xl_file = pd.ExcelFile(uploaded_file)
                sheet_tuple = tuple(xl_file.sheet_names)

                # Create new selection on sidebar when "XLSX"
                sheet_name = st.sidebar.selectbox("Select the sheet", sheet_tuple)
                df = xl_file.parse(sheet_name)

            # Generate Report
            with st.spinner("Generating Report..."):
                pr = ProfileReport(df,minimal=minimal)
                report_html = pr.to_html()
                html(report_html, height=1000, scrolling=True)
        
        else:
            st.error(f"Maximum allowed size is 10MB! We recieved {filesize} MB.")
    
    else:
        st.error("Not correct file format. Please upload only .csv or .xslx file format!!!")

else:
    st.title("Data Profiler")
    st.info("Upload your data in the left sidebar to generate report profiling.")

    
    