import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


aqi_df = pd.read_csv("aqi_data.csv")
datetime_columns = ['date']

# Mengonversi kolom datetime menjadi tipe data datetime
for column in datetime_columns:
    aqi_df[column] = pd.to_datetime(aqi_df[column])

# Mendapatkan nilai minimum dan maksimum dari kolom datetime
min_date = aqi_df["date"].min()
max_date = aqi_df["date"].max()

# Bagian Sidebar
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://static.vecteezy.com/system/resources/previews/007/250/596/non_2x/aqi-letter-logo-design-on-white-background-aqi-creative-initials-letter-logo-concept-aqi-letter-design-vector.jpg")
    
    # Row 1 dengan 2 kolom
    row1_col1, row1_col2 = st.columns(2)
    
    # Menambahkan konten ke masing-masing kolom di dalam sidebar
    start_date = row1_col1.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
    selected_hour_start = row1_col2.selectbox('Pilih Jam Awal', list(range(24)), index=0)

    # Row 2 dengan 2 kolom
    row2_col1, row2_col2 = st.columns(2)
    
    # Menambahkan konten ke masing-masing kolom di dalam sidebar
    end_date = row2_col1.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)
    selected_hour_end = row2_col2.selectbox('Pilih Jam Akhir', list(range(24)), index=23)

    # Dropdown untuk memilih stasiun
    selected_station = st.selectbox('Pilih Titik Pantau', ['All'] + list(aqi_df['station'].unique()), index=0)

    # Tombol untuk mengontrol apakah garis antara titik-titik akan ditampilkan atau tidak
    show_line = st.toggle('Tarik Garis', value=True)

# Menggunakan rentang waktu, jam, dan stasiun untuk memfilter DataFrame
start_datetime = pd.to_datetime(start_date) + pd.to_timedelta(selected_hour_start, unit='h')
end_datetime = pd.to_datetime(end_date) + pd.to_timedelta(selected_hour_end, unit='h')

if selected_station != 'All':
    main_df = aqi_df[(aqi_df["date"] >= start_datetime) & (aqi_df["date"] <= end_datetime) & (aqi_df["station"] == selected_station)]
else:
    main_df = aqi_df[(aqi_df["date"] >= start_datetime) & (aqi_df["date"] <= end_datetime)]

st.header('AQI - 12 Monitoring Points around Smelters')

st.subheader('Dataframes')

# Tampilkan hasil dengan st.dataframe()
st.write(f'Data from {start_datetime} and {end_datetime}, Monitoring Points: {selected_station if selected_station != "All" else "All"}')
st.data_editor(main_df, width=800)

st.subheader('Visualization')

# Mapping warna untuk setiap AQI_Label
color_map = {'Good': 'green', 'Moderate': 'yellow', 'Unhealthy for Sensitive Groups': 'orange', 
             'Unhealthy': 'red', 'Very Unhealthy': 'purple', 'Hazardous': 'black'}

# Plot data dengan warna berdasarkan AQI_Label dan tambahkan garis
fig, ax = plt.subplots(figsize=(20, 10))
max_pm25 = main_df['PM2.5'].max()
for label, color in color_map.items():
    label_df = main_df[main_df['AQI_Label'] == label]
    ax.scatter(label_df['date'], label_df['PM2.5'], label=label, color=color)

# Tarik garis antara titik-titiknya
if show_line:
    # Tarik garis antara titik-titiknya
    ax.plot(main_df['date'], main_df['PM2.5'], linestyle='-', color='blue', linewidth=0.5)

# Atur agar garis y selalu dimulai dari 0
ax.set_ylim(0, max_pm25)

ax.set_title('Grafik PM2.5 dari Waktu ke Waktu Filtered')
ax.set_xlabel('Tanggal')
ax.set_ylabel('PM2.5 Level')
ax.legend()
ax.grid(True)

# Menampilkan plot di Streamlit
st.pyplot(fig)

st.subheader('Info')
st.write('Jika data yang dimunculkan di grafik garisnya acak, disarankan memilih satu titik pantau emisi atau menonaktifkan toggle tarik garis.')

st.caption('Copyright (c) Ficky Alkarim 2024')
