# import xlwings
# import pandas as pd
# import plotly.express as px

# from tabulate import tabulate
# # Python3 code to select
# # data from excel
# import xlwings as xw
# import math
#
# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", 1000)
# pd.set_option("display.width", 1000)
#
# # from prophet.plot import plot_plotly
# # from plotly import graph_objects as go
#
import streamlit as st
import pandas as pd
import plotly.express as px
import copy



st.set_page_config(page_title="ZERODHA",page_icon="🌍",layout="wide")



theme_plotly = None # None or streamlit

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

def read_file_csv_Excel(file):
    """
    Read and return DataFrame based on file type (CSV or Excel).
    """
    if file is not None:
        file_extension = file.name.split('.')[-1].lower()
        if file_extension == 'csv':
            df = pd.read_csv(file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(file, engine='openpyxl')
        else:
            st.warning("Please upload a CSV or Excel file.")
            return None
        return df


def uploaded_file():
    st.title("CSV and Excel File Uploader")

    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

    if uploaded_file is not None:
        st.subheader("File Content:")

        # Read and display the contents of the uploaded file
        df = read_file_csv_Excel(uploaded_file)
        return df


read_file = uploaded_file()


def data_analist( symbol_df_isin, symbol):
    df = pd.DataFrame( symbol_df_isin)
    df["Invested"] = df['quantity'] * df['price']

    df.sort_values('symbol', axis=0, ascending=True, inplace=True)
    df.sort_values('order_execution_time', axis=0, ascending=True, inplace=True)

    # print(df.head(5))
    entry_list = []
    entry_buy_df = df.loc[(df["symbol"] == str(symbol))]
    entry_buy_df.reset_index(inplace=True, drop=True)
    DATE_LIST = entry_buy_df.index

    # print( entry_buy_df.head(100))
    entry_buy = {"trade_date": None, 'symbol': None, 'trade_type': None, 'Entry': None, 'quantity': 0, "Buy_avg": 0.00,
                 "Buy_valu": 0.00,"Qtt_BUY": 0.00, "Sell_avg": 0.00, "sell_value": 0.00, 'Qtt_sell': 0, "CHANG": 0.00,
                 "PNL": 0.00, "PNL_Total": 0.00, 'sell_quantity': 0.00, 'Invested': 0., "Invested_sell": 0.00}
    for date in DATE_LIST:
        entry_buy["trade_date"] = entry_buy_df.iloc[date, entry_buy_df.columns.get_loc('trade_date')]
        entry_buy["symbol"] = symbol
        entry_buy["trade_type"] = entry_buy_df.iloc[date, entry_buy_df.columns.get_loc('trade_type')]
        entry_buy["Entry"] = entry_buy_df.iloc[date, entry_buy_df.columns.get_loc('price')]
        if entry_buy["trade_type"] == "buy":
            entry_buy["Qtt_BUY"] = entry_buy_df.iloc[date, entry_buy_df.columns.get_loc('quantity')] + entry_buy[
                "Qtt_BUY"]
            entry_buy["Buy_valu"] = entry_buy["Buy_valu"] + entry_buy_df.iloc[
                date, entry_buy_df.columns.get_loc("Invested")]
            entry_buy['quantity'] = entry_buy_df.iloc[date, entry_buy_df.columns.get_loc('quantity')]
            entry_buy["Invested"] = float(entry_buy_df.iloc[date, entry_buy_df.columns.get_loc("Invested")])
            entry_buy["Buy_avg"] = entry_buy["Buy_valu"] / entry_buy["Qtt_BUY"]
            entry_buy["CHANG"] = 0.00
            entry_buy["PNL"] = 0.00
        else:
            entry_buy['Qtt_sell'] = entry_buy_df.iloc[date, entry_buy_df.columns.get_loc('quantity')] + entry_buy[
                'Qtt_sell']
            if entry_buy["Buy_valu"] == 0:
                entry_buy["Buy_avg"] = 0.00

            else:
                entry_buy["Buy_avg"] = entry_buy["Buy_valu"] / entry_buy["Qtt_BUY"]

            entry_buy['quantity'] = entry_buy_df.iloc[date, entry_buy_df.columns.get_loc('quantity')]
            entry_buy['sell_value'] = entry_buy['sell_value'] + entry_buy_df.iloc[date, entry_buy_df.columns.get_loc("Invested")]

            entry_buy['sell_quantity'] = entry_buy_df.iloc[date, entry_buy_df.columns.get_loc('quantity')]

            entry_buy["Sell_avg"] = entry_buy['sell_value'] / entry_buy['Qtt_sell']

            if entry_buy["Buy_avg"] == 0:
                entry_buy["Buy_avg"] = None
            else:
               entry_buy["CHANG"] = entry_buy["Sell_avg"] - entry_buy["Buy_avg"]


            entry_buy["PNL"] = (entry_buy["CHANG"] * entry_buy['Qtt_sell']) - entry_buy["PNL_Total"]
            entry_buy["PNL_Total"] = entry_buy["CHANG"] * entry_buy['Qtt_sell']
            entry_buy["Invested_sell"] = float(entry_buy_df.iloc[date, entry_buy_df.columns.get_loc("Invested")])
        entry_list.append(copy.deepcopy((entry_buy)))
        # print(pd.DataFrame(entry_list))
    entry_buy_pd = pd.DataFrame(entry_list)
    # print(pd.DataFrame(entry_list).round(2))
    return entry_buy_pd


def data_analist_all(data):
    isin_list = data["isin"].unique()
    all_market = []
    for isin in isin_list:
        symbol_df_isin = data.loc[(data['isin'] == isin)]
        symbol =  symbol_df_isin.iloc[0,  symbol_df_isin.columns.get_loc("symbol")]
        df = data_analist( symbol_df_isin= symbol_df_isin, symbol=symbol)
        all_market.append(df)

    appended_all_market = pd.concat(all_market, ignore_index=True)
    # print(appended_all_market)
    return appended_all_market


def data_total_all(data):
    isin_list = tradebook["isin"].unique()
    all_market = []

    data_total= {"trade_date": None, 'symbol': None, 'trade_type': None, 'Entry': None, 'quantity': 0, "Buy_avg": 0.00,
                 "Buy_valu": 0.00,"Qtt_BUY": 0.00, "Sell_avg": 0.00, "sell_value": 0.00, 'Qtt_sell': 0, "CHANG": 0.00,
                 "PNL": 0.00, "PNL_Total": 0.00, 'sell_quantity': 0.00, 'Invested': 0., "Invested_sell": 0.00}
    for isin in isin_list:
        symbol_df_isin = tradebook.loc[(tradebook['isin'] == isin)]
        symbol = symbol_df_isin .iloc[0, symbol_df_isin .columns.get_loc("symbol")]
        data = data_analist( symbol_df_isin =  symbol_df_isin , symbol=symbol)
        # print(data.tail(5))
        buy_df = data.loc[(data['trade_type'] == "buy")]
        sell_df = data.loc[(data['trade_type'] == "sell")]
        if buy_df['quantity'].sum() > 0 and sell_df['quantity'].sum() > 0:
            data_total['trade_date'] = sell_df.iloc[len(sell_df) - 1, sell_df.columns.get_loc('trade_date')]
            data_total["symbol"] = sell_df.iloc[0,  sell_df.columns.get_loc('symbol')]
            data_total['trade_type'] = sell_df.iloc[0,  sell_df.columns.get_loc('trade_type')]
            data_total["Entry"] = buy_df.iloc[0, data.columns.get_loc('Entry')]
            data_total['quantity'] = sell_df['quantity'].sum()
            data_total["Buy_valu"] = buy_df['Invested'].sum()
            data_total["Qtt_BUY"] = buy_df['quantity'].sum()
            data_total["Buy_avg"] = data_total["Buy_valu"] / data_total["Qtt_BUY"]

            data_total["sell_value"] = sell_df['Invested_sell'].sum()
            data_total["Qtt_sell"] = sell_df['quantity'].sum()
            data_total["Sell_avg"] = data_total["sell_value"] / data_total["Qtt_sell"]

            data_total["CHANG"] = data_total["Sell_avg"] - data_total["Buy_avg"]
            data_total["PNL"] = data_total["CHANG"] * data_total["Qtt_sell"]
            data_total["PNL_Total"] = data_total["CHANG"] * data_total["Qtt_sell"]
            data_total["Parsent"] = (data_total["PNL_Total"] / data_total["Buy_valu"]) * 100
            data_total["Invested"] = buy_df['Invested'].sum()
            data_total["Invested_sell"] = sell_df['Invested'].sum()


            if data_total["Qtt_BUY"] == 0:
                print(buy_df['quantity'].sum())
                print(data_total)
                breakpoint()
            all_market.append(copy.deepcopy((data_total)))
        #
        # print(pd.DataFrame(all_market))
        # breakpoint()
    data_total_pd = pd.DataFrame(all_market).round(2)

    data_total_pd.sort_values('trade_date', axis=0, ascending=True, inplace=True)
    data_total_pd = pd.DataFrame(data_total_pd)
    data_total_pd["PNL_cumsum"] = data_total_pd['PNL_Total'].cumsum()
    data_total_pd.reset_index(inplace=True, drop=True)
    return data_total_pd
tradebook = pd.DataFrame(read_file)


if not len(tradebook):
    tradebook = pd.read_excel('tradebook-LG5706-EQ 1-1-2022.xlsx', engine='openpyxl')
    tradebook = pd.DataFrame(tradebook)

tradebook['symbol'] = tradebook['symbol'].str.rsplit("-").str[0]

# ff = tradebook.loc[(tradebook['isin'] == "INE699H01024")]
# # tradebook['symbol'] = tradebook['symbol'].str.rsplit("-", 1).str[-1]
#
#
# print(ff)



Book_NAME = "data_NSC_ALL2.xlsx"


# def print_sheets(df, sheets_name, range):
#     ws = xlwings.Book(Book_NAME).sheets(sheets_name)
#     ws.range(range).value = pd.DataFrame(df.round(2))
# def exl_sheets_clear(sheets_name):
#     ws = xlwings.Book(Book_NAME).sheets(sheets_name)
#     ws.clear()

# exl_sheets_clear(sheets_name="Adj Close")
# print_sheets(df=df, sheets_name="Adj Close", range="A1")

def convert_df(df, file_name):
    csv1 = df.to_csv().encode("utf-8")
    st.download_button(
        label="Download data as CSV",
        data=csv1,
        file_name=file_name,
        mime="text/csv",key=f"{csv1}") )
    return
