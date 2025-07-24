import streamlit as st
import requests
import pandas as pd

# Config
BACKEND_URL = "http://backend:5000/scan"
HISTORY_URL = "http://backend:5000/history"

# Page setup
st.set_page_config(page_title="DevSecOps Security Dashboard", layout="wide")
st.title("🔐 DevSecOps Security Scanner")
st.markdown("Scan your GitHub repositories for security vulnerabilities using Bandit + AI summarization.")

# ---- Sidebar: Input ----
st.sidebar.header("📥 Scan a Repository")
repo_url = st.sidebar.text_input("GitHub Repo URL", placeholder="https://github.com/your/project")

if st.sidebar.button("🚀 Run Scan"):
    if not repo_url.strip():
        st.sidebar.error("Please enter a valid URL.")
    else:
        with st.spinner("Scanning repo and analyzing vulnerabilities..."):
            try:
                res = requests.post(BACKEND_URL, json={"repo_url": repo_url})
                if res.status_code == 200:
                    data = res.json()

                    st.success("✅ Scan complete")
                    st.markdown(f"**📦 Repository:** `{data.get('repo')}`")
                    st.markdown(f"🕒 **Scan Date:** `{data.get('date')}`")
                    st.markdown(f"🎯 **Risk Score:** `{data.get('risk_score')}`")

                    # --- Vulnerability Results ---
                    st.subheader("🔍 Vulnerabilities Found")
                    if not data['vulnerabilities']:
                        st.info("✅ No vulnerabilities found!")
                    else:
                        for v in data['vulnerabilities']:
                            with st.container():
                                st.markdown("---")
                                cols = st.columns([3, 1, 1])
                                cols[0].markdown(f"**📄 File:** `{v['filename']}`")
                                cols[1].markdown(f"**Line:** `{v['line_number']}`")
                                cols[2].markdown(f"**Severity:** `{v['issue_severity']}`")
                                st.markdown(f"**🧠 Issue:** {v['issue_text']}")
                                st.code(v['code'], language='python')

                    # --- AI Summary ---
                    if "report_summary" in data:
                        st.subheader("🤖 AI-Generated Summary")
                        st.success(data["report_summary"])
                    else:
                        st.warning("No summary available.")

                else:
                    st.error("❌ Error from backend.")
            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")

# ---- Historical Trends ----
st.subheader("📈 Risk Score Trend (Scan History)")

try:
    history = requests.get(HISTORY_URL).json()

    if not history:
        st.info("No previous scans yet.")
    else:
        df = pd.DataFrame(history)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date')

        st.line_chart(data=df, x='date', y='risk_score')

        with st.expander("📋 View Scan History Table"):
            st.dataframe(df[['repo', 'date', 'risk_score']])

except Exception as e:
    st.error(f"Failed to fetch history: {e}")
