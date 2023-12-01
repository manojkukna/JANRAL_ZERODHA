import streamlit as st
import pandas as pd
import plotly.express as px
import copy

import time
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns",None)
pd.set_option("display.width",None)



st.set_page_config(page_title="JANRAL ZERODHA",page_icon="🌍",layout="wide")



theme_plotly = None # None or streamlit

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Set the background color to black
background_color = "#000000"
text_color = "#FFFFFF"  # Optional: Set text color to white for better visibility

# Apply custom styles using HTML and CSS
custom_styles = f"""
    <style>
        body {{color: {text_color};}}
        .stApp {{background-color: {background_color};}}
    </style>
"""
# Display the custom styles using markdown
st.markdown(custom_styles, unsafe_allow_html=True)

st.sidebar.markdown(custom_styles, unsafe_allow_html=True)



def header_selet(header_selet):
    entry_buy = {'symbol': None, "Entry_Date": None, 'Exit_Date': None, 'Qtt': None, "Buy_Value": 0,
                 "Sell_Value": 0.00, "Profit": 0.00, "cumsum": None}
    entry_list = []
    header = pd.DataFrame(header_selet)
    entry_buy_df2 = pd.DataFrame(header_selet)
    entry_buy_df = entry_buy_df2.fillna(value=0.00)
    index_lis = header.index.tolist()
    count = 1
    for index in index_lis:
        cadican = entry_buy_df.iloc[index, 1]
        if cadican == "Symbol" and entry_buy_df.iloc[index, 5] and count:
            for index_2 in index_lis[index:]:
                if not entry_buy_df.iloc[index_2, 5] == 'Quantity':
                    entry_buy["symbol"] = entry_buy_df.iloc[index_2, 1]
                    entry_buy["Entry_Date"] = entry_buy_df.iloc[index_2, 3]
                    entry_buy["Exit_Date"] = entry_buy_df.iloc[index_2, 4]
                    entry_buy["Qtt"] = entry_buy_df.iloc[index_2, 5]
                    entry_buy["Buy_Value"] = entry_buy_df.iloc[index_2, 6]
                    entry_buy["Sell_Value"] = entry_buy_df.iloc[index_2, 7]
                    entry_buy["Profit"] = entry_buy_df.iloc[index_2, 8]
                    if entry_buy["Qtt"]:
                        entry_list.append(copy.deepcopy((entry_buy)))
                    if not entry_buy["Qtt"]:
                        count = 0
                        break
    entry_buy_pd = pd.DataFrame(entry_list)
    return entry_buy_pd

def red_padas(tradebook,file_extension):
    red_padas1 = file_extension(tradebook)
    red_padas = header_selet(header_selet=red_padas1)
    return red_padas


def uploaded_file():
    uploaded_file = st.file_uploader("Choose a file", type=['xlsx', 'xls', 'xlsm', 'csv'])
    if uploaded_file is not None:
       # Check the file type and read accordingly
       if uploaded_file.name.endswith(('.xlsx', '.xls', '.xlsm')):
          df = red_padas(tradebook=uploaded_file,file_extension=pd.read_excel)
          return df
       elif uploaded_file.name.endswith('.csv'):
           # df = pd.read_csv(uploaded_file)
           df = red_padas(tradebook=uploaded_file,file_extension=pd.read_csv)
           return df
taxpnl = pd.DataFrame(uploaded_file())


if not len(taxpnl):
    taxpnl=red_padas(tradebook='taxpnl-LG5706-2023_2024-Q1-Q3.xlsx',file_extension=pd.read_excel)



# taxpnl1 =
# taxpnl = header_selet(header_selet=taxpnl1)




