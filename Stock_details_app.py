import requests
import pandas as pd
import json
import streamlit as st
import plotly.graph_objects as go


def get_coin_data(coin_type: str, date_range: str) -> requests.Response:
    url = f"https://api.coingecko.com/api/v3/coins/{coin_type}/market_chart?vs_currency=usd&days={date_range}&interval=daily"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-KTWn3G39ejfyiRjSS84MBmnT"
    }
    response = requests.get(url, headers=headers)
    st.session_state.response = response
    st.session_state.url = url
    return response

def create_df(response_text: str) -> pd.DataFrame:
    data = json.loads(response_text)
    prices_df = pd.DataFrame(data['prices'], columns=['Timestamp', 'Price'])
    market_caps_df = pd.DataFrame(data['market_caps'], columns=['Timestamp', 'Market_Cap'])
    total_volumes_df = pd.DataFrame(data['total_volumes'], columns=['Timestamp', 'Total_Volume'])
    merged_df = prices_df.merge(market_caps_df, on='Timestamp').merge(total_volumes_df, on='Timestamp')
    merged_df['Timestamp'] = pd.to_datetime(merged_df['Timestamp'], unit='ms')
    return merged_df



if __name__ == '__main__':
    st.title("Crypto price tracker")
    user_input = st.text_input("Enter the coin you want to look for")
    if st.button("Get", on_click= get_coin_data, kwargs={"coin_type":user_input, "date_range":"364"}):

        if st.session_state.response.status_code == 404:
            st.write("coin does not exist, try enter again")

        elif st.session_state.response.status_code == 200:
            bitcoin_df = create_df(st.session_state.response.text)

            max_price_index = bitcoin_df['Price'].idxmax()
            max_price_timestamp = bitcoin_df.loc[max_price_index, 'Timestamp']
            max_price = bitcoin_df.loc[max_price_index, 'Price']

            min_price_index = bitcoin_df['Price'].idxmin()
            min_price_timestamp = bitcoin_df.loc[min_price_index, 'Timestamp']
            min_price = bitcoin_df.loc[min_price_index, 'Price']

            max_trade_index = bitcoin_df['Total_Volume'].idxmax()
            max_trade_timestamp = bitcoin_df.loc[max_trade_index, 'Timestamp']
            max_trade_price = bitcoin_df.loc[max_trade_index, 'Price']
            max_trade = bitcoin_df.loc[max_trade_index, 'Total_Volume']

            min_trade_index = bitcoin_df['Total_Volume'].idxmin()
            min_trade_timestamp = bitcoin_df.loc[min_trade_index, 'Timestamp']
            min_trade_price = bitcoin_df.loc[min_trade_index, 'Price']
            min_trade = bitcoin_df.loc[min_trade_index, 'Total_Volume']

            # Add trace for prices
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(x=bitcoin_df['Timestamp'], y=bitcoin_df['Price'], mode='lines+markers+text', name='Price',
                        textposition="top center"))

            fig.add_trace(
                go.Scatter(x=[max_price_timestamp], y=[max_price], mode='markers+text', marker=dict(color='red', size=10),
                           name='Highest Price', text=[f"${max_price/1000:.2f}k"], textposition="top center"))
            fig.add_trace(
                go.Scatter(x=[min_price_timestamp], y=[min_price], mode='markers+text', marker=dict(color='black', size=10),
                           name='Lowest Price', text=[f"${min_price/1000000:.2f}m"], textposition="top center"))

            fig.add_trace(
                go.Scatter(x=[max_trade_timestamp], y=[max_trade_price], mode='markers+text', marker=dict(symbol='triangle-up', color='orange', size=15),
                           name='Highest Trading Volume', text=[f"${max_trade/1000000:.2f}m"], textposition="top center"))
            fig.add_trace(
                go.Scatter(x=[min_trade_timestamp], y=[min_trade_price], mode='markers+text', marker=dict(symbol='triangle-up', color='green', size=15),
                           name='Lowest Trading Volume', text=[f"${min_trade/1000000:.2f}m"], textposition="top center"))

            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Price"
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("error code: " +  st.session_state.response.status_code)
