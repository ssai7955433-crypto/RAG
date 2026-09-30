from __future__ import annotations

import streamlit as st


def status_badge(label: str, ok: bool) -> None:
    color = "#16a34a" if ok else "#dc2626"
    st.markdown(
        f"<span style='display:inline-block; background:{color}; color:white; border-radius:999px; padding:6px 12px; font-size:12px; font-weight:600;'>{label}</span>",
        unsafe_allow_html=True,
    )
