import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="Dance Performance Dashboard", layout="wide")

# 2. 사이드바에서 언어 선택
st.sidebar.markdown("### 🌐 Language / 언어 선택")
lang = st.sidebar.radio("Choose your language", ["한국어", "English"])

# 3. 언어별 텍스트 사전 정의
text_data = {
    "한국어": {
        "title": "🩰 국내 무용 공연 정보 트래킹 대시보드",
        "sub": "전국 주요 무용 공연의 장르별, 지역별 데이터를 분석하고 비교하는 포트폴리오입니다.",
        "guide_title": "💡 처음 만나는 무용 장르 가이드 (전공자가 알려주는 꿀팁)",
        "guide_ballet": "**발레 (Ballet):** 신체의 연장과 우아한 도약을 중심으로 한 클래식 무용의 정수입니다.",
        "guide_contemporary": "**현대무용 (Contemporary):** 정형화된 규칙을 깨고 인간 고유의 감정과 자유로운 호흡을 표현하는 예술입니다.",
        "guide_traditional": "**한국무용 (Traditional):** 정중동(靜中動)의 미학, 깊은 호흡과 버선코의 곡선이 만드는 우리 고유의 춤입니다.",
        "filter_header": "🔍 데이터 필터링",
        "genre_label": "장르 선택",
        "region_label": "지역 선택",
        "month_label": "관람 월(Month) 선택",
        "price_label": "티켓 가격 범위 (원)",
        "metric_count": "총 공연 건수",
        "metric_price": "평균 티켓 가격",
        "metric_rate": "평균 예매율",
        "table_title": "📊 필터링된 공연 상세 정보 (링크 클릭 시 해당 페이지로 이동)",
        "no_data": "선택한 조건에 맞는 공연 데이터가 없습니다.",
        "chart1_title": "💰 공연별 티켓 가격 비교",
        "chart2_title": "📈 공연별 예매율 추이",
        "no_chart_data": "시각화할 데이터가 없습니다.",
        "col_name": "공연명", "col_group": "단체명", "col_genre": "장르", 
        "col_venue": "공연장", "col_region": "지역", "col_price": "티켓가격(원)", 
        "col_rate": "예매율(%)", "col_start": "시작일", "col_end": "종료일", 
        "col_link": "예매하기", "col_map": "공연장 위치"
    },
    "English": {
        "title": "🩰 Korea Dance Performance Tracking Dashboard",
        "sub": "A portfolio analyzing and comparing major dance performances by genre and region in Korea.",
        "guide_title": "💡 Quick Guide to Dance Genres (Major's Perspective)",
        "guide_ballet": "**Ballet:** The essence of classical dance centered on the extension of the body and elegant leaps.",
        "guide_contemporary": "**Contemporary:** An art that breaks formalized rules to express human emotions and free breathing.",
        "guide_traditional": "**Traditional Korean Dance:** The aesthetics of stillness in motion, created by deep breathing and elegant curves.",
        "filter_header": "🔍 Data Filtering",
        "genre_label": "Select Genre",
        "region_label": "Select Region",
        "month_label": "Select Month",
        "price_label": "Ticket Price Range (KRW)",
        "metric_count": "Total Performances",
        "metric_price": "Average Ticket Price",
        "metric_rate": "Average Booking Rate",
        "table_title": "📊 Filtered Performance Details (Click Links to Open)",
        "no_data": "No performance data matches the selected criteria.",
        "chart1_title": "💰 Ticket Price Comparison by Performance",
        "chart2_title": "📈 Booking Rate Trend by Performance",
        "no_chart_data": "No data available for visualization.",
        "col_name": "Performance", "col_group": "Organization", "col_genre": "Genre", 
        "col_venue": "Venue", "col_region": "Region", "col_price": "Price(KRW)", 
        "col_rate": "Booking Rate(%)", "col_start": "Start Date", "col_end": "End Date", 
        "col_link": "Book Now", "col_map": "Venue Map"
    }
}
t = text_data[lang]

# 4. 외부 CSV 파일 호출 (data 폴더 안에 넣었으므로 경로 명시)
try:
    df = pd.read_csv("data/data.csv")
except:
    df = pd.read_csv("data.csv")  # 루트 폴더에 있을 경우 예외처리

