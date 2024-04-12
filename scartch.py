import streamlit as st

options = {
    "Option 1": "value1",
    "Option 2": "value2",
    "Option 3": "value3"
}

selected_option = st.radio("Select an option:", options)

st.write("Selected option:", options[selected_option])