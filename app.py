import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 🌟 Page Style
st.set_page_config(page_title="📈 Stock Market Full Info + Prediction App", layout="wide")

# Page Title Center + Big
st.markdown(
    "<h1 style='text-align: center; color: #00BFFF;'>📈 Stock Market Full Info + Prediction App</h1><hr>", 
    unsafe_allow_html=True
)

# 🌗 Theme Selector
theme = st.selectbox(
    "Choose Theme:",
    ("Dark", "Light")
)

# Stock Symbol Input
stock = st.text_input("Stock ka symbol daalo (Example: AAPL, TCS.NS, INFY.NS):")

# Timeframe selection
timeframe = st.selectbox(
    "Select Timeframe:",
    ("5m", "10m", "15m", "1d", "1wk", "1mo")
)

# Period set according to interval
period_dict = {
    "5m": "1d",
    "10m": "1d",
    "15m": "5d",
    "1d": "6mo",
    "1wk": "2y",
    "1mo": "5y"
}
period = period_dict[timeframe]

if stock:
    stock_data = yf.Ticker(stock)

    try:
        hist_data = stock_data.history(period=period, interval=timeframe)

        if not hist_data.empty:
            # Calculate Moving Averages
            hist_data['MA50'] = hist_data['Close'].rolling(window=50).mean()
            hist_data['MA200'] = hist_data['Close'].rolling(window=200).mean()

            st.markdown("<h3 style='color:#FF5733;'>🕯️ Candlestick Chart</h3>", unsafe_allow_html=True)

            # Plot Candlestick with Moving Averages
            fig = go.Figure()

            fig.add_trace(go.Candlestick(
                x=hist_data.index,
                open=hist_data['Open'],
                high=hist_data['High'],
                low=hist_data['Low'],
                close=hist_data['Close'],
                name="Candlestick"
            ))

            fig.add_trace(go.Scatter(
                x=hist_data.index,
                y=hist_data['MA50'],
                mode='lines',
                name='50 MA',
                line=dict(color='blue', width=2)
            ))

            fig.add_trace(go.Scatter(
                x=hist_data.index,
                y=hist_data['MA200'],
                mode='lines',
                name='200 MA',
                line=dict(color='red', width=2)
            ))

            # 🔥 Theme Set according to user choice
            if theme == "Dark":
                selected_template = "plotly_dark"
                background_color = "#0e1117"
                font_color = "white"
            else:
                selected_template = "plotly_white"
                background_color = "white"
                font_color = "black"

            fig.update_layout(
                template=selected_template,
                plot_bgcolor=background_color,
                paper_bgcolor=background_color,
                font=dict(color=font_color),
                xaxis_title="Date",
                yaxis_title="Price",
                xaxis_rangeslider_visible=False,
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)

            # Company Info Section
            st.markdown("<h3 style='color:#FF5733;'>🏢 Company Information</h3>", unsafe_allow_html=True)
            info = stock_data.info
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"**Company Name:** {info.get('longName', 'N/A')}")
                st.info(f"**Country:** {info.get('country', 'N/A')}")
            with col2:
                st.warning(f"**Sector:** {info.get('sector', 'N/A')}")
                st.error(f"**Industry:** {info.get('industry', 'N/A')}")

            st.markdown("---")

            # Download Button Stylish
            st.download_button(
                label="📥 Download Historical Data",
                data=hist_data.to_csv().encode('utf-8'),
                file_name=f'{stock}_data.csv',
                mime='text/csv',
                key='download-csv',
                help="Download the stock historical data CSV file"
            )

            # Prediction Idea (Simple Moving Average Cross)
            st.markdown("<h3 style='color:#FF5733;'>📈 Simple Stock Prediction (Basic)</h3>", unsafe_allow_html=True)

            prediction = ""
            if hist_data['MA50'].iloc[-1] > hist_data['MA200'].iloc[-1]:
                prediction = "Bullish Trend Expected 📈"
            else:
                prediction = "Bearish Trend Expected 📉"

            st.info(prediction)

        else:
            st.error("⚠️ Data nahi mila! Check karo stock symbol ya interval settings.")

    except Exception as e:
        st.error(f"Kuch galti hui: {e}")

else:
    st.warning("👆 Pehle stock ka symbol daalo.")
