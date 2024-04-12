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
    return response


def create_df(response_text: str) -> pd.DataFrame:
    data = json.loads(response_text)
    prices_df = pd.DataFrame(data['prices'], columns=['Timestamp', 'Price'])
    market_caps_df = pd.DataFrame(data['market_caps'], columns=['Timestamp', 'Market_Cap'])
    total_volumes_df = pd.DataFrame(data['total_volumes'], columns=['Timestamp', 'Total_Volume'])
    merged_df = prices_df.merge(market_caps_df, on='Timestamp').merge(total_volumes_df, on='Timestamp')
    merged_df['Timestamp'] = pd.to_datetime(merged_df['Timestamp'], unit='ms')
    return merged_df


def add_df(random_stuff):
    st.session_state.dfs.append(random_stuff)


def plot_df(type, fig):
    if type < 300:
        for each_df in st.session_state.dfs:
            checkbox_value = st.checkbox(each_df[1], value=True, key=each_df[1])
            if checkbox_value:
                fig.add_trace(go.Scatter(x=each_df[0].tail(type)['Timestamp'], y=each_df[0].tail(type)['Price'],
                                         mode='lines+markers+text',
                                         name=each_df[1], text=each_df[0].tail(type)['Price'], textposition="top center",
                                         texttemplate='%{text:.2f}', hovertext=each_df[1]))
    else:
        for each_df in st.session_state.dfs:
            checkbox_value = st.checkbox(each_df[1], value=True, key=each_df[1])
            if checkbox_value:
                fig.add_trace(go.Scatter(x=each_df[0].tail(type)['Timestamp'], y=each_df[0].tail(type)['Price'],
                                         mode='lines+markers',
                                         name=each_df[1], text=each_df[0].tail(type)['Price'], textposition="top center",
                                         texttemplate='%{text:.2f}', hovertext=each_df[1]))


def clear_data_and_reset():
    # Clear all session state variables
    st.session_state.clear()
    st.experimental_rerun()



if __name__ == '__main__':
    # Button to fetch data
    st.title("Crypto Price Compare")
    user_input = st.text_input("Enter the coin you want to look for").lower()

    if "dfs" not in st.session_state:
        st.session_state.dfs = []

    if st.button("Fetch Data"):
        response = get_coin_data(user_input, 364)
        if response.status_code == 404:
            st.write("coin does not exist, try enter again")

        elif response.status_code == 200:
            bitcoin_df = create_df(response.text)
            st.session_state.initial_data_fetched = True
            if not any(user_input == each_df[1] for each_df in st.session_state.dfs):
                st.session_state.dfs.append([bitcoin_df, user_input])
            else:
                st.write("coin already plotted")

        else:
            st.write("error code: " + response.status_code)

    if "initial_data_fetched" in st.session_state:
        options = {"1 week":7, "1 month":30, "1 year":364}
        plot_type = st.radio("Select Plot Type", options)
        fig = go.Figure()
        plot_df(options[plot_type], fig)
        st.plotly_chart(fig, use_container_width=True)
        st.write("Enther another coin and fetch again!")
        if st.button("Clear Data"):
            clear_data_and_reset()


