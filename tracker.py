import pandas as pd
import streamlit as st

# ---------- Page Config ----------
st.set_page_config(page_title="📈 Inflation Tracker", layout="wide")

# ---------- Custom Styling ----------
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 2rem;
    }
    h1.title {
        text-align: center;
        font-size: 2.8em;
        background: linear-gradient(90deg, #4A90E2, #50E3C2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    .subheader {
        text-align: center;
        font-size: 1.1em;
        color: #555;
        margin-top: -1em;
        margin-bottom: 1.5em;
    }
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.05);
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("<h1 class='title'>📈 Inflation Impact Tracker</h1>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Visualize inflation trends using U.S. CPI data</div>", unsafe_allow_html=True)
st.markdown("---")

# ---------- Sidebar Upload ----------
with st.sidebar:
    st.header("📂 Upload CPI Data")
    uploaded_file = st.file_uploader("Upload CPI CSV", type="csv")
    st.caption("If no file is uploaded, default `CPIAUCSL.csv` will be used.")

# ---------- Load Data ----------
@st.cache_data
def load_cpi_data(csv_file=None):
    try:
        if csv_file is not None:
            cpi = pd.read_csv(csv_file)
        else:
            cpi = pd.read_csv("CPIAUCSL.csv")

        if 'observation_date' in cpi.columns and 'CPIAUCSL' in cpi.columns:
            cpi = cpi.rename(columns={"observation_date": "date", "CPIAUCSL": "cpi"})
            cpi["date"] = pd.to_datetime(cpi["date"])
            return cpi
        else:
            st.error("❌ CSV must contain 'observation_date' and 'CPIAUCSL'.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

cpi_data = load_cpi_data(uploaded_file)

# ---------- Display ----------
if not cpi_data.empty:
    st.markdown("## 🔍 Overview")

    col1, col2, col3 = st.columns(3)
    with col1:
        latest_date = cpi_data["date"].max().strftime("%B %Y")
        st.metric("📆 Latest CPI Date", latest_date)

    with col2:
        latest_cpi = cpi_data["cpi"].iloc[-1]
        st.metric("💹 CPI Value", f"{latest_cpi:.2f}")

    with col3:
        change = cpi_data["cpi"].pct_change().iloc[-1] * 100
        st.metric("📊 Monthly CPI Change", f"{change:.2f}%")

    st.markdown("## 📉 CPI Over Time")
    st.line_chart(cpi_data.set_index("date")["cpi"])

    with st.expander("📄 View Raw Data"):
        st.dataframe(cpi_data.tail(25))
else:
    st.warning("📤 Upload a valid CPI CSV file to begin.")






