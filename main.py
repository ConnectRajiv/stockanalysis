import pandas as pd
import yfinance as yf
import streamlit as st
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import time


st.set_page_config(
    page_title="Stock Analysis - Prahlad",
    page_icon=":chart_with_upwards_trend:",  # You can change this to the path of your favicon
)

st.write("""
   <div style="padding: 10px; background-color: #8B0000; border-radius: 10px;">
   <h3 style="color: #FFFFFF;">Disclaimer</h3>
   <p style="color: #FFB6C1;">This project is for educational purposes only. Predictions made by machine learning models may not always be accurate and should not be used as the sole basis for making investment decisions. Always conduct thorough research and consult with financial professionals before investing in the stock and crypto market.</p>
   </div>
   """, unsafe_allow_html=True)

# Display loading message with yellow color, padding at the top, and centered text
st.write("<div style='padding-top: 10px; text-align: center; color: grey;'>This app may take some time to load, please wait...</div>", unsafe_allow_html=True)




nifty50_symbols = ["ADANIPORTS.NS", "ASIANPAINT.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS",
                   "BAJAJFINSV.NS", "BPCL.NS", "BHARTIARTL.NS", "BRITANNIA.NS",
                   "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS", "EICHERMOT.NS", "GAIL.NS", "GRASIM.NS",
                   "HCLTECH.NS", "HDFCBANK.NS", "HEROMOTOCO.NS", "HINDALCO.NS",
                   "HINDUNILVR.NS", "HDFCLIFE.NS", "ICICIBANK.NS", "ITC.NS", "IOC.NS", "INDUSINDBK.NS",
                   "INFY.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS", "M&M.NS", "MARUTI.NS",
                   "NTPC.NS", "NESTLEIND.NS", "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS",
                   "SBILIFE.NS", "SHREECEM.NS", "SBIN.NS", "SUNPHARMA.NS", "TCS.NS", "TATAMOTORS.NS",
                   "TATASTEEL.NS", "TECHM.NS", "TITAN.NS", "UPL.NS", "ULTRACEMCO.NS", "WIPRO.NS",
                   "ZEEL.NS"]

# Fetch data for NIFTY 50 stocks
end_date = dt.datetime.today().strftime('%Y-%m-%d')
nifty50_data = yf.download(nifty50_symbols, start="2000-01-01", end=end_date)

# Extracting Symbol, Name, and Sector
symbols = []
names = []
sectors = []

for symbol in nifty50_symbols:
    stock_info = yf.Ticker(symbol).info
    symbols.append(symbol)
    names.append(stock_info.get('longName', 'N/A'))
    sectors.append(stock_info.get('sector', 'N/A'))

# Combining into a DataFrame
nifty50_df = pd.DataFrame({'Symbol': symbols, 'Name': names, 'Sector': sectors})
symbols = nifty50_df['Symbol'].sort_values().tolist()


# # Display loading message
# st.info("This app will take some time to load, please wait...")


# ticker = st.selectbox(
#     'Choose a Nifty 50 Stock',
#     symbols)

# Adding padding at the top of the select box
st.write("""
    <div style="margin-top: 10px;">
    </div>
""", unsafe_allow_html=True)

ticker = st.selectbox(
    'Choose a Nifty 50 Stock',
    symbols
)

st.write("You selected:", ticker)
# st.write("<span style='color: green;'>You selected:</span>", ticker, unsafe_allow_html=True)


# infoType = st.sidebar.radio(
#     "Choose an info type",
#     ('Fundamental Analysis', 'Technical Analysis')
# )

# Check if the window width is greater than a certain threshold (e.g., for desktop view)
if st.sidebar.checkbox("Show Sidebar"):
    # Display sidebar content
    infoType = st.sidebar.radio(
        "Choose an info type",
        ('Fundamental Analysis', 'Technical Analysis')
    )
else:
    # Display content without sidebar for mobile view
    infoType = st.radio(
        "Choose an info type",
        ('Fundamental Analysis', 'Technical Analysis')
    )

stock = yf.Ticker(ticker)

