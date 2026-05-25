import streamlit as st  
import pandas as pd  
  
# 1. 페이지 기본 설정 및 제목  
st.set_page_config(page_title="국내 무용 공연 대시보드", layout="wide")  
st.title("🩰 국내 무용 공연 정보 트래킹 대시보드")  
st.markdown("전국 주요 무용 공연의 장르별, 지역별 데이터를 분석하고 비교하는 포트폴리오입니다.")  
st.markdown("---")  
  
# 2. 데이터 불러오기  
@st.cache_data  
def load_data():  
    # 데이터 타입을 지정하여 불러오기  
    df = pd.read_csv("dance_data.csv")  
    df["시작일"] = pd.to_datetime(df["시작일"])  
    df["종료일"] = pd.to_datetime(df["종료일"])  
    return df  
  
try:  
    df = load_data()  
  
    # 3. 사이드바 필터 구성  
    st.sidebar.header("🔍 데이터 필터링")  
      
    # 장르 선택  
    genres = st.sidebar.multiselect("장르 선택", options=df["장르"].unique(), default=df["장르"].unique())  
    # 지역 선택  
    regions = st.sidebar.multiselect("지역 선택", options=df["지역"].unique(), default=df["지역"].unique())  
      
    # 필터링 적용  
    filtered_df = df[df["장르"].isin(genres) & df["지역"].isin(regions)]  
  
    # 4. 상단 요약 지표 (Metrics)  
    col1, col2, col3 = st.columns(3)  
    with col1:  
        st.metric("총 공연 건수", f"{len(filtered_df)} 건")  
    with col2:  
        avg_price = filtered_df["티켓가격(원)"].mean() if not filtered_df.empty else 0  
        st.metric("평균 티켓 가격", f"{int(avg_price):,} 원")  
    with col3:  
        avg_rate = filtered_df["예매율(%)"].mean() if not filtered_df.empty else 0  
        st.metric("평균 예매율", f"{avg_rate:.1f} %")  
  
    st.markdown("---")  
  
    # 5. 데이터 테이블 출력  
    st.subheader("📊 필터링된 공연 상세 정보")  
    if not filtered_df.empty:  
        # 날짜 포맷을 예쁘게 바꿔서 출력  
        display_df = filtered_df.copy()  
        display_df["시작일"] = display_df["시작일"].dt.strftime('%Y-%m-%d')  
        display_df["종료일"] = display_df["종료일"].dt.strftime('%Y-%m-%d')  
        st.dataframe(display_df, use_container_width=True)  
    else:  
        st.warning("선택한 조건에 맞는 공연 데이터가 없습니다.")  
  
    st.markdown("---")  
  
    # 6. 데이터 시각화 (차트)  
    chart_col1, chart_col2 = st.columns(2)  
      
    with chart_col1:  
        st.subheader("💰 공연별 티켓 가격 비교")  
        if not filtered_df.empty:  
            st.bar_chart(data=filtered_df, x="공연명", y="티켓가격(원)")  
        else:  
            st.info("시각화할 데이터가 없습니다.")  
  
    with chart_col2:  
        st.subheader("📈 공연별 예매율 추이")  
        if not filtered_df.empty:  
            st.line_chart(data=filtered_df, x="공연명", y="예매율(%)")  
        else:  
            st.info("시각화할 데이터가 없습니다.")  
  
except FileNotFoundError:  
    st.error("`dance_data.csv` 파일을 찾을 수 없습니다. 파이썬 파일과 같은 폴더에 위치해 있는지 확인해 주세요.")  