def risk_management(risk_df,symbol):

    if symbol:
        risk_df = risk_df.loc[(risk_df['symbol'] == symbol)]
    else:
        risk_df = risk_df
    risk_list = []
    risk_dict = {"Invested": None, "Wins": None, "Losser": None, "Nb_of_trade": None, "Profit": None, "Loss": None,
                           "Fees": 0.00, "RR": 0.00, "Avg_Winner": 0.00, "Avg_Loser": 0.00, "Bigges_Winner": 0.00,
                       "Bigges_Loser": 0.00, "Buy_avg": 0.00, "Qtt_Buy": 0, 'sell_value': 0.00, 'Sell_quantity': 0,
                        "Sell_avg": 0.00, "PNL_Total": 0.00,
                        "PNL_Total_parsent": 0.00, "Avg_Return": 0.00}

    risk_dict["Invested"] = risk_df['Buy_Value'].sum()
    risk_dict["Wins"] = len(risk_df.loc[(risk_df['Profit'] > 0)])
    risk_dict["Losser"] = len(risk_df.loc[(risk_df['Profit'] <= 0)])
    risk_dict["Nb_of_trade"] = risk_dict["Wins"] + risk_dict["Losser"]
    risk_dict["Profit"] = risk_df.loc[risk_df['Profit'] >= 0, 'Profit'].sum()
    risk_dict["Loss"] = risk_df.loc[risk_df['Profit'] < 0, 'Profit'].sum()
    risk_dict["Fees"] = risk_dict["Nb_of_trade"] * 15.96
    risk_dict["RR"] = round(risk_dict["Profit"] / abs(risk_dict["Loss"]), 2) if abs(risk_dict["Loss"]) != 0 else 0
    risk_dict["Avg_Winner"] = risk_dict["Profit"] / risk_dict["Nb_of_trade"]
    risk_dict["Avg_Loser"] = risk_dict["Loss"] / risk_dict["Nb_of_trade"]
    risk_dict["Bigges_Winner"] = risk_df['Profit'].max()
    risk_dict["Bigges_Loser"] = risk_df['Profit'].min()
    risk_dict["Buy_avg"] = risk_dict["Invested"] / float(risk_df["Qtt"].sum())
    risk_dict["sell_value"] = float(risk_df["Sell_Value"].sum())
    risk_dict["Sell_Qtt"] = float(risk_df["Qtt"].sum())
    risk_dict["Sell_avg"] = risk_dict["sell_value"] / float(risk_df["Qtt"].sum())
    risk_dict["PNL_Total"] = (risk_dict["Profit"] + risk_dict["Loss"]) #-risk_dict["Fees"]
    risk_dict["PNL_Total_parsent"] = round(risk_dict["PNL_Total"] / risk_dict["Invested"] * 100, 2)
    risk_dict["Avg_Return"] = risk_dict["PNL_Total"] / risk_dict["Nb_of_trade"]

    risk_list.append(copy.deepcopy((risk_dict)))
    risk_list_pd = pd.DataFrame(risk_list)
    # print(risk_list)
    # print(risk_list_pd)
    return risk_dict
def metric_label(risk_dict):
    from streamlit_extras.metric_cards import style_metric_cards

    total1, total2, total3, total4, total5, total6, total7 = st.columns(7, gap='large')
    with total2:
        st.metric(label="CAPITAL", value=f'{risk_dict["Invested"]:,.0f}')
    with total3:
        st.metric(label="Fees", value=f'{risk_dict["Fees"]:,.0f}')
    with total4:
        st.metric(label="RETURN ALL", value=f'{risk_dict["PNL_Total"]:,.0f}')
    with total5:
        st.metric(label="%RETURN ALL%", value=risk_dict["PNL_Total_parsent"])
    with total6:
        st.metric(label="R!R", value=f'1:{risk_dict["RR"]:,.0f}')

    total8, total9, total10, total11, total12, total13, total14 = st.columns(7, gap='large')

    with total8:
        st.metric(label="Nb_of_trade", value=f'{risk_dict["Nb_of_trade"]:,.0f}')
    with total9:
        st.metric(label="Wins", value=f'{risk_dict["Wins"]:,.0f}')
    with total10:
        st.metric(label="Losser", value=f'{ risk_dict["Losser"]:,.0f}')
    with total11:
        st.metric(label="%Win", value=f'{ risk_dict["Wins"] / risk_dict["Nb_of_trade"] * 100:,.0f}%')
    with total12:
        st.metric(label="%Losser", value=f'{ risk_dict["Losser"] / risk_dict["Nb_of_trade"] * 100:,.0f}%')
    with total13:
        st.metric(label="Profit", value=f'{risk_dict["Profit"]:,.0f}')
    with total14:
        st.metric(label="Loss", value=f'{risk_dict["Loss"]:,.0f}')
    style_metric_cards(background_color="#121270", border_left_color="#f20045", box_shadow="3px")

    total15, total16, total17, total18, total19, total20, total21 = st.columns(7, gap='large')

    with total16:
        st.metric(label="Avg_Return", value=f'{risk_dict["Avg_Return"]:,.0f}')
    with total17:
        st.metric(label="Avg_Winner", value=f'{ risk_dict["Avg_Winner"]:,.0f}')
    with total18:
        st.metric(label="Avg_Loser", value=f'{ risk_dict["Avg_Loser"]:,.0f}')
    with total19:
        st.metric(label="Bigges_Winner", value=f'{risk_dict["Bigges_Winner"]}')
    with total20:
        st.metric(label="Bigges_Loser", value=f'{ risk_dict["Bigges_Loser"]:,.0f}')
