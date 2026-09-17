import pandas as pd
import os

def process_datasets(file_paths: list[str]) -> str:
    """
    Reads multiple spreadsheet files (CSV, XLS, XLSX) using pandas,
    identifies common primary key columns, maps variable coverage across datasets,
    and returns a formatted analysis report string.
    """
    if len(file_paths) < 2:
        return "Error: At least 2 files are required for analysis."

    datasets = []
    
    try:
        # 1. Read files into DataFrames
        for path in file_paths:
            file_name = os.path.basename(path)
            ext = os.path.splitext(path)[1].lower()
            
            if ext == '.csv':
                df = pd.read_csv(path)
            elif ext in ['.xls', '.xlsx']:
                df = pd.read_excel(path)
            else:
                continue
                
            datasets.append({"name": file_name, "df": df})
            
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
                keys = df[key_col].dropna().astype(str).str.strip().tolist()
                unique_keys.update(keys)

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

        # Calculate presence percentage for each column
        for col in sorted(all_columns):
            count_in_datasets = sum(1 for ds in datasets if col in ds["df"].columns)
            percentage = (count_in_datasets / total_datasets) * 100
            report_lines.append(f"• {col}: {percentage:.1f}% ({count_in_datasets}/{total_datasets} databases)")

        return "\n".join(report_lines)

    except Exception as error:
        return f"Error processing files: {str(error)}"