def dataframe_columns(list):

    dataframe_columns_list = list.columns.values.tolist()
    return dataframe_columns_list
def line_chart(data, title):
    st.line_chart(data)
    st.title(title)


def dataframe(dataframe_df, default, trade_type, symbol):
    global df_selec
    if symbol:
        dataframe_df = dataframe_df.loc[(dataframe_df['symbol'] == symbol)]
    else:
        dataframe_df = dataframe_df

    if trade_type == 'buy':
        df_selec = dataframe_df.loc[(dataframe_df['trade_type'] == "buy")]
    if trade_type == "sell":
        df_selec = dataframe_df.loc[(dataframe_df['trade_type'] == "sell")]
    if trade_type == 'buy/sell':
        df_selec = dataframe_df
    PNL_Total =dataframe_df['PNL'].sum()
    st.title("# :red[ZERODHA ]")
    st.title(f"#:red[ SYMBOL-------{symbol}--------Rs.{round(PNL_Total,2)}]")

    st.line_chart(dataframe_df, x='trade_date', y='PNL_Total')

    df_selec.reset_index(inplace=True, drop=True)
    df_selec = df_selec.round(2)
    showData = st.multiselect('Filter: ', dataframe_df.columns,key=f'filter_{df_selec}', default=default)
    st.dataframe(df_selec[showData], use_container_width=False, height=200, width=2000)
    convert_df(df=df_selec, file_name="MANOJ KUKNA.csv")
    return dataframe_df

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

    risk_df = risk_df.round(2)

    buy_df = risk_df.loc[(risk_df['trade_type'] == "buy")]
    sell_df = risk_df.loc[(risk_df['trade_type'] == "sell")]

    risk_dict["Invested"] = buy_df['Invested'].sum()
    risk_dict["Wins"] = len(sell_df.loc[(sell_df['PNL'] > 0)])
    risk_dict["Losser"] = len(sell_df.loc[(sell_df['PNL'] <= 0)])
    risk_dict["Nb_of_trade"] = risk_dict["Wins"] + risk_dict["Losser"]
    risk_dict["Profit"] = sell_df.loc[sell_df['PNL'] >= 0, "PNL"].sum()
    risk_dict["Loss"] = sell_df.loc[sell_df['PNL'] < 0, "PNL"].sum()
    risk_dict["Fees"] = risk_dict["Nb_of_trade"] * 15.96
    risk_dict["RR"] =round(risk_dict["Profit"] / abs(risk_dict["Loss"]), 2) if abs(risk_dict["Loss"]) != 0 else 0
    risk_dict["Avg_Winner"] = risk_dict["Profit"] / risk_dict["Nb_of_trade"]
    risk_dict["Avg_Loser"] = risk_dict["Loss"] / risk_dict["Nb_of_trade"]
    risk_dict["Bigges_Winner"] = sell_df["PNL"].max()
    risk_dict["Bigges_Loser"] = sell_df["PNL"].min()
    risk_dict["Buy_avg"] = risk_dict["Invested"] / float(buy_df['quantity'].sum())
    risk_dict["Qtt_Buy"] = float(buy_df['quantity'].sum())
    risk_dict["sell_value"] = float(buy_df['quantity'].sum())
    risk_dict["Sell_quantity"] = float(sell_df['quantity'].sum())

    risk_dict["Sell_avg"] = risk_dict["sell_value"] / float(sell_df['quantity'].sum())
    risk_dict["PNL_Total"] = (risk_dict["Profit"] + risk_dict["Loss"]) #-risk_dict["Fees"]
    risk_dict["PNL_Total_parsent"] = round(risk_dict["PNL_Total"] / risk_dict["Invested"] * 100, 2)
    risk_dict["Avg_Return"] = risk_dict["PNL_Total"] / risk_dict["Nb_of_trade"]

    risk_list.append(copy.deepcopy((risk_dict)))
    risk_list_pd = pd.DataFrame(risk_list)
    # print(risk_list)
    # print(risk_list_pd)
    return risk_dict


