import streamlit as st
from extractor.parser import parse_filing
from extractor.llm_extract import extract_metrics
from extractor.anomaly import detect_anomalies
from extractor.excel_export import build_excel_report

st.set_page_config(page_title="FinDoc Extractor", page_icon="📄", layout="wide")

st.title("📄 FinDoc Extractor")
st.caption(
    "Upload an SEC 10-K or 10-Q filing (PDF or HTML) to extract key financial metrics, "
    "detect anomalies, and download a formatted Excel report."
)

with st.sidebar:
    st.header("About")
    st.markdown(
        "**FinDoc Extractor** uses GPT-4o to parse SEC filings and surface:\n"
        "- Revenue, EPS, EBITDA, Debt metrics\n"
        "- Year-over-year changes\n"
        "- Anomaly flags (revenue drops, audit issues, negative EBITDA)\n"
        "- Formatted Excel export\n\n"
        "Built with GitHub Copilot · Microsoft AI Skills Fest 2026"
    )

uploaded = st.file_uploader(
    "Upload SEC Filing (PDF or HTML)",
    type=["pdf", "html", "htm"],
    help="Download filings from sec.gov/cgi-bin/browse-edgar",
)

if uploaded:
    col_status, col_size = st.columns([3, 1])
    with col_status:
        st.info(f"Processing: **{uploaded.name}**")
    with col_size:
        st.metric("File Size", f"{len(uploaded.getvalue()) / 1024:.1f} KB")

    with st.spinner("Step 1/3 — Parsing document..."):
        filing_bytes = uploaded.getvalue()
        text = parse_filing(filing_bytes, uploaded.name)
    st.success(f"Parsed {len(text):,} characters")

    with st.spinner("Step 2/3 — Extracting financial metrics via GPT-4o..."):
        try:
            metrics = extract_metrics(text)
        except Exception as e:
            st.error(f"Extraction failed: {e}")
            st.stop()

    with st.spinner("Step 3/3 — Running anomaly detection..."):
        anomalies = detect_anomalies(metrics)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Extracted Metrics")
        display = {k: v for k, v in metrics.items() if v is not None}
        st.json(display)

    with col2:
        severity_icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}
        st.subheader(f"Anomaly Flags — {len(anomalies)} found")
        if not anomalies:
            st.success("No anomalies detected. Filing looks clean.")
        for flag in anomalies:
            icon = severity_icon.get(flag["severity"], "⚪")
            with st.expander(f"{icon} **{flag['severity']}** — {flag['flag']}"):
                st.write(flag["detail"])

    st.divider()

    company = metrics.get("company_name", "filing")
    year = metrics.get("fiscal_year", "")
    filename = f"findoc_{company}_{year}.xlsx".replace(" ", "_")

    excel_bytes = build_excel_report(metrics, anomalies)
    st.download_button(
        label="Download Excel Report",
        data=excel_bytes,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
