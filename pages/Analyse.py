
import streamlit as st
import plotly.graph_objects as go
from jugaad_data.nse import stock_df
from jugaad_data.nse import NSELive
import time
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from statistics import stdev
n = NSELive()
import pandas as pd
from datetime import date,timedelta
st.sidebar.title("⚙️Access Tools")
from nsetools import Nse
nse = Nse()
st_autorefresh(interval=15000, key="data_refresh")
st.title("View Analysis 📈")
st.divider(width="stretch")
all_symbols = nse.get_stock_codes()
st.set_page_config( layout="wide")
selected = st.selectbox("🔎 Select a Stock", all_symbols)
selected_symbol = selected.split(" - ")[0]

st.warning(f"Selected NSE Symbol: {selected_symbol}")
st.divider(width="stretch")
quote = n.stock_quote(selected_symbol)['priceInfo']
col1,col2,col3,col4 =st.columns(4)

with col1:
    st.subheader('Current Data:')
    col1.metric(border=True,label=selected_symbol,value=quote['lastPrice'],delta=round(quote['change'],4))
with col2:
    st.subheader('IntraDay Highest:')
    col2.metric(border=True,label=selected_symbol,value=quote['intraDayHighLow']['max'],delta=round(quote['intraDayHighLow']['max']-quote['lastPrice'],4))
with col3:
    st.subheader('IntraDay Low:')
    col3.metric(border=True,label=selected_symbol,value=quote['intraDayHighLow']['min'],delta=round(quote['intraDayHighLow']['min']-quote['lastPrice'],4))
with col4:
    st.subheader('Day Opening:')
    col4.metric(border=True,label=selected_symbol,value=quote['open'],delta=round(-quote['open']+quote['lastPrice'],4))
st.divider(width="stretch")
c1, c2 = st.columns([2, 1])

with c2:
    st.markdown("### 📅 Date Range")
    end_date   = st.date_input("To",   date.today())
    start_date = st.date_input("From", end_date - timedelta(days=180))
with c1:
    if start_date >= end_date:
        st.error("⚠️  'From' date must be earlier than 'To' date.")
    else:
       
        hist_df = stock_df(
            symbol=selected_symbol,
            from_date=start_date,
            to_date=end_date,
            series="EQ"
        )

        if hist_df.empty:
            st.warning("No data returned for the chosen range.")
        else:
           
            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x     = hist_df["DATE"],
                        open  = hist_df["OPEN"],
                        high  = hist_df["HIGH"],
                        low   = hist_df["LOW"],
                        close = hist_df["CLOSE"],
                        name  = selected_symbol
                    )
                ]
            )
            fig.update_layout(
                title=f"{selected_symbol} — Candlestick chart",
                xaxis_title="Date",
                yaxis_title="Price (₹)",
                xaxis_rangeslider_visible=False,
                height=550,
                margin=dict(l=20, r=20, t=50, b=20)
            )

            st.plotly_chart(fig, use_container_width=True)
with st.container(border=True) as container1:
    with c2:
            
        a,b = c2.columns(2)
        a.metric("Highest In Range:",hist_df["HIGH"].max(),round(hist_df["HIGH"].max()-quote['lastPrice'],4), border=True)
        b.metric("Lowest In Range:",hist_df["LOW"].min(),round(hist_df["LOW"].min()-quote['lastPrice'],4), border=True)
        st.divider(width="stretch")
        
st.divider()
a,b = st.columns([2,1])
with a:
    
    st.line_chart(hist_df,x="DATE",y="OPEN",x_label="Date",y_label="Price (₹)")
st.divider(width="stretch")
with b:
    st.metric("Mean Stock Value",round(hist_df["OPEN"].mean(),2),delta =round(hist_df["OPEN"].mean()-quote['lastPrice'],2),border=True )
    st.metric("Median Stock Value",round(hist_df["OPEN"].median(),2),delta =round(hist_df["OPEN"].median()-quote['lastPrice'],2),border=True )
    st.metric("Standard Deviation in Stock Value",round(stdev(hist_df["OPEN"]),2),delta ='% Deviation = ' + str(round(stdev(hist_df["OPEN"])/quote['lastPrice'],2)),border=True )
