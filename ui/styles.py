from __future__ import annotations

import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f8fafc;
            --card: #ffffff;
            --text: #0f172a;
            --muted: #64748b;
            --primary: #2563eb;
            --success: #16a34a;
            --warning: #f59e0b;
            --danger: #dc2626;
        }
        html, body, [data-testid="stAppViewContainer"] {
            background: var(--bg);
            color: var(--text);
        }
        .block-container {
            padding-top: 2rem;
        }
        div[data-testid="stFileUploader"] {
            background: var(--card);
            border-radius: 12px;
        }
        .stMetric {
            background: var(--card);
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
