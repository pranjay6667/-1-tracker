import pandas as pd
import streamlit as st

# ---------- Page Config ----------
st.set_page_config(page_title="📈 Inflation Tracker", layout="wide")

# ---------- Header ----------
st.markdown("""
    <h1 style='text-align: center; color: #4A90E2;'>📈 Inflation Impact Tracker</h1>
    <p style='text-align: center; font-size: 18px;'>Track and visualize historical inflation using CPI data from the U.S. Bureau of Labor Statistics</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------- Sidebar Upload ----------
with st.sidebar:
    st.header("📂 Data Source")
    uploaded_file = st.file_uploader("Upload CPI CSV", type="csv")
    st.markdown("If no file is uploaded, default `CPIAUCSL.csv` will be used.")

# ---------- Load Data ----------
@st.cache_data
def load_cpi_data(csv_file=None):
    try:
        if csv_file is not None:
            cpi = pd.read_csv(csv_file)
        else:
            cpi = pd.read_csv("CPIAUCSL.csv")

        # Rename columns
        if 'observation_date' in cpi.columns and 'CPIAUCSL' in cpi.columns:
            cpi = cpi.rename(columns={"observation_date": "date", "CPIAUCSL": "cpi"})
            cpi["date"] = pd.to_datetime(cpi["date"])
            return cpi
        else:
            st.error("❌ Columns must include 'observation_date' and 'CPIAUCSL'")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

cpi_data = load_cpi_data(uploaded_file)

# ---------- Display ----------
if not cpi_data.empty:
    col1, col2 = st.columns(2)

    with col1:
        latest_date = cpi_data["date"].max().strftime("%B %Y")
        latest_cpi = cpi_data["cpi"].iloc[-1]
        st.metric("📆 Latest CPI Date", latest_date)
        st.metric("💹 CPI Value", f"{latest_cpi:.2f}")

    with col2:
        change = cpi_data["cpi"].pct_change().iloc[-1] * 100
        st.metric("📊 Monthly CPI Change", f"{change:.2f}%")

    st.markdown("### 📉 CPI Over Time")
    st.line_chart(cpi_data.set_index("date")["cpi"])

    with st.expander("🧾 View Raw Data"):
        st.dataframe(cpi_data.tail(20))
else:
    st.info("Upload a valid CPI CSV to get started.")






