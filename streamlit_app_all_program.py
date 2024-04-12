import requests
import pandas as pd
import json
import streamlit as st
import plotly.graph_objects as go
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np



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
    """
    This is to plot the df and
    """
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

def predict_image(input_image):
    image = input_image.resize((28, 28))
    model = tf.keras.models.load_model("final_model.h5")
    if image.mode == 'RGBA':
        white_canvas = Image.new('RGB', image.size, '#aaa')
        white_canvas.paste(image, mask=image.split()[3])
        image = white_canvas
    st.write("Classifying...")
    image = image.convert('L')
    image = ImageOps.invert(image)
    img_inv = image.resize((28, 28))
    image_array = np.array(img_inv) / 255.0
    image_array = image_array.reshape((1, 28, 28, 1))

    my_prediction = model.predict(image_array)
    predicted_class = np.argmax(my_prediction)
    return predicted_class


def question_1():
    st.title("Crypto price tracker")
    user_input = st.text_input("Enter the coin you want to look for").lower()
    if st.button("Get"):
        response = get_coin_data(user_input, 364)

        if response.status_code == 404:
            st.write("coin does not exist, try enter again")

        elif response.status_code == 200:
            bitcoin_df = create_df(response.text)

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
                           name='Highest Price', text=[f"${max_price:.2f}$"], textposition="top center"))
            fig.add_trace(
                go.Scatter(x=[min_price_timestamp], y=[min_price], mode='markers+text', marker=dict(color='black', size=10),
                           name='Lowest Price', text=[f"${min_price:.2f}$"], textposition="top center"))

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


def question_2():
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
        options = {"1 week": 7, "1 month": 30, "1 year": 364}
        plot_type = st.radio("Select Plot Type", options)
        fig = go.Figure()
        plot_df(options[plot_type], fig)
        st.plotly_chart(fig, use_container_width=True)
        st.write("Enther another coin and fetch again!")
        if st.button("Clear Data"):
            clear_data_and_reset()

def question_3():
    st.title("Digit Guess App")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        prediction = predict_image(img)
        st.write(f"The machine think this number is {prediction}")
        st.image(img, caption="Uploaded Image", use_column_width=True)



if __name__ == "__main__":
    app_choice = st.sidebar.radio("Choose Application",
                                  ["Crypto price tracker", "Crypto Price Compare", "Digit Guess App"])

    if app_choice == "Crypto price tracker":
        question_1()


    elif app_choice == "Crypto Price Compare":
        question_2()


    elif app_choice == "Digit Guess App":
        question_3()
