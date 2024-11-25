# 필요한 라이브러리 불러오기
import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# 페이지 제목
st.title("전국 시군구별 합계출산율 시각화")
st.markdown("""
이 애플리케이션은 대한민국 전국 시군구별 합계출산율을 Choropleth 지도 형태로 시각화합니다.
""")

# 데이터 파일 경로
CSV_FILE = '../data/합계출산율.csv'  # CSV 파일 경로
GEOJSON_FILE = '../data/all_regions_2.json'  # GeoJSON 파일 경로

# 데이터 읽기
try:
    # CSV 데이터 읽기
    df_birth_pop = pd.read_csv(CSV_FILE, encoding='euc-kr')
    df_birth_pop.columns = ['행정구', '합계출산율']  # 컬럼 이름 재설정

    # GeoJSON 데이터 읽기
    gdf_all_regions = gpd.read_file(GEOJSON_FILE)

    # 데이터 확인
    st.markdown("### 데이터 미리보기")
    st.write("#### CSV 데이터:")
    st.dataframe(df_birth_pop.head())

    st.write("#### GeoJSON 데이터:")
    st.write(gdf_all_regions.head())

    # 지도 시각화
    st.markdown("### Choropleth 지도")
    title = '전국 합계출산율'
    title_html = f'<h3 align="center" style="font-size:20px"><b>{title}</b></h3>'

    # 지도 생성
    m = folium.Map(
        location=[36.5, 127.5],
        zoom_start=7,
        tiles='cartodbpositron'
    )
    m.get_root().html.add_child(folium.Element(title_html))

    # Choropleth 지도 추가
    folium.Choropleth(
        geo_data=gdf_all_regions,
        data=df_birth_pop,
        columns=('행정구', '합계출산율'),
        key_on='feature.properties.SIG_KOR_NM',
        fill_color='BuPu',
        legend_name='전국 시군구별 합계출산율',
        fill_opacity=0.7,
        line_opacity=0.5
    ).add_to(m)

    # Streamlit에서 지도 표시
    folium_static(m)

    # 추가 설명
    st.markdown("""
    #### 지도 해석
    - 색상이 진할수록 합계출산율이 높은 지역을 나타냅니다.
    - 각 시군구별 출산율 데이터는 코드 내부에서 로드된 데이터를 기반으로 표시됩니다.
    """)
except FileNotFoundError as e:
    st.error(f"데이터 파일이 없습니다: {e}")