# 데이터 전처리 루틴
df["월"] = pd.to_datetime(df["시작일"]).dt.month
df["월_display"] = df["월"].map(lambda x: f"{x}월" if lang == "한국어" else f"Month {x}")
df["공연장위치"] = df["공연장"].map(lambda x: f"https://map.kakao.com/?q={str(x).replace(' ', '+')}")

if lang == "English":
    df["장르"] = df["장르"].map({"발레": "Ballet", "현대무용": "Contemporary", "한국무용": "Traditional"})
    df["지역"] = df["지역"].map({
        "서울": "Seoul", "경기": "Gyeonggi", "광주": "Gwangju", "대구": "Daegu", 
        "부산": "Busan", "인천": "Incheon", "대전": "Daejeon", "울산": "Ulsan",
        "제주": "Jeju", "전북": "Jeonbuk", "전남": "Jeonnam", "서울(내한)": "Seoul(Int'l)"
    })

df_display = df.rename(columns={
    "공연명": t["col_name"], "단체명": t["col_group"], "장르": t["col_genre"],
    "공연장": t["col_venue"], "지역": t["col_region"], "티켓가격(원)": t["col_price"], 
    "예매율(%)": t["col_rate"], "시작일": t["col_start"], "종료일": t["col_end"], 
    "예매하기": t["col_link"], "공연장위치": t["col_map"]
})

# 5. UI 렌더링
st.title(t["title"])
st.markdown(t["sub"])

with st.expander(t["guide_title"]):
    st.markdown(f"- {t['guide_ballet']}")
    st.markdown(f"- {t['guide_contemporary']}")
    st.markdown(f"- {t['guide_traditional']}")
st.markdown("---")

# 6. 사이드바 필터링
st.sidebar.header(t["filter_header"])
genres = st.sidebar.multiselect(t["genre_label"], options=df_display[t["col_genre"]].unique(), default=df_display[t["col_genre"]].unique())
regions = st.sidebar.multiselect(t["region_label"], options=df_display[t["col_region"]].unique(), default=df_display[t["col_region"]].unique())
months = st.sidebar.multiselect(t["month_label"], options=sorted(df_display["월_display"].unique(), key=lambda x: int(x.replace('월','').replace('Month ',''))), default=df_display["월_display"].unique())

min_price, max_price = int(df_display[t["col_price"]].min()), int(df_display[t["col_price"]].max())
price_range = st.sidebar.slider(t["price_label"], min_value=min_price, max_value=max_price, value=(min_price, max_price), step=5000)

filtered_df = df_display[
    df_display[t["col_genre"]].isin(genres) & df_display[t["col_region"]].isin(regions) & 
    df_display["월_display"].isin(months) & (df_display[t["col_price"]] >= price_range[0]) & (df_display[t["col_price"]] <= price_range[1])
]

# 7. 요약 지표
col1, col2, col3 = st.columns(3)
with col1: st.metric(t["metric_count"], f"{len(filtered_df)} 건" if lang == "한국어" else f"{len(filtered_df)} Items")
with col2: st.metric(t["metric_price"], f"{int(filtered_df[t['col_price']].mean() if not filtered_df.empty else 0):,} 원" if lang == "한국어" else f"{int(filtered_df[t['col_price']].mean() if not filtered_df.empty else 0):,} KRW")
with col3: st.metric(t["metric_rate"], f"{filtered_df[t['col_rate']].mean() if not filtered_df.empty else 0:.1f} %")
st.markdown("---")

# 8. 데이터 테이블 출력
st.subheader(t["table_title"])
if not filtered_df.empty:
    st.dataframe(
        filtered_df.drop(columns=["월", "월_display"]), use_container_width=True,
        column_config={
            t["col_link"]: st.column_config.LinkColumn(t["col_link"], display_text="🔗 " + t["col_link"]),
            t["col_map"]: st.column_config.LinkColumn(t["col_map"], display_text="📍 Map")
        }
    )
else:
    st.warning(t["no_data"])
st.markdown("---")

# 9. 시각화 차트
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.subheader(t["chart1_title"])
    if not filtered_df.empty: st.bar_chart(data=filtered_df, x=t["col_name"], y=t["col_price"])
    else: st.info(t["no_chart_data"])
with chart_col2:
    st.subheader(t["chart2_title"])
    if not filtered_df.empty: st.line_chart(data=filtered_df, x=t["col_name"], y=t["col_rate"])
    else: st.info(t["no_chart_data"])
