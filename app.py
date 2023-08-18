import pickle
from pathlib import Path 
#yaml and config file 
import yaml 
from yaml import SafeLoader
#with open('config.yaml') as config_file:
#    config = yaml.load(config_file, Loader=SafeLoader)

#date import for any usage (eg. get current date for file's name...)
import datetime 
from datetime import datetime
now = datetime.now()

#streamlit + snowpark library
import streamlit as st
import pandas as pd
import json

from azure.identity import DefaultAzureCredential
import msal
import requests

import io
import sys
import base64
import time
import json
import snowflake.connector

#work with tabular data (csv + xlsx)
from io import BytesIO

#work with azure blobs and other services
from azure.storage.blob import BlobServiceClient


###SETTING WEB APP BACKGROUND
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-repeat: no-repeat;
    display: block;
    background-position: 100vh 100vw;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
#set_background('blank.png')
# #002161
###CHANGING WEB APP SIDEBAR COLOR
sidebar_color = '''
                <style>
                [data-testid=stSidebar] {
                    background-color: #0e428f;
                }
                </style>
                ''' 
st.markdown(sidebar_color, unsafe_allow_html=True)

with st.sidebar:
    daymonthyear = str((now.strftime("%d/%m/%Y")))
    hour = str((now.strftime("%H:%M:%S")))
    st.sidebar.image("govhack.png")
    #st.sidebar.title(f"Welcome to CES Data Upload Website")
    #st.sidebar.write(f"Last action was taken on " + str((now.strftime("%d/%m/%Y"))) + " at " + str((now.strftime("%H:%M:%S"))))
    st.sidebar.markdown("<h2 style = 'text-align: center; color:white; font-size: 30px'>Visual Lies' Report Portal</h2>", unsafe_allow_html=True )
    st.sidebar.write(f"<span style = 'color:white;font-style:italic'>Last updated on {daymonthyear} at {hour} </span>", unsafe_allow_html=True)


###ADDING NAVIGATION BAR USING BOOTSTRAP + CSS

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav" style="background-color: #b8edf5; padding: 15px; border: 1px solid #999999; border-radius:15px 15px 15px 15px">
        <span style="color: #333333; font-size: 20px;font-weight:bold;float:right;">VISUAL LIES - GOVHACK 2023</span>
        <br>
        <span style = "color: #333333;font-size:15px;position:absolute;right:10px">https://github.com/VisuaLies-Govhack23/HeriTours</span>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

navbar_style = """
    <style>
        nav {
            background-color: #3498DB;
            height: 10px; /* Adjust the height as needed */
            width: 100%; /* Set the width to 100% to span the full width */
            position: fixed;
            top: 0;
            left: 0;
            z-index: 9999;
        }
    </style>
"""
st.markdown(navbar_style, unsafe_allow_html=True)

st.markdown("<h1 style = 'text-align: center;color:#002161'>NSW Heritage Visualisation</h1>", unsafe_allow_html=True)

st.markdown("<h3 style = 'text-align: center;font-size:20px'> Uncover Heritage NSW: Reviving Local Narratives for Lasting Impact</h3>",unsafe_allow_html=True)

#st.markdown("Discover Heritage NSW seeks to revitalize the appreciation of local heritage, cultivating a deep connection between individuals and their cultural origins. This initiative aims to unravel the hidden narratives embedded in the heritage of New South Wales, fostering a sense of identity, well-being, and community engagement. By harnessing innovative approaches, collaborative partnerships, and AI-driven technologies, we aspire to empower communities to uncover, preserve, and celebrate their heritage, thus strengthening bonds, promoting economic growth, and nurturing a shared sense of belonging. Together, we endeavor to unleash the transformative potential of heritage, cultivating critical awareness and fostering a genuine appreciation for the diverse heritage treasures scattered throughout New South Wales.')
st.markdown("<span style = 'text-align: center;font-size:15px;font-style:italic;animation: fade-in;'> Discover Heritage NSW seeks to revitalize the appreciation of local heritage, cultivating a deep connection between individuals and their cultural origins. This initiative aims to unravel the hidden narratives embedded in the heritage of New South Wales, fostering a sense of identity, well-being, and community engagement. By harnessing innovative approaches, collaborative partnerships, and AI-driven technologies, we aspire to empower communities to uncover, preserve, and celebrate their heritage, thus strengthening bonds, promoting economic growth, and nurturing a shared sense of belonging. Together, we endeavor to unleash the transformative potential of heritage, cultivating critical awareness and fostering a genuine appreciation for the diverse heritage treasures scattered throughout New South Wales.</span>",unsafe_allow_html=True)

st.markdown("<h2 style = 'font-weight:bold;font-size:30px'> Cultural Diversity in Australia - Census 2021 </h2>", unsafe_allow_html=True)

st.markdown("<iframe title='data visualization' width='800' height='400' src='https://app.powerbi.com/reportEmbed?reportId=f77c29c4-4bad-49c8-9a90-08d66c3920d9&autoAuth=true&ctid=99b27c4c-69fe-467e-886e-e2014e05d147' frameborder='10' allowFullScreen='true'></iframe>", unsafe_allow_html=True)


st.markdown("<h2 style = 'font-weight:bold; font-size:30px'> Pie chart </h2>", unsafe_allow_html=True)


st.markdown(
    """
    <style>
    span {
        margin-top: 10px
    }
    </style>
    """,
    unsafe_allow_html= True
)

st.markdown (
    """
    <style>
    h2, stDownloadButton, stButton, stFileUploader {
        margin-top: 50px
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    div {
        margin-top: 0px
    
    }
    </style>
    """
    , unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@500&family=Lato:wght@500&display=swap');

    .css-9ycgxx {
        color: #0056FB;
        font-size: 16px;
        font-family: Inter;
        font-weight: bold;
    }
    """
    ,unsafe_allow_html=True
)

st.markdown(
    """
    <style>

    .css-5rimss {
        animation: fade-in 0.8s 1.7s forwards cubic-bezier(0.11, 0, 0.5, 0);
    }
    """
    ,unsafe_allow_html=True
)