def Profit_pie(pie_df,symbol):
    pie_df = pd.DataFrame(pie_df)
    if symbol:
        pie_df = pie_df.loc[(pie_df["symbol"] == symbol)]
        names = 'Profit'
    else:
        pie_df = pie_df
        names = "symbol"
    Profit = pie_df.loc[pie_df['Profit'] >= 0, 'Profit'].sum()
    Profit_pie = pie_df.loc[pie_df['Profit'] >= 0]
    fig = px.pie(Profit_pie, values='Profit',names=names, title=f"Pofit_piy_chaty = Rs. {round(Profit,2)}")
    fig.update_layout(legend_title='Profit value', legend_y=0.9)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
def Loss_pie(pie_df, symbol):
    pie_df = pd.DataFrame(pie_df)
    if symbol:
        pie_df = pie_df.loc[(pie_df["symbol"] == symbol)]
        names = 'Profit'
    else:
        pie_df = pie_df
        names = "symbol"
    Loss = pie_df.loc[pie_df['Profit'] < 0, 'Profit'].sum()
    Loss_pie = pie_df.loc[pie_df['Profit'] < 0]
    Loss_pie =pd.DataFrame(Loss_pie)
    Loss_pie['Profit'] = Loss_pie['Profit'].abs()
    fig = px.pie(Loss_pie, values='Profit', names=names, title=f"Loss_piy_chaty = Rs. {round(Loss,2)}")
    fig.update_layout(legend_title='Loss value', legend_y=0.9)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


def convert_df(df, file_name):
    csv1 = df.to_csv().encode("utf-8")
    st.download_button(
        label="Download data as CSV",
        data=csv1,
        file_name=file_name,
        mime="text/csv",key=f"{csv1}")
    return
def dataframe_columns(list):
    dataframe_columns_list = list.columns.values.tolist()
    return dataframe_columns_list
def line_chart(data, title):
    st.line_chart(data)
    st.title(title)
def dataframe(dataframe_df, default, symbol):
    global df_selec
    if symbol:
        dataframe_df = dataframe_df.loc[(dataframe_df['symbol'] == symbol)]
    else:
        dataframe_df = dataframe_df

    dataframe_df = pd.DataFrame(dataframe_df)
    dataframe_df['cumsum'] = dataframe_df['Profit'].cumsum()


    PNL_Total =dataframe_df['Profit'].sum()

    if PNL_Total > 0:

        st.markdown("<h1 style='color: green;'>ZERODHA Rs</h1>", unsafe_allow_html=True)
        # st.title("# : green[ZERODHA ]")
        # st.title(f"#: green[ SYMBOL-------{symbol}--------Rs.{round(PNL_Total, 2)}]")
        #

    else:
        st.title("# :red[ZERODHA ]")
        st.title(f"#:red[ SYMBOL-------{symbol}--------Rs.{round(PNL_Total, 2)}]")
        # Set title color to green

    st.line_chart(dataframe_df, x='Entry_Date', y='cumsum')

    dataframe_df.reset_index(inplace=True, drop=True)
    showData = st.multiselect('Filter: ', dataframe_df.columns,key=f'filter_{dataframe_df}', default=default)
    st.dataframe(dataframe_df[showData], use_container_width=False, height=200, width=2000)
    convert_df(df=dataframe_df, file_name="MANOJ KUKNA.csv")
    return dataframe_df












# print(taxpnl)


unique_tickers = taxpnl
unique_tickers.sort_values('symbol', axis=0, ascending=True, inplace=True)

st.sidebar.image("ZORODHDA.png",caption="Developed and Maintaned by: KUKAN MANOJ                          :      MO ->8000594016")
st.sidebar.header("#Please filter")
stock_tickers = st.sidebar.selectbox('selected  selectbox  symbol', unique_tickers["symbol"].unique())




metric_label(risk_dict=risk_management(risk_df=taxpnl, symbol=None))
left, right, = st.columns(2)  # center
with left:
    Profit_pie(pie_df=taxpnl.round(2), symbol=None)
with right:
    Loss_pie(pie_df=taxpnl.round(2), symbol=None)

df2 = dataframe(dataframe_df=taxpnl,
          default=dataframe_columns(list=taxpnl),
          symbol=None)



metric_label(risk_dict=risk_management(risk_df=taxpnl, symbol=stock_tickers))

left, right, = st.columns(2)  # center
with left:
    Profit_pie(pie_df=taxpnl.round(2), symbol=stock_tickers)
with right:
    Loss_pie(pie_df=taxpnl.round(2), symbol=stock_tickers)
df = dataframe(dataframe_df=taxpnl,
          default=dataframe_columns(list=taxpnl),
          symbol=stock_tickers)




# janral zorhodh stock market journal  STOCK MARET JOURNAL        Z AI TECHNOLOGY
#   STOCK MARKET JANRAL
# streamlit run ZERODH_TAXPNL.py