def metric_label(risk_dict):
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
        pie_df = pie_df.loc[(pie_df["symbol"] == symbol) & (pie_df["trade_type"] == "sell")]
        names= 'PNL'
    else:
        pie_df = pie_df.loc[(pie_df["trade_type"] == "sell")]
        names = "symbol"
    Profit = pie_df.loc[pie_df['PNL'] >= 0, "PNL"].sum()
    Profit_pie = pie_df.loc[pie_df['PNL'] >= 0]
    fig = px.pie(Profit_pie, values='PNL',names=names, title=f"Pofit_piy_chaty = Rs. {round(Profit,2)}")
    fig.update_layout(legend_title='Profit value', legend_y=0.9)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
def Loss_pie(pie_df, symbol):
    pie_df = pd.DataFrame(pie_df)
    if symbol:
        pie_df = pie_df.loc[(pie_df["symbol"] == symbol) & (pie_df["trade_type"] == "sell")]
        names = 'PNL'
    else:
        pie_df = pie_df.loc[(pie_df["trade_type"] == "sell")]
        names = "symbol"
    Loss = pie_df.loc[pie_df['PNL'] < 0, "PNL"].sum()
    Loss_pie = pie_df.loc[pie_df['PNL'] < 0]
    Loss_pie =pd.DataFrame(Loss_pie)
    Loss_pie['PNL'] = Loss_pie['PNL'].abs()
    fig = px.pie(Loss_pie, values='PNL', names=names, title=f"Loss_piy_chaty = Rs. {round(Loss,2)}")
    fig.update_layout(legend_title='Loss value', legend_y=0.9)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


