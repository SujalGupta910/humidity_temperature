import streamlit as st
from serial_reader import SerialReader
from plotter import plot_data
import time

# SET COM PORT HERE or autodetect
PORT = "COM3"

st.set_page_config(page_title="DHT11 Dashboard", layout="wide")
st.title("🌡️ DHT11 Temperature & Humidity Dashboard")

reader = SerialReader(PORT)
reader.start()

placeholder = st.empty()

try:
    while True:
        with placeholder.container():
            plot_data(reader.data)
        time.sleep(1)
except KeyboardInterrupt:
    reader.stop()
