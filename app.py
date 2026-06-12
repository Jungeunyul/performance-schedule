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

# 4. 40개 초대형 데이터 세트 정의 (전국 시립단체, 대학 무용제, 거장 내한 라인업 포함)
data = [
    # --- 발레 (13개) ---
    {"공연명": "국립발레단 <지젤>", "단체명": "국립발레단", "장르": "발레", "공연장": "예술의전당 오페라극장", "지역": "서울", "티켓가격(원)": 60000, "예매율(%)": 92.5, "시작일": "2026-06-01", "종료일": "2026-06-07", "예매하기": "https://www.sac.or.kr"},
    {"공연명": "유니버설발레단 <백조의 호수>", "단체명": "유니버설발레단", "장르": "발레", "공연장": "세종문화회관 대극장", "지역": "서울", "티켓가격(원)": 80000, "예매율(%)": 88.1, "시작일": "2026-06-15", "종료일": "2026-06-22", "예매하기": "https://www.sejongpac.or.kr"},
    {"공연명": "광주시립발레단 <돈키호테>", "단체명": "광주시립발레단", "장르": "발레", "공연장": "광주예술의전당", "지역": "광주", "티켓가격(원)": 30000, "예매율(%)": 78.2, "시작일": "2026-07-01", "종료일": "2026-07-03", "예매하기": "https://gjart.gwangju.go.kr"},
    {"공연명": "파리 오페라 발레단 <백조의 호수>", "단체명": "파리 오페라 발레단", "장르": "발레", "공연장": "예술의전당 오페라극장", "지역": "서울(내한)", "티켓가격(원)": 120000, "예매율(%)": 98.2, "시작일": "2026-08-10", "종료일": "2026-08-15", "예매하기": "https://www.sac.or.kr"},
    {"공연명": "영국 로열 발레단 <돈키호테>", "단체명": "영국 로열 발레단", "장르": "발레", "공연장": "세종문화회관 대극장", "지역": "서울(내한)", "티켓가격(원)": 150000, "예매율(%)": 95.4, "시작일": "2026-09-01", "종료일": "2026-09-05", "예매하기": "https://www.sejongpac.or.kr"},
    {"공연명": "국립발레단 <호두까기인형>", "단체명": "국립발레단", "장르": "발레", "공연장": "예술의전당 오페라극장", "지역": "서울", "티켓가격(원)": 70000, "예매율(%)": 99.1, "시작일": "2026-12-15", "종료일": "2026-12-25", "예매하기": "https://www.sac.or.kr"},
    {"공연명": "유니버설발레단 <더 발레리나>", "단체명": "유니버설발레단", "장르": "발레", "공연장": "예술의전당 CJ토월극장", "지역": "서울", "티켓가격(원)": 50000, "예매율(%)": 83.5, "시작일": "2026-05-20", "종료일": "2026-05-25", "예매하기": "https://www.sac.or.kr"},
    {"공연명": "와이즈발레단 <VITA>", "단체명": "와이즈발레단", "장르": "발레", "공연장": "마포아트센터 아트홀맥", "지역": "서울", "티켓가격(원)": 40000, "예매율(%)": 79.5, "시작일": "2026-05-15", "종료일": "2026-05-17", "예매하기": "https://www.mfac.or.kr"},
    {"공연명": "서울발레시어터 <호두까기 인형>", "단체명": "서울발레시어터", "장르": "발레", "공연장": "과천시민회관 대극장", "지역": "경기", "티켓가격(원)": 30000, "예매율(%)": 82.1, "시작일": "2026-12-10", "종료일": "2026-12-13", "예매하기": "https://tickets.interpark.com"},
    {"공연명": "대구오페라하우스 발레 <잠자는 숲속의 미녀>", "단체명": "대구시립무용단 발레팀", "장르": "발레", "공연장": "대구오페라하우스", "지역": "대구", "티켓가격(원)": 20000, "예매율(%)": 74.5, "시작일": "2026-10-05", "종료일": "2026-10-07", "예매하기": "http://daeguoperahouse.org"},
    {"공연명": "국립발레단 <라 바야데르>", "단체명": "국립발레단", "장르": "발레", "공연장": "예술의전당 오페라극장", "지역": "서울", "티켓가격(원)": 80000, "예매율(%)": 91.3, "시작일": "2026-10-20", "종료일": "2026-10-26", "예매하기": "https://www.sac.or.kr"},
    {"공연명": "유니버설발레단 <심청>", "단체명": "유니버설발레단", "장르": "발레", "공연장": "예술의전당 오페라극장", "지역": "서울", "티켓가격(원)": 90000, "예매율(%)": 89.9, "시작일": "2026-11-05", "종료일": "2026-11-10", "예매하기": "https://www.sac.or.kr"},
    {"공연명": "마린스키 발레단 <백조의 호수> 내한", "단체명": "마린스키 발레단", "장르": "발레", "공연장": "세종문화회관 대극장", "지역": "서울(내한)", "티켓가격(원)": 180000, "예매율(%)": 97.6, "시작일": "2026-11-15", "종료일": "2026-11-19", "예매하기": "https://www.sejongpac.or.kr"},

    # --- 현대무용 (14개) ---
    {"공연명": "국립현대무용단 <공간의 몸짓>", "단체명": "국립현대무용단", "장르": "현대무용", "공연장": "대학로 예술극장 대극장", "지역": "서울", "티켓가격(원)": 30000, "예매율(%)": 75.4, "시작일": "2026-07-05", "종료일": "2026-07-12", "예매하기": "https://theater.arko.or.kr"},
    {"공연명": "LDP무용단 <국경 대치>", "단체명": "LDP무용단", "장르": "현대무용", "공연장": "서강대학교 메리홀", "지역": "서울", "티켓가격(원)": 25000, "예매율(%)": 81.0, "시작일": "2026-05-28", "종료일": "2026-05-31", "예매하기": "https://tickets.interpark.com"},
    {"공연명": "대구시립무용단 <몸의 언어>", "단체명": "대구시립무용단", "장르": "현대무용", "공연장": "대구문화예술회관", "지역": "대구", "티켓가격(원)": 15000, "예매율(%)": 62.4, "시작일": "2026-06-05", "종료일": "2026-06-06", "예매하기": "https://daeguartcenter.or.kr"},
    {"공연명": "피나 바우쉬 부퍼탈 탄츠테아터 <봄의 제전>", "단체명": "부퍼탈 탄츠테아터", "장르": "현대무용", "공연장": "LG아트센터 서울", "지역": "서울(내한)", "티켓가격(원)": 90000, "예매율(%)": 91.0, "시작일": "2026-10-12", "종료일": "2026-10-15", "예매하기": "https://www.lgart.com"},
    {"공연명": "크리스탈 파이트 & 키드 피봇 <어셈블리 홀>", "단체명": "Kid Pivot", "장르": "현대무용", "공연장": "LG아트센터 서울", "지역": "서울(내한)", "티켓가격(원)": 100000, "예매율(%)": 96.5, "시작일": "2026-06-05", "종료일": "2026-06-07", "예매하기": "https://www.lgart.com"},
    {"공연명": "알렉산더 에크만 <한여름 밤의 꿈>", "단체명": "유테보리 오페라 무용단", "장르": "현대무용", "공연장": "LG아트센터 서울", "지역": "서울(내한)", "티켓가격(원)": 95000, "예매율(%)": 94.8, "시작일": "2026-07-17", "종료일": "2026-07-19", "예매하기": "https://www.lgart.com"},
    {"공연명": "국립현대무용단 <정글>", "단체명": "국립현대무용단", "장르": "현대무용", "공연장": "예술의전당 자유소극장", "지역": "서울", "티켓가격(원)": 35000, "예매율(%)": 86.4, "시작일": "2026-11-01", "종료일": "2026-11-06", "예매하기": "https://www.sac.or.kr"},
    {"공연명": "모던테이블 <다크니스 품바>", "단체명": "모던테이블", "장르": "현대무용", "공연장": "대학로 예술극장 대극장", "지역": "서울", "티켓가격(원)": 30000, "예매율(%)": 89.7, "시작일": "2026-06-25", "종료일": "2026-06-28", "예매하기": "https://theater.arko.or.kr"},
    {"공연명": "엠비규어스댄스컴퍼니 <바디콘서트>", "단체명": "엠비규어스댄스컴퍼니", "장르": "현대무용", "공연장": "고양아람누리 아람극장", "지역": "경기", "티켓가격(원)": 40000, "예매율(%)": 94.2, "시작일": "2026-08-21", "종료일": "2026-08-23", "예매하기": "https://www.artgy.or.kr"},
    {"공연명": "네덜란드 댄스 시어터(NDT 1) 내한공연", "단체명": "Nederlands Dans Theater", "장르": "현대무용", "공연장": "LG아트센터 서울", "지역": "서울(내한)", "티켓가격(원)": 110000, "예매율(%)": 96.8, "시작일": "2026-11-12", "종료일": "2026-11-15", "예매하기": "https://www.lgart.com"},
    {"공연명": "광주시립무용단 <빛의 숨결>", "단체명": "광주시립무용단", "장르": "현대무용", "공연장": "광주예술의전당", "지역": "광주", "티켓가격(원)": 20000, "예매율(%)": 70.2, "시작일": "2026-09-10", "종료일": "2026-09-12", "예매하기": "https://gjart.gwangju.go.kr"},
    {"공연명": "대전시립무용단 <현대적 조우>", "단체명": "대전시립무용단", "장르": "현대무용", "공연장": "대전예술의전당", "지역": "대전", "티켓가격(원)": 15000, "예매율(%)": 73.1, "시작일": "2026-05-12", "종료일": "2026-05-14", "예매하기": "https://www.daejeon.go.kr/djac"},
    {"공연명": "국제현대무용제(MODAFE) 개막작", "단체명": "한국현대무용협회", "장르": "현대무용", "공연장": "아르코예술극장 대극장", "지역": "서울", "티켓가격(원)": 40000, "예매율(%)": 88.5, "시작일": "2026-09-15", "종료일": "2026-09-30", "예매하기": "https://theater.arko.or.kr"},
    {"공연명": "고블린파티 <옛날 옛적에>", "단체명": "고블린파티", "장르": "현대무용", "공연장": "남산국악당", "지역": "서울", "티켓가격(원)": 20000, "예매율(%)": 84.1, "시작일": "2026-07-22", "종료일": "2026-07-25", "예매하기": "https://www.hanokmaeul.or.kr"},

    # --- 한국무용 (13개) ---
    {"공연명": "국립무용단 <전통의 향연>", "단체명": "국립무용단", "장르": "한국무용", "공연장": "국립극장 해오름극장", "지역": "서울", "티켓가격(원)": 40000, "예매율(%)": 84.3, "시작일": "2026-06-10", "종료일": "2026-06-14", "예매하기": "https://www.ntok.go.kr"},
    {"공연명": "경기도무용단 <련(蓮)>", "단체명": "경기도무용단", "장르": "한국무용", "공연장": "경기아트센터 대극장", "지역": "경기", "티켓가격(원)": 20000, "예매율(%)": 69.8, "시작일": "2026-06-20", "종료일": "2026-06-21", "예매하기": "https://www.ggac.or.kr"},
    {"공연명": "국립무용단 <방랑자>", "단체명": "국립무용단", "장르": "한국무용", "공연장": "국립극장 해오름극장", "지역": "서울", "티켓가격(원)": 45000, "예매율(%)": 87.2, "시작일": "2026-11-20", "종료일": "2026-11-23", "예매하기": "https://www.ntok.go.kr"},
    {"공연명": "국립무용단 <향연(饗宴)>", "단체명": "국립무용단", "장르": "한국무용", "공연장": "국립극장 해오름극장", "지역": "서울", "티켓가격(원)": 50000, "예매율(%)": 91.2, "시작일": "2026-09-17", "종료일": "2026-09-21", "예매하기": "https://www.ntok.go.kr"},
    {"공연명": "부산시립무용단 <영남의 춤 가락>", "단체명": "부산시립무용단", "장르": "한국무용", "공연장": "부산시민회관 대극장", "지역": "부산", "티켓가격(원)": 20000, "예매율(%)": 71.3, "시작일": "2026-06-11", "종료일": "2026-06-12", "예매하기": "https://www.bscc.or.kr"},
    {"공연명": "인천시립무용단 <담청(淡青)>", "단체명": "인천시립무용단", "장르": "한국무용", "공연장": "인천문화예술회관", "지역": "인천", "티켓가격(원)": 15000, "예매율(%)": 68.9, "시작일": "2026-07-18", "종료일": "2026-07-19", "예매하기": "https://www.incheon.go.kr/art"},
    {"공연명": "정동극장 <궁:장녹수전>", "단체명": "정동극장 예술단", "장르": "한국무용", "공연장": "국립정동극장", "지역": "서울", "티켓가격(원)": 30000, "예매율(%)": 85.0, "시작일": "2026-05-01", "종료일": "2026-07-31", "예매하기": "https://www.jeongdong.or.kr"},
    {"공연명": "대전시립무용단 <숨고르기>", "단체명": "대전시립무용단", "장르": "한국무용", "공연장": "대전예술의전당", "지역": "대전", "티켓가격(원)": 20000, "예매율(%)": 74.3, "시작일": "2026-08-04", "종료일": "2026-08-06", "예매하기": "https://www.daejeon.go.kr/djac"},
    {"공연명": "전주시립국악단 무용팀 <전주 버꾸춤>", "단체명": "전주시립국악단", "장르": "한국무용", "공연장": "전주덕진예술회관", "지역": "전북", "티켓가격(원)": 10000, "예매율(%)": 65.4, "시작일": "2026-05-18", "종료일": "2026-05-19", "예매하기": "http://art.jeonju.go.kr"},
    {"공연명": "울산시립무용단 <태화강의 춤>", "단체명": "울산시립무용단", "장르": "한국무용", "공연장": "울산문화예술회관", "지역": "울산", "티켓가격(원)": 15000, "예매율(%)": 67.2, "시작일": "2026-10-11", "종료일": "2026-10-12", "예매하기": "https://ucac.ulsan.go.kr"},
    {"공연명": "제주도립무용단 <탐라의 숨결>", "단체명": "제주도립무용단", "장르": "한국무용", "공연장": "제주아트센터", "지역": "제주", "티켓가격(원)": 10000, "예매율(%)": 71.1, "시작일": "2026-09-05", "종료일": "2026-09-06", "예매하기": "http://www.jejusi.go.kr/acenter/index.do"},
    {"공연명": "국립남도국악원 무용극 <진도강강술래>", "단체명": "국립남도국악원", "장르": "한국무용", "공연장": "국립남도국악원 진악당", "지역": "전남", "티켓가격(원)": 10000, "예매율(%)": 78.5, "시작일": "2026-06-25", "종료일": "2026-06-26", "예매하기": "https://jindo.gugak.go.kr"},
    {"공연명": "서울시무용단 <감괘(坎卦)>", "단체명": "서울시무용단", "장르": "한국무용", "공연장": "세종문화회관 대극장", "지역": "서울", "티켓가격(원)": 40000, "예매율(%)": 89.2, "시작일": "2026-05-08", "종료일": "2026-05-10", "예매하기": "https://www.sejongpac.or.kr"}
]
df = pd.DataFrame(data)

