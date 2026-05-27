import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & Title
st.set_page_config(page_title="K-Dance Stage Hub", layout="wide")
st.title("🩰 K-Dance Stage Hub: Integrated Dashboard for Dance Performances")
st.markdown("### Final Project Portfolio by Eunyul Jung (Student ID: 2025310819)")
st.markdown("This interactive dashboard aggregates and analyzes dance performance data in South Korea, comparing local troupes with international touring companies.")
st.markdown("---")

# 2. Data Loading with Standardized Schema
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("dance_data.csv")
    except FileNotFoundError:
        # Create mock data aligned with the proposal if file is not found yet
        mock_data = {
            "Performance Name": [
                "Korea National Ballet: Swan Lake", "Universal Ballet: Giselle", 
                "Paris Opera Ballet: Giselle Tour", "National Dance Company: Scent of Ink",
                "Nederlands Dans Theater (NDT) Tour", "Seoul Performing Arts Festival (SPAF)"
            ],
            "Genre": ["Ballet", "Ballet", "Ballet", "Traditional Korean", "Contemporary", "Contemporary"],
            "Origin": ["Local", "Local", "International Tour", "Local", "International Tour", "Local"],
            "Venue": ["Seoul Arts Center", "Arts Center Incheon", "LG Arts Center", "National Theater of Korea", "LG Arts Center", "Arko Arts Theater"],
            "Month": ["Jan", "March", "May", "May", "July", "October"],
            "Ticket Price(KRW)": [80000, 60000, 150000, 50000, 180000, 40000],
            "Booking Link": ["https://www.interpark.com", "https://www.interpark.com", "https://www.sac.or.kr", "https://www.ntok.go.kr", "https://www.lgart.com", "https://theater.arko.or.kr"]
        }
        df = pd.DataFrame(mock_data)
    
    # Ensure standard mapping to prevent layout breaking
    column_mapping = {
        "공연명": "Performance Name", "장르": "Genre", "구분": "Origin", "단체구분": "Origin",
        "공연장": "Venue", "월": "Month", "티켓가격": "Ticket Price(KRW)", "가격": "Ticket Price(KRW)",
        "예매링크": "Booking Link"
    }
    df = df.rename(columns=column_mapping)
    return df

df = load_data()

# 3. Sidebar Filters (Key Feature 1: Performance Filtering)
st.sidebar.header("🔍 Filter Options")

# Filter by Genre
if "Genre" in df.columns:
    genre_options = df["Genre"].unique()
    selected_genres = st.sidebar.multiselect("Select Genre", options=genre_options, default=genre_options)
else:
    selected_genres = []

# Filter by Origin (Local vs International Tour)
if "Origin" in df.columns:
    origin_options = df["Origin"].unique()
    selected_origins = st.sidebar.multiselect("Select Origin", options=origin_options, default=origin_options)
else:
    selected_origins = []

# Apply Sidebar Filters
filtered_df = df.copy()
if selected_genres:
    filtered_df = filtered_df[filtered_df["Genre"].isin(selected_genres)]
if selected_origins:
    filtered_df = filtered_df[filtered_df["Origin"].isin(selected_origins)]

# 4. Top Summary Metrics
st.markdown("### 📊 Key Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Tracked Shows", f"{len(filtered_df)} Events")
with col2:
    avg_price = filtered_df["Ticket Price(KRW)"].mean() if not filtered_df.empty else 0
    st.metric("Average Ticket Price", f"{int(avg_price):,} KRW")
with col3:
    local_count = len(filtered_df[filtered_df["Origin"] == "Local"]) if not filtered_df.empty else 0
    st.metric("Local Troupe Shows", f"{local_count} Events")

st.markdown("---")

# 5. Advanced Visualizations (Key Features 2 & 3)
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("💰 Price Analysis by Venue & Origin")
    if not filtered_df.empty:
        # Plotly Bar chart for professional comparison
        fig_price = px.bar(
            filtered_df, 
            x="Venue", 
            y="Ticket Price(KRW)", 
            color="Origin",
            barmode="group",
            text="Performance Name",
            title="Ticket Price Distribution Across Venues",
            labels={"Ticket Price(KRW)": "Price (KRW)", "Venue": "Performance Venue"},
            color_discrete_map={"Local": "#1f77b4", "International Tour": "#ff7f0e"}
        )
        st.plotly_chart(fig_price, use_container_width=True)
    else:
        st.info("No data available to display the price chart.")

with chart_col2:
    st.subheader("📅 Monthly Frequency Tracking (Peak Seasons)")
    if not filtered_df.empty:
        # Define month order for correct chronological display
        month_order = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
        
        fig_month = px.histogram(
            filtered_df,
            x="Month",
            color="Genre",
            title="Dance Shows Distribution Throughout the Year",
            category_orders={"Month": month_order},
            labels={"Month": "Month of the Year", "count": "Number of Shows"}
        )
        st.plotly_chart(fig_month, use_container_width=True)
    else:
        st.info("No data available to display the monthly trends.")

st.markdown("---")

# 6. Interactive Data Table (Key Feature 4)
st.subheader("📋 Interactive Data Schedule & Booking")
if not filtered_df.empty:
    st.markdown("Search, sort, or explore the current dance schedule below:")
    
    # Display the dataset beautifully
    st.dataframe(filtered_df, use_container_width=True)
    
    # Quick Link Access Section
    st.markdown("**🔗 Quick Access to Ticketing Platforms:**")
    link_cols = st.columns(len(filtered_df.head(4)))
    for idx, row in filtered_df.head(4).iterrows():
        with link_cols[idx % 4]:
            st.link_button(f"🎟️ {row['Performance Name'][:20]}...", row['Booking Link'])
else:
    st.warning("No performance data matches the selected filters.")
