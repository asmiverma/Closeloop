from __future__ import annotations

import streamlit as st


st.set_page_config(page_title="Closeloop", layout="centered")
st.title("Closeloop Sales Workflow")
st.caption("Phase 1 scaffold in progress")

company_name = st.text_input("Company name")
run_clicked = st.button("Run workflow", disabled=True)

if run_clicked:
    st.info("Pipeline implementation starts in later phases.")
