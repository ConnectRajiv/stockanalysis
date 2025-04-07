import streamlit as st
import datetime as dt
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def display_fundamental_analysis(ticker):
    st.title('Fundamental Analysis')

    stock = yf.Ticker(ticker)
    info = stock.info

    st.subheader('Company Profile')
    st.markdown('**Name**: ' + (info['longName'] if 'longName' in info else 'N/A'))
    st.markdown('**Sector**: ' + (info['sector'] if 'sector' in info else 'N/A'))
    st.markdown('**Industry**: ' + (info['industry'] if 'industry' in info else 'N/A'))
    st.markdown('**Phone**: ' + (info['phone'] if 'phone' in info else 'N/A'))
    st.markdown('**Address**: ' + (info['address1'] if 'address1' in info else 'N/A') + ', ' +
                (info['city'] if 'city' in info else 'N/A') + ', ' +
                (info['zip'] if 'zip' in info else 'N/A') + ', ' +
                (info['country'] if 'country' in info else 'N/A'))
    st.markdown('**Website**: ' + (info['website'] if 'website' in info else 'N/A'))
    st.markdown('**Business Summary**')
    st.info(info['longBusinessSummary'] if 'longBusinessSummary' in info else 'N/A')

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
    st.markdown('**Exchange**: ' + (info['exchange'] if 'exchange' in info else 'N/A'))
    st.markdown('**Quote Type**: ' + (info['quoteType'] if 'quoteType' in info else 'N/A'))

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

