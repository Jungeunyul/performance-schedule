import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="Dance Performance Dashboard", layout="wide")

# 2. 사이드바에서 언어 선택 (한국어 / English)
st.sidebar.markdown("### 🌐 Language / 언어 선택")
lang = st.sidebar.radio("Choose your language", ["한국어", "English"])

# 3. 언어별 텍스트 사전 정의
text_data = {
    "한국어": {
        "title": "🩰 국내 무용 공연 정보 트래킹 대시보드",
        "sub": "전국 주요 무용 공연의 장르별, 지역별 데이터를 분석하고 비교하는 포트폴리오입니다.",
        "filter_header": "🔍 데이터 필터링",
        "genre_label": "장르 선택",
        "region_label": "지역 선택",
        "metric_count": "총 공연 건수",
        "metric_price": "평균 티켓 가격",
        "metric_rate": "평균 예매율",
        "table_title": "📊 필터링된 공연 상세 정보 (클릭 시 진짜 예매 페이지로 이동)",
        "no_data": "선택한 조건에 맞는 공연 데이터가 없습니다.",
        "chart1_title": "💰 공연별 티켓 가격 비교",
        "chart2_title": "📈 공연별 예매율 추이",
        "no_chart_data": "시각화할 데이터가 없습니다.",
        "col_name": "공연명", "col_group": "단체명", "col_genre": "장르", 
        "col_venue": "공연장", "col_region": "지역", "col_price": "티켓가격(원)", 
        "col_rate": "예매율(%)", "col_start": "시작일", "col_end": "종료일", "col_link": "예매하기"
    },
    "English": {
        "title": "🩰 Korea Dance Performance Tracking Dashboard",
        "sub": "A portfolio analyzing and comparing major dance performances by genre and region in Korea.",
        "filter_header": "🔍 Data Filtering",
        "genre_label": "Select Genre",
        "region_label": "Select Region",
        "metric_count": "Total Performances",
        "metric_price": "Average Ticket Price",
        "metric_rate": "Average Booking Rate",
        "table_title": "📊 Filtered Performance Details (Click Link to Official Booking Site)",
        "no_data": "No performance data matches the selected criteria.",
        "chart1_title": "💰 Ticket Price Comparison by Performance",
        "chart2_title": "📈 Booking Rate Trend by Performance",
        "no_chart_data": "No data available for visualization.",
        "col_name": "Performance", "col_group": "Organization", "col_genre": "Genre", 
        "col_venue": "Venue", "col_region": "Region", "col_price": "Price(KRW)", 
        "col_rate": "Booking Rate(%)", "col_start": "Start Date", "col_end": "End Date", "col_link": "Book Now"
    }
}

t = text_data[lang]

# 4. 데이터 정의 (피나 바우쉬 주소 맨 끝 따옴표 부활 완료!)
data = [
    {"공연명": "국립발레단 <지젤>", "단체명": "국립발레단", "장르": "발레", "공연장": "예술의전당 오페라극장", "지역": "서울", "티켓가격(원)": 60000, "예매율(%)": 92.5, "시작일": "2026-06-01", "종료일": "2026-06-07", "예매하기": "https://www.sac.or.kr/site/main/program/program_list"},
    {"공연명": "유니버설발레단 <백조의 호수>", "단체명": "유니버설발레단", "장르": "발레", "공연장": "세종문화회관 대극장", "지역": "서울", "티켓가격(원)": 80000, "예매율(%)": 88.1, "시작일": "2026-06-15", "종료일": "2026-06-22", "예매하기": "https://www.sejongpac.or.kr/portal/performance/perf/list.do"},
    {"공연명": "국립현대무용단 <공간의 몸짓>", "단체명": "국립현대무용단", "장르": "현대무용", "공연장": "대학로 예술극장 대극장", "지역": "서울", "티켓가격(원)": 30000, "예매율(%)": 75.4, "시작일": "2026-07-05", "종료일": "2026-07-12", "예매하기": "https://theater.arko.or.kr/Pages/Performance/List.aspx"},
    {"공연명": "LDP무용단 <국경 대치>", "단체명": "LDP무용단", "장르": "현대무용", "공연장": "서강대학교 메리홀", "지역": "서울", "티켓가격(원)": 25000, "예매율(%)": 81.0, "시작일": "2026-05-28", "종료일": "2026-05-31", "예매하기": "https://tickets.interpark.com/contents/genre/dance"},
    {"공연명": "국립무용단 <전통의 향연>", "단체명": "국립무용단", "장르": "한국무용", "공연장": "국립극장 해오름극장", "지역": "서울", "티켓가격(원)": 40000, "예매율(%)": 84.3, "시작일": "2026-06-10", "종료일": "2026-06-14", "예매하기": "https://www.ntok.go.kr/kr/Ticket/Performance/List"},
    {"공연명": "경기도무용단 <련(蓮)>", "단체명": "경기도무용단", "장르": "한국무용", "공연장": "경기아트센터 대극장", "지역": "경기", "티켓가격(원)": 20000, "예매율(%)": 69.8, "시작일": "2026-06-20", "종료일": "2026-06-21", "예매하기": "https://www.ggac.or.kr/?p=14"},
    {"공연명": "광주시립발레단 <돈키호테>", "단체명": "광주시립발레단", "장르": "발레", "공연장": "광주예술의전당", "지역": "광주", "티켓가격(원)": 30000, "예매율(%)": 78.2, "시작일": "2026-07-01", "종료일": "2026-07-03", "예매하기": "https://gjart.gwangju.go.kr/ko/cmd.do?opencode=prmList"},
    {"공연명": "대구시립무용단 <몸의 언어>", "단체명": "대구시립무용단", "장르": "현대무용", "공연장": "대구문화예술회관", "지역": "대구", "티켓가격(원)": 15000, "예매율(%)": 62.4, "시작일": "2026-06-05", "종료일": "2026-06-06", "예매하기": "https://daeguartcenter.or.kr/content/01schedule/01_01.html"},
    {"공연명": "파리 오페라 발레단 <백조의 호수>", "단체명": "파리 오페라 발레단", "장르": "발레", "공연장": "예술의전당 오페라극장", "지역": "서울(내한)", "티켓가격(원)": 120000, "예매율(%)": 98.2, "시작일": "2026-08-10", "종료일": "2026-08-15", "예매하기": "https://www.sac.or.kr/site/main/program/program_list"},
    {"공연명": "영국 로열 발레단 <돈키호테>", "단체명": "영국 로열 발레단", "장르": "발레", "공연장": "세종문화회관 대극장", "지역": "서울(내한)", "티켓가격(원)": 150000, "예매율(%)": 95.4, "시작일": "2026-09-01", "종료일": "2026-09-05", "예매하기": "https://www.sejongpac.or.kr/portal/performance/perf/list.do"},
    {"공연명": "피나 바우쉬 부퍼탈 탄츠테아터 <봄의 제전>", "단체명": "부퍼탈 탄츠테아터", "장르": "현대무용", "공연장": "LG아트센터 서울", "지역": "서울(내한)", "티켓가격(원)": 90000, "예매율(%)": 91.0, "시작일": "2026-10-12", "종료일": "2026-10-15", "예매하기": "https://www.lgart.com/product/list"}
]
df = pd.DataFrame(data)

