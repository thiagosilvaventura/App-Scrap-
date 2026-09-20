"""
Analyzer Pro Max - core analysis engine.

This module extends the original `analyzerpy.py` cross-dataset comparison
(`process_datasets`, kept intact below with the same name and behavior so
nothing that already calls it breaks) with two additions:

  1. Individual dataset ranking: for one loaded dataset, rank every column by
     - fill_rate_pct: how much data it has (quantity)
     - avg_similarity_pct: how similar its values are to the same column in
       every other loaded dataset (Jaccard similarity of unique values)

  2. Export helpers: write a report to CSV, or produce a copy-ready text block.

Pure pandas, no UI dependencies, so any front end (Streamlit, Flask, a
notebook, a CLI) can reuse it unchanged.
"""

import pandas as pd
import os

# Values treated as "missing" in addition to real NaN (case-insensitive).
MISSING_TOKENS = {"", "-", "n/a", "null", "nan", "none"}


def _load_dataset(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return pd.read_csv(path)
    if ext in (".xls", ".xlsx"):
        return pd.read_excel(path)
    raise ValueError(f"Unsupported file type: {path}")


def load_datasets(file_paths: list[str]) -> list[dict]:
    """Load a list of file paths into {'name', 'df'} dicts, skipping unsupported files."""
    datasets = []
    for path in file_paths:
        try:
            df = _load_dataset(path)
        except ValueError:
            continue
        datasets.append({"name": os.path.basename(path), "df": df})
    return datasets


def _clean_series(s: pd.Series) -> pd.Series:
    """Strip strings and drop values considered 'missing'."""
    cleaned = s.dropna().astype(str).str.strip()
    return cleaned[~cleaned.str.lower().isin(MISSING_TOKENS)]


# ---------------------------------------------------------------------------
# Original cross-dataset comparison — same name, same behavior as analyzerpy.py
# ---------------------------------------------------------------------------

def process_datasets(file_paths: list[str]) -> str:
    """
    Reads multiple spreadsheet files (CSV, XLS, XLSX) using pandas,
    identifies common primary key columns, maps variable coverage across datasets,
    and returns a formatted analysis report string.
    """
    if len(file_paths) < 2:
        return "Error: At least 2 files are required for analysis."

    datasets = load_datasets(file_paths)

    if not datasets:
        return "Error: No valid CSV/Excel files were loaded."

    # 2. Identify common columns (variables) across all datasets
    common_cols = set(datasets[0]["df"].columns)
    for ds in datasets[1:]:
        common_cols = common_cols.intersection(set(ds["df"].columns))

    common_cols_list = list(common_cols)

    if not common_cols_list:
        return "Error: No common columns/variables found across all selected datasets!"

    # Automatically select the first common column as the primary key
    key_col = common_cols_list[0]

    # 3. Collect unique key values across all datasets
    unique_keys = set()
    for ds in datasets:
        df = ds["df"]
        if key_col in df.columns:
            unique_keys.update(_clean_series(df[key_col]).tolist())

    # 4. Map all unique columns existing across all combined datasets
    all_columns = set()
    for ds in datasets:
        all_columns.update(ds["df"].columns)

    # 5. Build analysis report string
    total_datasets = len(datasets)
    report_lines = [
        "=== ANALYSIS REPORT ===",
        f"Analyzed Databases: {total_datasets}",
        f"Common Key Used: \"{key_col}\"",
        f"Total Unique Records (Key): {len(unique_keys)}\n",
        "--- % Variable Appearance by Database ---"
    ]

    for col in sorted(all_columns):
        count_in_datasets = sum(1 for ds in datasets if col in ds["df"].columns)
        percentage = (count_in_datasets / total_datasets) * 100
        report_lines.append(f"• {col}: {percentage:.1f}% ({count_in_datasets}/{total_datasets} databases)")

    return "\n".join(report_lines)


def cross_dataset_table(datasets: list[dict], key_col: str | None = None) -> dict:
    """
    Same analysis as `process_datasets`, but returns structured data
    (a DataFrame plus summary numbers) instead of a text block, for UIs
    that want to render bars/tables rather than plain text.
    """
    common_cols = set(datasets[0]["df"].columns)
    for ds in datasets[1:]:
        common_cols = common_cols.intersection(set(ds["df"].columns))
    common_cols_list = sorted(common_cols)

    if key_col is None or key_col not in common_cols_list:
        key_col = common_cols_list[0] if common_cols_list else None

    unique_keys = set()
    if key_col:
        for ds in datasets:
            if key_col in ds["df"].columns:
                unique_keys.update(_clean_series(ds["df"][key_col]).tolist())

    all_columns = set()
    for ds in datasets:
        all_columns.update(ds["df"].columns)

    total = len(datasets)
    rows = []
    for col in sorted(all_columns):
        count_in = sum(1 for ds in datasets if col in ds["df"].columns)
        rows.append({
            "variable": col,
            "present_in": count_in,
            "total_datasets": total,
            "percentage": round(count_in / total * 100, 1),
        })

    return {
        "table": pd.DataFrame(rows),
        "common_columns": common_cols_list,
        "key_col": key_col,
        "unique_keys_count": len(unique_keys),
        "total_datasets": total,
    }


# ---------------------------------------------------------------------------
# New: individual dataset ranking (quantity + similarity)
# ---------------------------------------------------------------------------

def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union) * 100


