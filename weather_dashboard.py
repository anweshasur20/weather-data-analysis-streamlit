import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page title
st.set_page_config(page_title="Weather Dashboard", layout="wide")
st.title("🌤️ Weather Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload weather data CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file).head(1000)


        # Check required columns
        required_columns = ['Location', 'Date_Time', 'Temperature_C', 'Humidity_pct', 'Precipitation_mm', 'Wind_Speed_kmh']
        if not all(col in df.columns for col in required_columns):
            st.error(f"CSV is missing required columns. Required: {required_columns}")
        else:
            # Convert Date_Time to datetime
            df['Date_Time'] = pd.to_datetime(df['Date_Time'])

            # Sidebar filters
            st.sidebar.header("🔍 Filter Options")
            location_list = df['Location'].unique()
            selected_location = st.sidebar.selectbox("📍 Select Location", location_list)

            date_range = st.sidebar.date_input(
    "📅 Select Date Range",
    (df['Date_Time'].min().date(), df['Date_Time'].max().date())
)


            # Filtered Data
            filtered_df = df[
                (df['Location'] == selected_location) &
                (df['Date_Time'].dt.date >= date_range[0]) &
                (df['Date_Time'].dt.date <= date_range[1])
            ]

            st.subheader(f"📍 Data for {selected_location}")
            st.dataframe(filtered_df)

            # Plotting section
            st.subheader("📊 Weather Trends")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**🌡️ Temperature Over Time**")
                st.line_chart(filtered_df.set_index('Date_Time')['Temperature_C'])

                st.markdown("**🌧️ Precipitation Over Time**")
                st.line_chart(filtered_df.set_index('Date_Time')['Precipitation_mm'])

            with col2:
                st.markdown("**💧 Humidity Over Time**")
                st.line_chart(filtered_df.set_index('Date_Time')['Humidity_pct'])

                st.markdown("**🌬️ Wind Speed Over Time**")
                st.line_chart(filtered_df.set_index('Date_Time')['Wind_Speed_kmh'])

    except Exception as e:
        st.error(f"❌ Error loading or processing file: {e}")
else:
    st.info("👆 Please upload a CSV file to begin.")
