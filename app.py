import streamlit as st
from serial_reader import SerialReader
from plotter import plot_data
import time

PORT = "COM3"

st.set_page_config(page_title="DHT11 Dashboard", layout="wide")
st.title("🌡️ DHT11 Temperature & Humidity Dashboard")

reader = SerialReader(PORT)
reader.start()

# Wait briefly for connection
time.sleep(2)

if not reader.connected:
    st.error("🚫 Unable to connect to Arduino on port COM3. Please check the connection.")
    st.stop()

placeholder = st.empty()
warning_placeholder = st.empty()

try:
    while True:
        if not reader.data:
            with warning_placeholder:
                st.warning("⚠️ Connected to serial port, but no data received yet...")
                time.sleep(1)
                continue
        else:
            warning_placeholder.empty()

        # Check for data staleness (>10 seconds without update)
        if reader.last_received_time and time.time() - reader.last_received_time > 10:
            st.error("⏱️ No new data received in the last 10 seconds. Check Arduino.")
            reader.stop()
            st.stop()

        with placeholder.container():
            plot_data(reader.data)
        time.sleep(1)
except KeyboardInterrupt:
    reader.stop()
