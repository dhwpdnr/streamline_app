import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
import json
import branca.colormap as cm

# GeoJSON 경계 데이터 로드
geojson_path = "./data/Daejeon.geojson"
with open(geojson_path, "r") as f:
    geojson = json.load(f)

# 평균 온도 데이터가 저장된 CSV 파일 로드
avg_temp_data_path = "./data/merged_avg_tamax_by_region.csv"
df_avg_temp = pd.read_csv(avg_temp_data_path)
df_avg_temp["Date"] = pd.to_datetime(df_avg_temp["Date"])  # 날짜 형식 변환

# 선택 가능한 최소 날짜와 최대 날짜 설정
min_date = df_avg_temp["Date"].min()
max_date = df_avg_temp["Date"].max()

# Streamlit 사용자 인터페이스 구성
st.title("구역별 평균 온도 시각화")

# 사용자가 날짜 선택
selected_date = st.date_input(
    "날짜를 선택하세요",
    value=max_date,  # 기본값을 가장 최근 날짜로 설정
    min_value=min_date,  # 선택 가능한 최소 날짜
    max_value=max_date,  # 선택 가능한 최대 날짜
)

# 선택된 날짜에 해당하는 데이터 필터링
filtered_data = df_avg_temp[df_avg_temp["Date"] == pd.Timestamp(selected_date)]

# 컬러맵과 범례 설정
min_temp = filtered_data["Avg_TAMAX"].min()
max_temp = filtered_data["Avg_TAMAX"].max()
colormap = cm.linear.YlOrRd_09.scale(min_temp, max_temp)
colormap.caption = "평균 온도 (°C)"

# Folium 지도 생성
m = folium.Map(location=[36.3504, 127.3845], zoom_start=10)

# GeoJSON 경계와 평균 온도 데이터를 사용하여 지도에 표시
for feature in geojson["features"]:
    region_name = feature["properties"]["adm_nm"]
    region_temp = (
        filtered_data[filtered_data["Region"] == region_name]["Avg_TAMAX"].values[0]
        if not filtered_data[filtered_data["Region"] == region_name].empty
        else None
    )

    if region_temp is not None:
        geom = json.dumps(feature["geometry"])
        style_function = lambda x, color=colormap(region_temp): {
            "fillColor": color,
            "color": "black",
            "weight": 2,
            "fillOpacity": 0.5,
        }
        folium.GeoJson(
            geom,
            style_function=style_function,
            tooltip=f"{region_name}: {region_temp:.2f}°C",
        ).add_to(m)

# 범례를 지도에 추가
m.add_child(colormap)

# Streamlit에서 지도 표시
folium_static(m)
