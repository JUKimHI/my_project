# 필요한 라이브러리 불러오기
import streamlit as st
import pandas as pd
import geopandas as gpd
import folium

# 페이지 제목
st.title("전국 시군구별 합계출산율 시각화")
st.markdown("""
이 애플리케이션은 대한민국 전국 시군구별 합계출산율을 Choropleth 지도 형태로 시각화합니다.
데이터를 업로드하고, 대한민국 지역별 출산율을 확인하세요.
""")

# 사이드바 정보
st.sidebar.header("옵션 설정")
st.sidebar.markdown("여기서 데이터 파일을 업로드하거나 옵션을 조정하세요.")

# 데이터 업로드
uploaded_csv = st.sidebar.file_uploader("CSV 데이터 업로드 (합계출산율)", type=["csv"])
uploaded_geojson = st.sidebar.file_uploader("GeoJSON 파일 업로드 (행정구역)", type=["json"])

if uploaded_csv and uploaded_geojson:
    # 데이터 읽기
    df_birth_pop = pd.read_csv(uploaded_csv, encoding='euc-kr')
    df_birth_pop.columns = ['행정구', '합계출산율']  # 컬럼 이름 재설정
    
    gdf_all_regions = gpd.read_file(uploaded_geojson)

    # 데이터 확인
    st.markdown("### 업로드된 데이터")
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
    
    m

    # 추가 설명
    st.markdown("""
    #### 지도 해석
    - 색상이 진할수록 합계출산율이 높은 지역을 나타냅니다.
    - 각 시군구별 출산율 데이터는 업로드된 파일을 기반으로 표시됩니다.
    """)
else:
    st.warning("CSV 파일과 GeoJSON 파일을 모두 업로드해주세요")