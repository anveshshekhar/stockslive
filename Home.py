import streamlit as st
from jugaad_data.nse import NSELive
import datetime

n =NSELive()


st.set_page_config(page_title="Live Market Tracker",layout='wide')
col1,col2= st.columns(2)
st.sidebar.title("⚙️Access Tools")
with col1:
    st.image(image='stock.png',width =300)
with col2:
    st.markdown("""
                <div style='background: linear-gradient(to right, #000066,#660066); padding:30px; border-radius:10px; text-align:center;'>
                    <h1 style='font-size:45px;'>📊 Live Market Tracker</h1>
                    <p style='font-size:20px;'>Real-time stats to give you the edge 🔥</p>
                </div>
                """, unsafe_allow_html=True)
st.divider( width="stretch")
st.success(body='Successfuly Connected and Fetching Data from NSE',icon='🛜')
c1,c2,c3 = st.columns(3)
nif5 = n.live_index("NIFTY 50")['metadata']
nifb = n.live_index("NIFTY BANK")['metadata']
rel = n.stock_quote("RELIANCE")['priceInfo']

c1.metric(border=True,label=nif5['indexName'],value=nif5['last'],delta=round(nif5['change'],3))
c2.metric(border=True,label=nifb['indexName'],value=nifb['last'],delta=round(nifb['change'],3))
c3.metric(border=True,label="RELIANCE",value=rel['lastPrice'],delta=round(rel['change'],4))

st.divider(width='stretch')
