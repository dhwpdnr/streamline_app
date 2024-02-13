import os
import json
import numpy as np
from netCDF4 import Dataset, num2date
from shapely.geometry import shape, Point
import pandas as pd

# GeoJSON 파일
geojson_path = './data/Daejeon.geojson'
with open(geojson_path, 'r') as f:
    geojson = json.load(f)

# 데이터 폴더 경로
data_folder_path = './ncdata'

# 결과 저장 경로
output_folder = './processed_data'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# /ncdata 폴더 내 모든 .nc 파일 처리
for filename in os.listdir(data_folder_path):
    if filename.endswith('.nc'):
        # 파일 경로 생성
        file_path = os.path.join(data_folder_path, filename)
        # 년도 추출
        year = filename.split('_')[-1].split('.')[0]
        # nc 파일 로드
        ncfile = Dataset(file_path, 'r')
        latitudes = ncfile.variables['latitude'][:]
        longitudes = ncfile.variables['longitude'][:]
        times = ncfile.variables['time'][:]
        tamax = ncfile.variables['TAMAX'][:]
        # 시간 변수의 단위 정보를 가져오기
        dates = num2date(times[:], units=ncfile.variables['time'].units)

        # 지역별 평균 TAMAX 계산 및 adm_cd2 추가
        results = []
        for feature in geojson['features']:
            region_name = feature['properties']['adm_nm']
            adm_cd2 = feature['properties']['adm_cd2']
            geom = shape(feature['geometry'])

            for t_index, date in enumerate(dates):
                temp_values = []
                minx, miny, maxx, maxy = geom.bounds
                lat_indices = np.where((latitudes >= miny) & (latitudes <= maxy))[0]
                lon_indices = np.where((longitudes >= minx) & (longitudes <= maxx))[0]

                for i in lat_indices:
                    for j in lon_indices:
                        point = Point(longitudes[j], latitudes[i])
                        if geom.contains(point):
                            temp_values.append(tamax[t_index, i, j])

                if temp_values:
                    avg_temp = np.mean(temp_values)
                    results.append({
                        'Region': region_name,
                        'adm_cd2': adm_cd2,
                        'Date': date.strftime('%Y-%m-%d'),
                        'Avg_TAMAX': avg_temp
                    })

        ncfile.close()

        # 결과를 데이터프레임으로 변환하고 CSV로 저장
        df_results = pd.DataFrame(results)
        output_filename = f"avg_tamax_by_region_{year}.csv"
        output_path = os.path.join(output_folder, output_filename)
        df_results.to_csv(output_path, index=False)

        print(f"Processed and saved: {output_filename}")

print("save nc data complete")

dfs = []

# 모든 CSV 파일을 순회하며 DataFrame으로 로드
for filename in os.listdir(output_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(output_folder, filename)
        df = pd.read_csv(file_path)
        dfs.append(df)

# 모든 DataFrame 병합
merged_df = pd.concat(dfs, ignore_index=True)

# 새로운 CSV 파일로 저장
merged_csv_path = os.path.join("./data", "merged_avg_tamax_by_region.csv")
merged_df.to_csv(merged_csv_path, index=False)

print(f"Merged CSV saved to: {merged_csv_path}")