if lang == "English":
    df["장르"] = df["장르"].map({"발레": "Ballet", "현대무용": "Contemporary", "한국무용": "Traditional"})
    df["지역"] = df["지역"].map({"서울": "Seoul", "경기": "Gyeonggi", "광주": "Gwangju", "대구": "Daegu", "서울(내한)": "Seoul(International)"})

# 표 컬럼명 변환
df_display = df.rename(columns={
    "공연명": t["col_name"], "단체명": t["col_group"], "장르": t["col_genre"],
    "공연장": t["col_venue"], "지역": t["col_region"], "티켓가격(원)": t["col_price"], 
    "예매율(%)": t["col_rate"], "시작일": t["col_start"], "종료일": t["col_end"], "예매하기": t["col_link"]
})

# 5. 메인 화면 타이틀 출력
st.title(t["title"])
st.markdown(t["sub"])
st.markdown("---")

# 6. 사이드바 필터 동작
st.sidebar.header(t["filter_header"])
genres = st.sidebar.multiselect(t["genre_label"], options=df_display[t["col_genre"]].unique(), default=df_display[t["col_genre"]].unique())
regions = st.sidebar.multiselect(t["region_label"], options=df_display[t["col_region"]].unique(), default=df_display[t["col_region"]].unique())

filtered_df = df_display[df_display[t["col_genre"]].isin(genres) & df_display[t["col_region"]].isin(regions)]

# 7. 상단 요약 지표 (Metrics)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(t["metric_count"], f"{len(filtered_df)} " + ("Items" if lang == "English" else "건"))
with col2:
    avg_price = filtered_df[t["col_price"]].mean() if not filtered_df.empty else 0
    st.metric(t["metric_price"], f"{int(avg_price):,} KRW" if lang == "English" else f"{int(avg_price):,} 원")
with col3:
    avg_rate = filtered_df[t["col_rate"]].mean() if not filtered_df.empty else 0
    st.metric(t["metric_rate"], f"{avg_rate:.1f} %")

st.markdown("---")

# 8. 데이터 테이블 출력 및 하이퍼링크 설정
st.subheader(t["table_title"])
if not filtered_df.empty:
    st.dataframe(
        filtered_df, 
        use_container_width=True,
        column_config={
            t["col_link"]: st.column_config.LinkColumn(
                t["col_link"],
                help="클릭하면 해당 공연의 공식 예매 페이지로 이동합니다" if lang == "한국어" else "Click to open official booking site",
                display_text="🔗 " + t["col_link"]
            )
        }
    )
else:
    st.warning(t["no_data"])

st.markdown("---")

# 9. 데이터 시각화 (차트)
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader(t["chart1_title"])
    if not filtered_df.empty:
        st.bar_chart(data=filtered_df, x=t["col_name"], y=t["col_price"])
    else:
        st.info(t["no_chart_data"])

with chart_col2:
    st.subheader(t["chart2_title"])
    if not filtered_df.empty:
        st.line_chart(data=filtered_df, x=t["col_name"], y=t["col_rate"])
    else:
        st.info(t["no_chart_data"])
