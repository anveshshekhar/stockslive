import streamlit as st
from streamlit_autorefresh import st_autorefresh
from nsetools import Nse
from jugaad_data.nse import stock_df
from datetime import date,timedelta
import pandas as pd
from jugaad_data.nse import NSELive
from statistics import stdev
nse= Nse()
st_autorefresh(interval=15000, key="data_refresh")
st.set_page_config(layout="wide")
st.sidebar.title("⚙️Access Tools")
st.title("Compare Stocks : 💹🆚")
a,b = st.columns(2)
n = NSELive()
with a:
    with a.container(border=True):
        all_symbols = nse.get_stock_codes()
        selected1 = st.selectbox("🔎 Select First Stock", all_symbols)
        
with b: 
    with b.container(border=True):
        all_symbols = nse.get_stock_codes()
        selected2 = st.selectbox("🔎 Select Second Stock", all_symbols)

quote1 = n.stock_quote(selected1)['priceInfo']
quote2 = n.stock_quote(selected2)['priceInfo']


with st.container(border=True):
    end_date   = st.date_input("To",   date.today())
    start_date = st.date_input("From", end_date - timedelta(days=180))
        
df1 = stock_df(symbol=selected1,to_date=end_date,from_date=start_date,series="EQ")
df2 = stock_df(symbol=selected2,to_date=end_date,from_date=start_date,series="EQ")
with st.container(border=True):   
    colchart1,colchart2 = st.columns([1,1])
    with colchart1:
        st.subheader("Selected Stock 1: %s"%(selected1))
        char1  = colchart1.line_chart(df1,y='CLOSE',x='DATE')
        colchart1.metric("Mean Stock Value",round(df1["OPEN"].mean(),2),delta =round(df1["OPEN"].mean()-quote1['lastPrice'],2),border=True )
        colchart1.metric("Median Stock Value",round(df1["OPEN"].median(),2),delta =round(df1["OPEN"].median()-quote1['lastPrice'],2),border=True )
        colchart1.metric("Standard Deviation in Stock Value",round(stdev(df1["OPEN"]),2),delta ='% Deviation = ' + str(round(stdev(df1["OPEN"])/quote1['lastPrice'],2)),border=True )
        
    with colchart2:
        st.subheader("   Selected Stock 2: %s"%(selected2))

        char2  = colchart2.line_chart(df2,y='CLOSE',x='DATE')
        st.metric("Mean Stock Value",round(df2["OPEN"].mean(),2),delta =round(df2["OPEN"].mean()-quote2['lastPrice'],2),border=True )
        st.metric("Median Stock Value",round(df2["OPEN"].median(),2),delta =round(df2["OPEN"].median()-quote2['lastPrice'],2),border=True )
        st.metric("Standard Deviation in Stock Value",round(stdev(df2["OPEN"]),2),delta ='% Deviation = ' + str(round(stdev(df2["OPEN"])/quote2['lastPrice'],2)),border=True )
