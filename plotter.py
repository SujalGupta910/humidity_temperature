import pandas as pd
import streamlit as st
import altair as alt
from datetime import datetime
from tzlocal import get_localzone

def plot_data(data_list):
    if not data_list:
        st.write("Waiting for data...")
        return

    local_tz = get_localzone()
    df = pd.DataFrame(data_list)
    df["datetime"] = pd.to_datetime(df["time"], unit="s").dt.tz_localize("UTC").dt.tz_convert(local_tz)
    df = df.tail(100)

    time_format = "%I:%M:%S %p"

    def create_chart(y_field, y_title, color):
        return alt.Chart(df).mark_line(color=color).encode(
            x=alt.X("datetime:T", title="Time", axis=alt.Axis(format=time_format, labelAngle=0)),
            y=alt.Y(f"{y_field}:Q", title=y_title),
            tooltip=[alt.Tooltip("datetime:T", format=time_format), alt.Tooltip(f"{y_field}:Q", title=y_title)]
        ).properties(title=y_title, height=300)

    temp_chart = create_chart("temperature", "Temperature (°C)", "red")
    hum_chart = create_chart("humidity", "Humidity (%)", "blue")

    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(temp_chart, use_container_width=True)
    with col2:
        st.altair_chart(hum_chart, use_container_width=True)

    latest = df.iloc[-1]
    col3, col4 = st.columns(2)
    with col3:
        st.metric("🌡️ Temperature (°C)", f"{latest['temperature']:.2f}")
    with col4:
        st.metric("💧 Humidity (%)", f"{latest['humidity']:.2f}")

    st.caption(f"Last updated: {datetime.now(local_tz).strftime('%I:%M:%S %p')}")
