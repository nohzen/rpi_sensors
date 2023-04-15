"""
python -m streamlit run dashboard_streamlit.py --server.headless true
http://raspX.local:8501
"""
import datetime
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


### Read csv datas ###
csv_path = "data_office.csv"
df = pd.read_csv(csv_path, header=0, index_col=0)

# label - ylabel
ylabel_dict = {
    "Temperature (SHT31)" : "Temperature [℃]",
    "Humidity (SHT31)" : "Humidity [%RH]",
    # "Temperature (ADT7410)" : "Temperature [℃]",
    "CO2 (MH-z19)": "CO2 [ppm]",
    "Temperature (MH-z19)" : "Temperature [℃]"
    }

# label - column of df
column_dict = {
    "Temperature (SHT31)" : "sht31_temperature",
    "Humidity (SHT31)" : "sht31_humidity",
    # "Temperature (ADT7410)" : "adt7410_temperature",
    "CO2 (MH-z19)": "mhz19_co2",
    "Temperature (MH-z19)": "mhz19_temperature"
}

# label - type
type_dict = {
    "Temperature (SHT31)" : "Temperature",
    "Humidity (SHT31)" : "Humidity",
    # "Temperature (ADT7410)" : "Temperature",
    "CO2 (MH-z19)": "CO2",
    # "Temperature (MH-z19)" : "Temperature",
}
type_set = set(type_dict.values())


### Sidebar ###
st.sidebar.write("# 設定")
# select_column = st.sidebar.selectbox(
#     '可視化するデータを選択:',
#     df.columns)
# selected_labels = st.sidebar.multiselect(
#     "可視化するデータを選択:",
#     column_dict.keys(),
#     default=column_dict.keys())
selected_types = st.sidebar.multiselect(
    "可視化するデータ",
    type_set,
    default=type_set)
time_range_list = ["weak", "day", "hour"]
time_range = st.sidebar.selectbox(
    "日時範囲",
    time_range_list,
    index=1
)
graph_list = ["pyplot", "streamlit"]
graph = st.sidebar.selectbox(
    "グラフタイプ",
    graph_list,
    index=0
)


### main ###
st.write("# 観測データ可視化")
# st.write(df.head())
# st.dataframe(df)
# label = "CO2 (MH-z19 1)"
# st.line_chart(df[column_dict[label]])

### Draw Graph ###
df.index = pd.to_datetime(df.index)
# date_time = df.index

for selected_type in selected_types:
    st.write('## {}の時間変化'.format(selected_type))

    selected_labels = []
    for label, type in type_dict.items():
        if type == selected_type:
            selected_labels.append(label)

    columns = [column_dict[label] for label in selected_labels]
    select_data = df[columns]

    ## time range
    now = datetime.datetime.now()
    if time_range == "weak":
        past = now - datetime.timedelta(weeks=1.1)
    elif time_range == "day":
        past = now - datetime.timedelta(days=1.1)
    elif time_range == "hour":
        past = now - datetime.timedelta(hours=1.1)
    else:
        raise NotImplementedError()
    select_data = select_data[past: now]
    date_time = select_data.index

    if graph == "streamlit":
        st.line_chart(select_data)
    elif graph == "pyplot":
        fig, ax = plt.subplots()
        ax.plot(date_time, select_data, marker=".", label=selected_labels)
        # ax.plot(date_time, select_data, label=selected_labels)

        ax.set_title(selected_type)
        ax.set_xlabel("date time")
        ax.set_ylabel(ylabel_dict[selected_labels[0]])
        ax.grid()

        plt.legend()
        plt.xticks(rotation=30)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%d(%a.) %H:%M"))

        plt.tight_layout()

        st.pyplot(fig)


# for label in selected_labels:
#     st.write('## {}の時間変化'.format(label))
#     column = column_dict[label]
#     select_data = df[column]

#     fig, ax = plt.subplots()
#     ax.plot(date_time, select_data, marker=".", label=label)

#     ax.set_title(label)
#     ax.set_xlabel("date time")
#     ax.set_ylabel(ylabel_dict[label])
#     ax.grid()
#     # ax.set_facecolor((1.0, 0.0, 0.0, 1.0))
#     # fig.set_facecolor((0.0, 0.0, 1.0, 1.0))

#     plt.xticks(rotation=30)
#     plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%d(%a.) %H:%M"))
#     plt.tight_layout()

#     st.pyplot(fig)
#     # st.pyplot(fig, transparent=True)


st.write("# 生データ ダウンロード")
now = datetime.datetime.now()
save_csv_path = "raw_data_{0:%Y%m%d}.csv".format(now)
with open(csv_path) as file:
    st.download_button(label="Download as csv", data=file, file_name=save_csv_path)