data_analist_all = data_analist_all(data=tradebook)

# exl_sheets_clear(sheets_name="Adj Close")
# print_sheets(df=df, sheets_name="Adj Close", range="A1")


unique_tickers = tradebook
unique_tickers.sort_values('symbol', axis=0, ascending=True, inplace=True)


st.sidebar.image("logo1.png",caption="Developed and Maintaned by: KUKAN MANOJ                          :      MO ->8000594016")
st.sidebar.header("Please filter")
stock_tickers_trade_type = st.sidebar.selectbox('selected   selectbox   trade_type', ['buy/sell', 'buy', "sell"])
stock_tickers = st.sidebar.selectbox('selected  selectbox  symbol', unique_tickers["symbol"].unique())
st.sidebar.header("stock symbol_all Please filter")
stock_tickers_trade_type_ALL = st.sidebar.selectbox('selected   selectbox ', ['Buy/sell', 'Buy', "Sell"])

metric_label(risk_dict=risk_management(risk_df=data_analist_all,symbol=stock_tickers))
left, right, = st.columns(2)  # center
with left:
    Profit_pie(pie_df=data_analist_all.round(2), symbol=stock_tickers)
with right:
    Loss_pie(pie_df=data_analist_all.round(2), symbol=stock_tickers)
df = dataframe(dataframe_df=data_analist_all,
          default=dataframe_columns(list=data_analist_all),
          trade_type=stock_tickers_trade_type,
          symbol=stock_tickers)


metric_label(risk_dict=risk_management(risk_df=data_analist_all, symbol=None))
left, right, = st.columns(2)  # center
with left:
    Profit_pie(pie_df=data_analist_all.round(2), symbol=None)
with right:
    Loss_pie(pie_df=data_analist_all.round(2), symbol=None)

df2 = dataframe(dataframe_df=data_analist_all,
          default=dataframe_columns(list=data_analist_all),
          trade_type=stock_tickers_trade_type,
          symbol=None)






# janral zorhodh
#  JANRAL ZERODHA
# streamlit run ZERODHA.py