if (infoType == 'Fundamental Analysis'):
    stock = yf.Ticker(ticker)
    info = stock.info
    # print(info)
    st.title('Company Profile')
    st.subheader(info['longName'])


    st.markdown('** Sector **: ' + (info['sector'] if 'sector' in info else 'N/A'))
    st.markdown('** Industry **: ' + (info['industry'] if 'industry' in info else 'N/A'))
    # st.markdown('** Phone **: ' + (info['phone'] if 'phone' in info else 'N/A'))
    # st.markdown(
    #     '** Address **: ' + (info['address1'] if 'address1' in info else 'N/A') + ', ' +
    #     (info['city'] if 'city' in info else 'N/A') + ', ' +
    #     (info['zip'] if 'zip' in info else 'N/A') + ', ' +
    #     (info['country'] if 'country' in info else 'N/A'))
    st.markdown('** Website **: ' + (info['website'] if 'website' in info else 'N/A'))
    st.markdown('** Business Summary **')
    # st.info(info['longBusinessSummary'] if 'longBusinessSummary' in info else 'N/A')

    # Assuming `info['longBusinessSummary']` contains the text
    text = info['longBusinessSummary'] if 'longBusinessSummary' in info else 'N/A'

    # Splitting text into sentences using regular expression
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

    # Selecting the first five sentences
    first_five_sentences = ' '.join(sentences[:4])

    # Displaying the first five sentences
    st.info(first_five_sentences)


    fundInfo = {
        'Enterprise Value (USD)': info.get('enterpriseValue', 'N/A'),
        'Enterprise To Revenue Ratio': info.get('enterpriseToRevenue', 'N/A'),
        'Enterprise To Ebitda Ratio': info.get('enterpriseToEbitda', 'N/A'),
        'Net Income (USD)': info.get('netIncomeToCommon', 'N/A'),
        'Profit Margin Ratio': info.get('profitMargins', 'N/A'),
        'Forward PE Ratio': info.get('forwardPE', 'N/A'),
        'PEG Ratio': info.get('pegRatio', 'N/A'),
        'Price to Book Ratio': info.get('priceToBook', 'N/A'),
        'Forward EPS (USD)': info.get('forwardEps', 'N/A'),
        'Beta ': info.get('beta', 'N/A'),
        'Book Value (USD)': info.get('bookValue', 'N/A'),
        'Dividend Rate (%)': info.get('dividendRate', 'N/A'),
        'Dividend Yield (%)': info.get('dividendYield', 'N/A'),
        'Five year Avg Dividend Yield (%)': info.get('fiveYearAvgDividendYield', 'N/A'),
        'Payout Ratio': info.get('payoutRatio', 'N/A')
    }

    fundDF = pd.DataFrame.from_dict(fundInfo, orient='index')
    fundDF = fundDF.rename(columns={0: 'Value'})
    st.subheader('Fundamental Info')
    st.table(fundDF)

    st.subheader('General Stock Info')
    st.markdown('** Exchange **: ' + (info['exchange'] if 'exchange' in info else 'N/A'))
    st.markdown('** Quote Type **: ' + (info['quoteType'] if 'quoteType' in info else 'N/A'))

    start = dt.datetime.today() - dt.timedelta(2 * 365)
    end = dt.datetime.today()
    df = yf.download(ticker, start, end)
    df = df.reset_index()
    fig = go.Figure(
        data=go.Scatter(x=df['Date'], y=df['Adj Close'])
    )
    fig.update_layout(
        title={
            'text': "Stock Prices Over Past Two Years",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    st.plotly_chart(fig, use_container_width=True)

    marketInfo = {
        "Volume": info.get('volume', 'N/A'),
        "Average Volume": info.get('averageVolume', 'N/A'),
        "Market Cap": info.get("marketCap", 'N/A'),
        "Float Shares": info.get('floatShares', 'N/A'),
        'Share Outstanding': info.get('sharesOutstanding', 'N/A')

    }

    marketDF = pd.DataFrame(data=marketInfo, index=[0])
    st.table(marketDF)

    start_date = dt.datetime.today() - dt.timedelta(2 * 365)
    historical_data = yf.download(ticker, start=start_date, end=end_date)

    # Calculate returns
    historical_data['Returns'] = historical_data['Adj Close'].pct_change() * 100

    # Plot returns
    fig_returns = go.Figure()
    fig_returns.add_trace(
        go.Scatter(x=historical_data.index, y=historical_data['Returns'], mode='lines', name='Returns'))
    fig_returns.update_layout(title='Stock Returns Over the Past Two Years', xaxis_title='Date',
                              yaxis_title='Returns (%)')
    st.plotly_chart(fig_returns, use_container_width=True)


    st.markdown("""
           <style>
           .author {
             font-size: 16px;
             text-align: center;
             margin-top: 30px;
             padding: 10px;
             border-radius: 10px;
           }
           .author a {
             color: #0077b5;
             text-decoration: none;
           }
           @media (prefers-color-scheme: light) {
             .author {
               background-color: #f5f5f5; /* Light mode background color */
             }
           }
           @media (prefers-color-scheme: dark) {
             .author {
               background-color: #333333; /* Dark mode background color */
             }
             .author a {
               color: #4dbdff; /* Dark mode link color */
             }
           }
           </style>
           """, unsafe_allow_html=True)

    st.markdown(
        '<p class="author">Author: Prahlad Pallav | <a href="https://www.linkedin.com/in/prahladpallav/" target="_blank">LinkedIn</a></p>',
        unsafe_allow_html=True)
else:
    def calcMovingAverage(data, size):
        df = data.copy()
        df['sma'] = df['Adj Close'].rolling(size).mean()
        df['ema'] = df['Adj Close'].ewm(span=size, min_periods=size).mean()
        df.dropna(inplace=True)
        return df


    def calc_macd(data):
        df = data.copy()
        df['ema12'] = df['Adj Close'].ewm(span=12, min_periods=12).mean()
        df['ema26'] = df['Adj Close'].ewm(span=26, min_periods=26).mean()
        df['macd'] = df['ema12'] - df['ema26']
        df['signal'] = df['macd'].ewm(span=9, min_periods=9).mean()
        df.dropna(inplace=True)
        return df


    def calcBollinger(data, size):
        df = data.copy()
        df["sma"] = df['Adj Close'].rolling(size).mean()
        df["bolu"] = df["sma"] + 2 * df['Adj Close'].rolling(size).std(ddof=0)
        df["bold"] = df["sma"] - 2 * df['Adj Close'].rolling(size).std(ddof=0)
        df["width"] = df["bolu"] - df["bold"]
        df.dropna(inplace=True)
        return df


    st.title('Technical Indicators')
    st.subheader('Moving Average')

    coMA1, coMA2 = st.columns(2)

    with coMA1:
        numYearMA = st.number_input('Insert period (Year): ', min_value=1, max_value=10, value=2, key=0)

    with coMA2:
        windowSizeMA = st.number_input('Window Size (Day): ', min_value=5, max_value=500, value=20, key=1)

    start = dt.datetime.today() - dt.timedelta(numYearMA * 365)
    end = dt.datetime.today()
    dataMA = yf.download(ticker, start, end)
    df_ma = calcMovingAverage(dataMA, windowSizeMA)
    df_ma = df_ma.reset_index()

    figMA = go.Figure()

    figMA.add_trace(
        go.Scatter(
            x=df_ma['Date'],
            y=df_ma['Adj Close'],
            name="Prices Over Last " + str(numYearMA) + " Year(s)"
        )
    )

    figMA.add_trace(
        go.Scatter(
            x=df_ma['Date'],
            y=df_ma['sma'],
            name="SMA" + str(windowSizeMA) + " Over Last " + str(numYearMA) + " Year(s)"
        )
    )

    figMA.add_trace(
        go.Scatter(
            x=df_ma['Date'],
            y=df_ma['ema'],
            name="EMA" + str(windowSizeMA) + " Over Last " + str(numYearMA) + " Year(s)"
        )
    )

    figMA.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    figMA.update_layout(legend_title_text='Trend')
    figMA.update_yaxes(tickprefix="Rs")

    st.plotly_chart(figMA, use_container_width=True)

    st.subheader('Moving Average Convergence Divergence (MACD)')
    numYearMACD = st.number_input('Insert period (Year): ', min_value=1, max_value=10, value=2, key=2)

    startMACD = dt.datetime.today() - dt.timedelta(numYearMACD * 365)
    endMACD = dt.datetime.today()
    dataMACD = yf.download(ticker, startMACD, endMACD)
    df_macd = calc_macd(dataMACD)
    df_macd = df_macd.reset_index()

    figMACD = make_subplots(rows=2, cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.01)

    figMACD.add_trace(
        go.Scatter(
            x=df_macd['Date'],
            y=df_macd['Adj Close'],
            name="Prices Over Last " + str(numYearMACD) + " Year(s)"
        ),
        row=1, col=1
    )

    figMACD.add_trace(
        go.Scatter(
            x=df_macd['Date'],
            y=df_macd['ema12'],
            name="EMA 12 Over Last " + str(numYearMACD) + " Year(s)"
        ),
        row=1, col=1
    )

    figMACD.add_trace(
        go.Scatter(
            x=df_macd['Date'],
            y=df_macd['ema26'],
            name="EMA 26 Over Last " + str(numYearMACD) + " Year(s)"
        ),
        row=1, col=1
    )

    figMACD.add_trace(
        go.Scatter(
            x=df_macd['Date'],
            y=df_macd['macd'],
            name="MACD Line"
        ),
        row=2, col=1
    )

    figMACD.add_trace(
        go.Scatter(
            x=df_macd['Date'],
            y=df_macd['signal'],
            name="Signal Line"
        ),
        row=2, col=1
    )

    figMACD.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="left",
        x=0
    ))

    figMACD.update_yaxes(tickprefix="Rs")
    st.plotly_chart(figMACD, use_container_width=True)

    st.subheader('Bollinger Band')
    coBoll1, coBoll2 = st.columns(2)
    with coBoll1:
        numYearBoll = st.number_input('Insert period (Year): ', min_value=1, max_value=10, value=2, key=6)

    with coBoll2:
        windowSizeBoll = st.number_input('Window Size (Day): ', min_value=5, max_value=500, value=20, key=7)

    startBoll = dt.datetime.today() - dt.timedelta(numYearBoll * 365)
    endBoll = dt.datetime.today()
    dataBoll = yf.download(ticker, startBoll, endBoll)
    df_boll = calcBollinger(dataBoll, windowSizeBoll)
    df_boll = df_boll.reset_index()
    figBoll = go.Figure()
    figBoll.add_trace(
        go.Scatter(
            x=df_boll['Date'],
            y=df_boll['bolu'],
            name="Upper Band"
        )
    )

    figBoll.add_trace(
        go.Scatter(
            x=df_boll['Date'],
            y=df_boll['sma'],
            name="SMA" + str(windowSizeBoll) + " Over Last " + str(numYearBoll) + " Year(s)"
        )
    )

    figBoll.add_trace(
        go.Scatter(
            x=df_boll['Date'],
            y=df_boll['bold'],
            name="Lower Band"
        )
    )

    figBoll.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="left",
        x=0
    ))

    figBoll.update_yaxes(tickprefix="Rs")
    st.plotly_chart(figBoll, use_container_width=True)

    st.markdown("""
       <style>
       .author {
         font-size: 16px;
         text-align: center;
         margin-top: 30px;
         padding: 10px;
         border-radius: 10px;
       }
       .author a {
         color: #0077b5;
         text-decoration: none;
       }
       @media (prefers-color-scheme: light) {
         .author {
           background-color: #f5f5f5; /* Light mode background color */
         }
       }
       @media (prefers-color-scheme: dark) {
         .author {
           background-color: #333333; /* Dark mode background color */
         }
         .author a {
           color: #4dbdff; /* Dark mode link color */
         }
       }
       </style>
       """, unsafe_allow_html=True)

    st.markdown(
        '<p class="author">Author: Prahlad Pallav | <a href="https://www.linkedin.com/in/prahladpallav/" target="_blank">LinkedIn</a></p>',
        unsafe_allow_html=True)
