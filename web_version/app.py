"""
Analyzer Pro Max - Streamlit front end.

All analysis is done by `analyzer_core.py` (pure pandas). This file only
handles file upload, layout, and the TMX Pro Max visual theme (dark glass
panels, neon green / cyan accents) via custom CSS.

Run with:
    pip install streamlit pandas openpyxl xlrd
    streamlit run app.py
"""

import tempfile
import os
import streamlit as st
import analyzer_core as ac

st.set_page_config(page_title="Analyzer Pro Max", page_icon="🟢", layout="wide")

# ---------------------------------------------------------------------------
# TMX Pro Max visual theme (neon green / cyan on a dark glass panel)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    :root {
        --az-green: #00ff41;
        --az-cyan: #00ffff;
    }

    .stApp {
        background: radial-gradient(circle at 20% 0%, #0d1a10 0%, #05070a 45%, #030403 100%);
        color: #e2e8f0;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }

    h1, h2, h3 {
        color: var(--az-green) !important;
        text-shadow: 0 0 8px rgba(0,255,65,0.35);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* file uploader drop zone */
    section[data-testid="stFileUploaderDropzone"] {
        background: rgba(0,0,0,0.25) !important;
        border: 1px dashed rgba(255,255,255,0.25) !important;
        border-radius: 8px !important;
    }
    section[data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--az-green) !important;
        background: rgba(0,255,65,0.06) !important;
    }

    /* metrics */
    div[data-testid="stMetric"] {
        background: rgba(0,0,0,0.35);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 8px;
        padding: 10px 14px;
    }
    div[data-testid="stMetricValue"] { color: var(--az-green) !important; }

    /* buttons */
    .stButton > button, .stDownloadButton > button {
        background: linear-gradient(135deg, rgba(0,200,50,0.9) 0%, rgba(0,150,30,0.9) 100%);
        color: #000; border: 1px solid var(--az-green); border-radius: 6px;
        font-weight: 700; box-shadow: 0 0 10px rgba(0,255,65,0.2);
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: linear-gradient(135deg, rgba(0,255,65,1) 0%, rgba(0,200,50,1) 100%);
        box-shadow: 0 0 15px rgba(0,255,65,0.4);
    }

    /* tabs */
    button[data-baseweb="tab"] { color: rgba(255,255,255,0.6); font-weight: 700; text-transform: uppercase; }
    button[data-baseweb="tab"][aria-selected="true"] { color: var(--az-green) !important; }

    /* progress bar used for coverage % */
    div[data-testid="stProgress"] > div > div > div {
        background-image: linear-gradient(90deg, rgba(0,200,50,0.8), var(--az-green));
    }

    /* dataframe / table */
    div[data-testid="stDataFrame"] { border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.title("Analyzer Pro Max")
st.caption("Variable comparison and analysis across datasets — pandas-powered")

# ---------------------------------------------------------------------------
# File upload (drag-and-drop is native to st.file_uploader)
# ---------------------------------------------------------------------------
uploaded_files = st.file_uploader(
    "Drop CSV / XLS / XLSX files here (2 or more for cross-dataset comparison)",
    type=["csv", "xls", "xlsx"],
    accept_multiple_files=True,
)

if not uploaded_files:
    st.info("Upload at least one dataset to start. Files are processed locally in this session only.")
    st.stop()

# Persist uploads to temp files so analyzer_core (which reads by path) can load them.
tmp_dir = tempfile.mkdtemp(prefix="analyzer_pro_max_")
paths = []
for f in uploaded_files:
    p = os.path.join(tmp_dir, f.name)
    with open(p, "wb") as out:
        out.write(f.getbuffer())
    paths.append(p)

datasets = ac.load_datasets(paths)

st.write(
    " · ".join(f"📄 **{d['name']}** ({len(d['df'])} rows, {len(d['df'].columns)} columns)" for d in datasets)
)

tab_cross, tab_individual = st.tabs(["Cross-dataset comparison", "Individual analysis"])

# ---------------------------------------------------------------------------
# Tab 1: cross-dataset comparison (same logic as the original process_datasets)
# ---------------------------------------------------------------------------
with tab_cross:
    if len(datasets) < 2:
        st.warning("Load at least 2 datasets to compare variables across them.")
    else:
        common_cols = ac.cross_dataset_table(datasets)["common_columns"]
        key_col = st.selectbox("Primary key (common column)", common_cols, key="key_col")
        result = ac.cross_dataset_table(datasets, key_col=key_col)

        c1, c2, c3 = st.columns(3)
        c1.metric("Datasets analyzed", result["total_datasets"])
        c2.metric("Common columns", len(result["common_columns"]))
        c3.metric("Unique records (key)", result["unique_keys_count"])

        st.markdown("#### Variable presence by dataset")
        for _, row in result["table"].iterrows():
            label = f"🔑 {row['variable']}" if row["variable"] == key_col else row["variable"]
            st.write(f"**{label}** — {row['percentage']}% ({row['present_in']}/{row['total_datasets']} datasets)")
            st.progress(row["percentage"] / 100)

        report_text = ac.process_datasets(paths)
        st.markdown("#### Report")
        st.code(report_text, language="text")  # built-in copy button

        st.download_button(
            "⬇ Export CSV",
            data=result["table"].to_csv(index=False),
            file_name="analyzer-cross-comparison.csv",
            mime="text/csv",
        )

# ---------------------------------------------------------------------------
# Tab 2: individual dataset ranking (quantity + similarity)
# ---------------------------------------------------------------------------
with tab_individual:
    names = [d["name"] for d in datasets]
    selected_name = st.selectbox("Selected dataset", names, key="base_dataset")
    base_index = names.index(selected_name)

    sort_by = st.radio(
        "Rank by",
        ["Quantity (fill rate)", "Similarity"],
        horizontal=True,
    )

    ranking = ac.rank_individual_variables(datasets, base_index)
    if sort_by == "Similarity":
        ranking = ranking.sort_values("avg_similarity_pct", ascending=False, na_position="last")

    st.dataframe(
        ranking,
        use_container_width=True,
        column_config={
            "fill_rate_pct": st.column_config.ProgressColumn(
                "Fill rate", min_value=0, max_value=100, format="%.1f%%"
            ),
            "avg_similarity_pct": st.column_config.ProgressColumn(
                "Avg. similarity", min_value=0, max_value=100, format="%.1f%%"
            ),
        },
        hide_index=True,
    )

    st.markdown("#### Report")
    st.code(ac.to_copy_text(ranking), language="text")  # built-in copy button

    st.download_button(
        "⬇ Export CSV",
        data=ranking.to_csv(index=False),
        file_name=f"analyzer-ranking-{selected_name}.csv",
        mime="text/csv",
    )
