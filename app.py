import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & Title
st.set_page_config(page_title="K-Dance Stage Hub", layout="wide")
st.title("🩰 K-Dance Stage Hub: Integrated Dashboard for Dance Performances")
st.markdown("### Final Project Portfolio by Eunyul Jung (Student ID: 2025310819)")
st.markdown("This interactive dashboard aggregates and analyzes dance performance data in South Korea, comparing local troupes with international touring companies.")
st.markdown("---")

# 2. Data Loading & Dynamic Column Matching (Prevents KeyError)
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("dance_data.csv")
        
        # --- SMART COLUMN MAPPING ---
        # Checks what columns actually exist in your CSV and maps them safely
        cols = df.columns
        
        # 1. Performance Name Mapping
        name_col = next((c for c in cols if c in ["공연명", "Performance Name", "Performance", "Title", "name"]), None)
        if name_col: df = df.rename(columns={name_col: "Performance Name"})
        else: df["Performance Name"] = "Unnamed Performance"
            
        # 2. Genre Mapping
        genre_col = next((c for c in cols if c in ["장르", "Genre", "genre"]), None)
        if genre_col: df = df.rename(columns={genre_col: "Genre"})
        else: df["Genre"] = "General"
            
        # 3. Origin Mapping (Local vs International)
        origin_col = next((c for c in cols if c in ["구분", "단체구분", "Origin", "origin", "Type"]), None)
        if origin_col: df = df.rename(columns={origin_col: "Origin"})
        else: df["Origin"] = "Local" # Default fallback
            
        # 4. Venue Mapping
        venue_col = next((c for c in cols if c in ["공연장", "Venue", "venue", "Location"]), None)
        if venue_col: df = df.rename(columns={venue_col: "Venue"})
        else: df["Venue"] = "Various Venues"
            
        # 5. Month Mapping
        month_col = next((c for c in cols if c in ["월", "Month", "month", "시작일", "Date"]), None)
        if month_col: df = df.rename(columns={month_col: "Month"})
        else: df["Month"] = "May"
            
        # 6. Ticket Price Mapping (Crucial Fix for KeyError!)
        price_col = next((c for c in cols if "가격" in c or "Price" in c or "price" in c or "티켓" in c), None)
        if price_col: 
            df = df.rename(columns={price_col: "Ticket Price(KRW)"})
            # Convert to numeric safely, removing commas if any
            df["Ticket Price(KRW)"] = pd.to_numeric(df["Ticket Price(KRW)"].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce').fillna(0)
        else: 
            df["Ticket Price(KRW)"] = 0
            
        # 7. Booking Link Mapping
        link_col = next((c for c in cols if "링크" in c or "Link" in c or "link" in c or "URL" in c), None)
        if link_col: df = df.rename(columns={link_col: "Booking Link"})
        else: df["Booking Link"] = "https://www.interpark.com"

    except FileNotFoundError:
        # Fallback Mock Data if file reading completely fails
        mock_data = {
            "Performance Name": ["Korea National Ballet: Swan Lake", "Universal Ballet: Giselle", "Paris Opera Ballet: Giselle Tour", "National Dance Company: Scent of Ink"],
            "Genre": ["Ballet", "Ballet", "Ballet", "Traditional Korean"],
            "Origin": ["Local", "Local", "International Tour", "Local"],
            "Venue": ["Seoul Arts Center", "Arts Center Incheon", "LG Arts Center", "National Theater of Korea"],
            "Month": ["Jan", "March", "May", "May"],
            "Ticket Price(KRW)": [80000, 60000, 150000, 50000],
            "Booking Link": ["https://www.interpark.com", "https://www.interpark.com", "https://www.sac.or.kr", "https://www.ntok.go.kr"]
        }
        df = pd.DataFrame(mock_data)
        
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("🔍 Filter Options")

# Filter by Genre
genre_options = df["Genre"].unique()
selected_genres = st.sidebar.multiselect("Select Genre", options=genre_options, default=genre_options)

# Filter by Origin
origin_options = df["Origin"].unique()
selected_origins = st.sidebar.multiselect("Select Origin", options=origin_options, default=origin_options)

# Apply Sidebar Filters Safely
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

# 5. Advanced Visualizations
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("💰 Price Analysis by Venue & Origin")
    if not filtered_df.empty and filtered_df["Ticket Price(KRW)"].sum() > 0:
        fig_price = px.bar(
            filtered_df, 
            x="Venue", 
            y="Ticket Price(KRW)", 
            color="Origin",
            barmode="group",
            text="Performance Name",
            title="Ticket Price Distribution Across Venues",
            labels={"Ticket Price(KRW)": "Price (KRW)", "Venue": "Performance Venue"}
        )
        st.plotly_chart(fig_price, use_container_width=True)
    else:
        st.info("No price data available or price values are zero.")

with chart_col2:
    st.subheader("📅 Monthly Frequency Tracking (Peak Seasons)")
    if not filtered_df.empty:
        fig_month = px.histogram(
            filtered_df,
            x="Month",
            color="Genre",
            title="Dance Shows Distribution Throughout the Year",
            labels={"Month": "Timeline / Month", "count": "Number of Shows"}
        )
        st.plotly_chart(fig_month, use_container_width=True)
    else:
        st.info("No timeline data available to display.")

st.markdown("---")

# 6. Interactive Data Table
st.subheader("📋 Interactive Data Schedule & Booking")
if not filtered_df.empty:
    st.markdown("Search, sort, or explore the current dance schedule below:")
    st.dataframe(filtered_df, use_container_width=True)
    
    st.markdown("**🔗 Quick Access to Ticketing Platforms:**")
    valid_links = filtered_df.dropna(subset=["Booking Link"])
    if not valid_links.empty:
        link_cols = st.columns(min(len(valid_links), 4))
        for idx, (_, row) in enumerate(valid_links.head(4).iterrows()):
            with link_cols[idx]:
                st.link_button(f"🎟️ {str(row['Performance Name'])[:15]}...", str(row['Booking Link']))
else:
    st.warning("No performance data matches the selected filters.")