def rank_individual_variables(datasets: list[dict], base_index: int) -> pd.DataFrame:
    """
    Rank every column of one dataset by:
      - fill_rate_pct: % of non-missing values (quantity)
      - avg_similarity_pct: average Jaccard similarity of this column's unique
        values against the same column in every other loaded dataset that has
        it (None if no other dataset shares this column)

    Returns a DataFrame sorted by fill_rate_pct desc; re-sort by
    avg_similarity_pct in the UI layer if the user wants that ranking instead.
    """
    base = datasets[base_index]
    base_df = base["df"]
    others = [ds for i, ds in enumerate(datasets) if i != base_index]
    total_rows = len(base_df)

    rows = []
    for col in base_df.columns:
        cleaned = _clean_series(base_df[col])
        non_null = len(cleaned)
        fill_rate_pct = (non_null / total_rows * 100) if total_rows else 0.0
        unique_vals = set(cleaned.tolist())
        cardinality_pct = (len(unique_vals) / non_null * 100) if non_null else 0.0

        peers = [o for o in others if col in o["df"].columns]
        if peers:
            scores = []
            for o in peers:
                other_vals = set(_clean_series(o["df"][col]).tolist())
                scores.append(_jaccard(unique_vals, other_vals))
            avg_similarity_pct = round(sum(scores) / len(scores), 1)
        else:
            avg_similarity_pct = None

        rows.append({
            "variable": col,
            "fill_rate_pct": round(fill_rate_pct, 1),
            "non_null_count": non_null,
            "total_rows": total_rows,
            "unique_values": len(unique_vals),
            "cardinality_pct": round(cardinality_pct, 1),
            "avg_similarity_pct": avg_similarity_pct,
            "present_in_datasets": f"{len(peers) + 1}/{len(datasets)}",
        })

    result = pd.DataFrame(rows)
    return result.sort_values("fill_rate_pct", ascending=False).reset_index(drop=True)


def rank_all_datasets(datasets: list[dict]) -> dict:
    """Convenience wrapper: individual ranking for every loaded dataset, keyed by name."""
    return {ds["name"]: rank_individual_variables(datasets, i) for i, ds in enumerate(datasets)}


# ---------------------------------------------------------------------------
# Export helpers
# ---------------------------------------------------------------------------

def export_csv(df: pd.DataFrame, output_path: str) -> str:
    """Write a DataFrame to CSV and return the path."""
    df.to_csv(output_path, index=False)
    return output_path


def to_copy_text(df: pd.DataFrame) -> str:
    """Tab-separated text block, ready to paste into a spreadsheet or chat."""
    return df.to_csv(index=False, sep="\t")
```[cite: 7]
