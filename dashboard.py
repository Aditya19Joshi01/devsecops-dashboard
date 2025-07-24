import streamlit as st
import requests

BACKEND_URL = "http://localhost:5000/scan"  # Flask endpoint

st.set_page_config(page_title="DevSecOps Dashboard", layout="wide")
st.title("🔐 DevSecOps Security Scanner")

st.markdown("Enter your GitHub repository URL to scan for vulnerabilities.")

# Input field
repo_url = st.text_input("GitHub Repo URL", placeholder="https://github.com/your/project")

# Scan button
if st.button("Scan Now"):
    if repo_url.strip() == "":
        st.error("Please enter a valid repository URL.")
    else:
        with st.spinner("Scanning..."):
            try:
                response = requests.post(BACKEND_URL, json={"repo_url": repo_url})

                # Show HTTP status
                st.write("Status Code:", response.status_code)

                # Debug raw JSON response
                try:
                    result = response.json()
                except Exception as json_err:
                    st.error("Failed to parse JSON response.")
                    st.text(response.text)
                    raise json_err  # re-throw to show in terminal

                st.success("Scan Complete ✅")

                st.markdown(f"**Repository:** {result.get('repo', '-')}")
                st.markdown(f"**Scan Date:** {result.get('date', '-')}")
                st.markdown(f"**Risk Score:** {result.get('risk_score', '-')}")

                st.subheader("🔎 Vulnerabilities Found:")

                if not result['vulnerabilities']:
                    st.info("No vulnerabilities found.")
                else:
                    for v in result['vulnerabilities']:
                        st.markdown("---")
                        st.write(f"📄 **File:** `{v['filename']}`")
                        st.write(f"🔢 **Line:** {v['line_number']}")
                        st.write(f"⚠️ **Severity:** `{v['issue_severity']}`")
                        st.write(f"🧠 **Issue:** {v['issue_text']}")
                        st.code(v['code'], language='python')

            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.subheader("📈 Scan History Trends")

# Fetch scan history
try:
    history = requests.get("http://localhost:5000/history").json()

    if not history:
        st.info("No scan history found.")
    else:
        import pandas as pd

        # Convert to DataFrame
        df = pd.DataFrame(history)
        df['date'] = pd.to_datetime(df['date'])

        # Sort by date
        df = df.sort_values(by='date')

        # Plot risk scores
        st.line_chart(data=df, x='date', y='risk_score')

        # Optionally show full table
        with st.expander("📋 Show scan history table"):
            st.dataframe(df[['repo', 'date', 'risk_score']])

except Exception as e:
    st.error(f"Failed to fetch history: {e}")