# 아이디어 1: 월(Month) 추출 로직
df["월"] = pd.to_datetime(df["시작일"]).dt.month
df["월_display"] = df["월"].map(lambda x: f"{x}월" if lang == "한국어" else f"Month {x}")

# 아이디어 3: 공연장 위치 맵 링크 생성
df["공연장위치"] = df["공연장"].map(lambda x: f"https://map.kakao.com/?q={x.replace(' ', '+')}")

if lang == "English":
    df["장르"] = df["장르"].map({"발레": "Ballet", "현대무용": "Contemporary", "한국무용": "Traditional"})
    df["지역"] = df["지역"].map({
        "서울": "Seoul", "경기": "Gyeonggi", "광주": "Gwangju", "대구": "Daegu", 
        "부산": "Busan", "인천": "Incheon", "대전": "Daejeon", "울산": "Ulsan",
        "제주": "Jeju", "전북": "Jeonbuk", "전남": "Jeonnam", "서울(내한)": "Seoul(Int'l)"
    })

# 표 컬럼명 변환
df_display = df.rename(columns={
    "공연명": t["col_name"], "단체명": t["col_group"], "장르": t["col_genre"],
    "공연장": t["col_venue"], "지역": t["col_region"], "티켓가격(원)": t["col_price"], 
    "예매율(%)": t["col_rate"], "시작일": t["col_start"], "종료일": t["col_end"], 
    "예매하기": t["col_link"], "공연장위치": t["col_map"]
})

