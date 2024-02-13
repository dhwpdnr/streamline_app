# Sparcs 해커톤 데이터분석 미션
대전 지역 지역별 최고 온도 시각화
<br>
<br>
## 참고 데이터 
기상청 데이터 : [기상청 기후변화 표준 시나리오](http://www.climate.go.kr/home/CCS/contents_2021/35_download.php) <br>
행정동 경계 데이터 : [행정동 경계](https://github.com/vuski/admdongkor)
<br>
<br>
## 데이터 
Daejeon.geojson : 대전지역 행정동 경계 정보 <br>
merged_avg_tamax_by_region.csv : 대전지역 각 행정구역의 일별 최고온도 (2000년 ~ 2019년)
<br>
<br>
## 파일 
streamlit_app.py : 앱 실행 파일 <br>
data_preprocessing.py : 데이터 전처리
<br>
<br>
## Quick Start
라이브러리 섩치
```bash
pip install -r requirements.txt
```
streamlit 실행
```bash
streamlit run streamlit_app.py
```

