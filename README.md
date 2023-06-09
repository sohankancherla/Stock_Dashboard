# Stock Dashboard (WIP)
This program is a stock dashboard that helps you get real-time information about different stocks. You can enter the stock symbol that you're interested in, and the dashboard will gather a variety of information about that stock. This information includes the closing prices, earning dates, market cap, 3-month treasury rate, and S&P 500 closing price. All of this data is then compiled into a CSV file that you can download and access later.

![image](https://user-images.githubusercontent.com/30853467/228386850-e442a62b-24c1-4a1a-93b1-c16f6d65f717.png)


# How to Run
- replace fredapi with your own key (https://fred.stlouisfed.org/docs/api/fred/)
- cmd: streamlit run stock_dashboard.py

# Upcoming Features
- Data Visualizations: The Dashboard will include a multitude of graphs and visualizations to help users understand the data visually
- Insider Trading Detector: The main goal of this program is to identify which companies and when insider trading happens

# APIs and Libraries
- Fred API to get the 3 month treasury rate
- yfinance to get realtime stock data
- strealit to build the dashboard