# 5. 메인 화면 타이틀 및 가이드박스 출력
st.title(t["title"])
st.markdown(t["sub"])

with st.expander(t["guide_title"]):
    st.markdown(f"- {t['guide_ballet']}")
    st.markdown(f"- {t['guide_contemporary']}")
    st.markdown(f"- {t['guide_traditional']}")

st.markdown("---")

# 6. 사이드바 필터 동작 (40개 데이터에 맞춰 범위 유연 확장)
st.sidebar.header(t["filter_header"])
genres = st.sidebar.multiselect(t["genre_label"], options=df_display[t["col_genre"]].unique(), default=df_display[t["col_genre"]].unique())
regions = st.sidebar.multiselect(t["region_label"], options=df_display[t["col_region"]].unique(), default=df_display[t["col_region"]].unique())

# 아이디어 1: 정렬된 월별 선택 필터
months = st.sidebar.multiselect(t["month_label"], options=sorted(df_display["월_display"].unique(), key=lambda x: int(x.replace('월','').replace('Month ',''))), default=df_display["월_display"].unique())

# 아이디어 2: 티켓 가격 슬라이더 필터
min_price = int(df_display[t["col_price"]].min())
max_price = int(df_display[t["col_price"]].max())
price_range = st.sidebar.slider(t["price_label"], min_value=min_price, max_value=max_price, value=(min_price, max_price), step=5000)

# 최종 4중 교집합 필터링 연산
filtered_df = df_display[
    df_display[t["col_genre"]].isin(genres) & 
    df_display[t["col_region"]].isin(regions) & 
    df_display["월_display"].isin(months) &
    (df_display[t["col_price"]] >= price_range[0]) & 
    (df_display[t["col_price"]] <= price_range[1])
]

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

# 8. 데이터 테이블 출력 및 하이퍼링크 다중 설정 (예매처 & 지도)
st.subheader(t["table_title"])
if not filtered_df.empty:
    st.dataframe(
        filtered_df.drop(columns=["월", "월_display"]), 
        use_container_width=True,
        column_config={
            t["col_link"]: st.column_config.LinkColumn(
                t["col_link"],
                display_text="🔗 " + t["col_link"]
            ),
            t["col_map"]: st.column_config.LinkColumn(
                t["col_map"],
                display_text="📍 Map"
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
