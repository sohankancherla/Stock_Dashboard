import pandas as pd
import yfinance as yf
import streamlit as st
import datetime
from fredapi import Fred


#get the closing stock prices
def get_stock_closing_prices(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    hist = stock.history(start=start_date, end=end_date)
    hist.index = hist.index.tz_localize(None)
    return hist['Close']

#update the csv with the next earning date
def find_next_earnings_date(row_date, earnings_dates):
    for ed in earnings_dates:
        if row_date < ed:
            return ed
    return None


# Replace 'your_api_key' with your FRED API key
fred = Fred(api_key='your_api_key')

#get the 3 month treasury rate from the fredapi
def get_treasury_rate(start_date, end_date):
    rates = fred.get_series('DTB3', start_date, end_date) / 100
    rates.index = pd.to_datetime(rates.index).tz_localize(None)  # Convert index to timezone-naive
    return rates

#MAIN CODE
st.title('Stock Dashboard')

symbol = st.text_input("Stock Symbol:")

#once user enters a stock symbol
if symbol:
    # Get Market Category
    stock = yf.Ticker(symbol)
    market_cap = stock.fast_info['marketCap']
    if market_cap < 200000000:
        st.write("Market Cap Category: Small Cap")
    elif market_cap < 100000000:
        st.write("Market Cap Category: Mid Cap")
    else:
        st.write("Market Cap Category: Large Cap")

    # Get Earnings' Dates
    earnings_calendar = stock.get_earnings_dates(limit=21).index.values[4:]
    next_earnings = earnings_calendar[0]
    last_earnings = str(earnings_calendar[-1]).split('T')[0]
    earnings_calendar = earnings_calendar[::-1]
    format_string = "%Y-%m-%d"
    dt = datetime.datetime.strptime(last_earnings, format_string)

    end_date = datetime.date.today()
    closing_prices = get_stock_closing_prices(symbol, dt, end_date)
    df = pd.DataFrame({'Closing Price': closing_prices})

    # Convert the earnings dates to datetime objects
    earnings_dates = [pd.to_datetime(ed).to_pydatetime().date() for ed in earnings_calendar]

    # Create the new column with the next earnings date
    df['Next Earnings Date'] = df.index.map(lambda x: find_next_earnings_date(x.date(), earnings_dates))

    # Get the S&P 500 closing prices
    sp500_closing_prices = get_stock_closing_prices('^GSPC', dt, end_date)
    sp500_df = pd.DataFrame({'S&P 500 Closing Price': sp500_closing_prices})

    # Merge the two DataFrames on their indices
    df = df.merge(sp500_df, left_index=True, right_index=True)

    # Get the 3-month Treasury rate
    treasury_rate = get_treasury_rate(dt, end_date)
    treasury_df = pd.DataFrame({'3-Month Treasury Rate': treasury_rate})

    # Merge the DataFrame
    df = df.merge(treasury_df, left_index=True, right_index=True, how='left')

    # Fill any missing Treasury rate data with the most recent available rate
    df['3-Month Treasury Rate'].fillna(method='ffill', inplace=True)

    # Download button to download the csv
    csv = df.to_csv(index=False).encode('utf-8-sig')
    button_label='Download Data as CSV'
    file_name = f'{symbol}_data.csv'
    st.download_button(label=button_label, data=csv, file_name=file_name, mime='text/csv')

    st.write(df)

