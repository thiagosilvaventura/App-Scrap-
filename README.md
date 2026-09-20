# 🚀App scrap


Web Analyzer Pro Max

> **Local dataset comparison and variable analysis — powered by Pandas and Streamlit.**

Analyzer Pro Max is a sleek, dark-themed web application designed for **data analysts, developers, and risk/data teams** who need to quickly compare, cross-reference, and analyze multiple datasets.

The application processes datasets locally within the Streamlit session and provides automated metrics for **data completeness, cardinality, variable presence, and cross-dataset similarity**.

Supported formats:

* `.csv`
* `.xls`
* `.xlsx`

---


<img width="1346" height="605" alt="image" src="https://github.com/user-attachments/assets/132dcaf4-1ac4-40c9-8b42-13e66591e042" />
<img width="1336" height="570" alt="image" src="https://github.com/user-attachments/assets/95618c8f-3918-4520-9d5e-e78cda2d41ee" />
<img width="1307" height="604" alt="image" src="https://github.com/user-attachments/assets/7e38eac1-de99-4e30-9d5d-91d213f107fa" />



## ✨ Key Features

| Feature                         | Description                                                              |
| ------------------------------- | ------------------------------------------------------------------------ |
| 📂 **Drag & Drop Upload**       | Upload multiple datasets directly through the Streamlit interface.       |
| 📊 **Cross-Dataset Comparison** | Automatically identifies variables shared across uploaded datasets.      |
| 🔎 **Variable Analysis**        | Analyze non-null values, unique values, fill rates, and cardinality.     |
| 📈 **Similarity Metrics**       | Compare variable presence and characteristics across different datasets. |
| 🎛️ **Dynamic Ranking**         | Rank variables by quantity/fill rate or similarity.                      |
| 🔑 **Common Key Detection**     | Helps identify potential common identifiers and primary-key candidates.  |
| 💾 **Multiple Formats**         | Supports CSV, XLS, and XLSX files.                                       |
| 🔒 **Local Processing**         | Dataset processing is performed locally within the application session.  |
| ⚡ **Pandas Powered**            | Uses Pandas for efficient tabular-data processing and analysis.          |
| 🌑 **Dark UI**                  | Designed with a modern dark-themed analytical interface.                 |

---

## 🖥️ Application Preview

### 1. Drag & Drop Upload Interface

The application provides a simple interface for uploading multiple datasets simultaneously.


---

### 2. Cross-Dataset Analysis Dashboard

After uploading the datasets, Analyzer Pro Max automatically compares variables across the available files.



---

### 3. Dynamic Variable Ranking

Variables can be ranked according to metrics such as **fill rate, quantity, cardinality, and similarity**.



> **Image paths:** Replace the filenames above with the actual image filenames you upload to the repository.
> Recommended structure:
>
> `images/upload-interface.png`
> `images/cross-dataset-analysis.png`
> `images/dynamic-ranking.png`

---

# 📊 Analysis Metrics

Analyzer Pro Max calculates several metrics for each detected variable.

| Metric               | Description                                                                             |
| -------------------- | --------------------------------------------------------------------------------------- |
| **Fill Rate**        | Percentage of rows containing a non-null value.                                         |
| **Non-Null Count**   | Number of populated values in the variable.                                             |
| **Total Rows**       | Total number of records in the dataset.                                                 |
| **Unique Values**    | Number of distinct values found in the variable.                                        |
| **Cardinality %**    | Percentage of unique values relative to the total number of rows.                       |
| **Dataset Presence** | Number of uploaded datasets containing the variable.                                    |
| **Similarity**       | Cross-dataset comparison based on variable presence and available data characteristics. |

---

## 📋 Example Output

For example, uploading datasets such as:

* `user_risk_profiles.csv`
* `transactions_log.csv`

can produce an analytical table similar to:

| Variable          | Fill Rate | Non-Null Count | Total Rows | Unique Values | Cardinality | Present in Datasets |
| ----------------- | --------: | -------------: | ---------: | ------------: | ----------: | ------------------: |
| `user_id`         | 🟢 100.0% |             50 |         50 |            50 |        100% |                 2/2 |
| `risk_score`      | 🟢 100.0% |             50 |         50 |            42 |         84% |                 1/2 |
| `is_vpn_detected` | 🟢 100.0% |             50 |         50 |             2 |          4% |                 1/2 |

This makes it easier to identify:

* Highly complete variables
* Potential identifiers
* Low-cardinality attributes
* Variables shared between datasets
* Dataset-specific fields
* Potential join keys
* Data-quality inconsistencies

---

# 🧠 How It Works

The analysis pipeline can be summarized as:

```text
┌──────────────────────┐
│   Upload Datasets    │
│  CSV / XLS / XLSX    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Data Extraction    │
│       Pandas         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Variable Detection   │
│ & Key Identification │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Metric Calculation   │
│ Fill / Cardinality   │
│ Similarity / Count   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Interactive Analysis │
│       Dashboard      │
└──────────────────────┘
```

---

# 🛠️ Technology Stack

| Technology    | Purpose                                   |
| ------------- | ----------------------------------------- |
| **Python**    | Application and analytical logic          |
| **Streamlit** | Web interface and interactive dashboard   |
| **Pandas**    | Dataset processing and metric calculation |
| **OpenPyXL**  | Excel `.xlsx` file support                |

---

# 🚀 Getting Started

## Prerequisites

Make sure you have **Python 3.9 or later** installed.

You can verify your Python version with:

```bash
python --version
```

---

## 📥 Installation

### 1. Clone the repository

```bash
git clone https://github.com/thiagosilvaventura/App-Scrap-.git
```

### 2. Navigate to the project directory

```bash
cd App-Scrap-
```

### 3. Install the required dependencies

```bash
pip install streamlit pandas openpyxl
```

### 4. Run the application

```bash
streamlit run app.py
```

Streamlit will start the local server and make the application available at:

```text
http://localhost:8501
```

---

# 📁 Project Structure

```text
App-Scrap-/
│
├── app.py
│   └── Main Streamlit application and UI configuration
│
├── analyzer_core.py
│   └── Core analytical logic and metric calculations
│
├── analyzerpy.py
│   └── Data extraction and primary-key analysis
│
├── images/
│   ├── upload-interface.png
│   ├── cross-dataset-analysis.png
│   └── dynamic-ranking.png
│
└── README.md
    └── Project documentation
```

---

# 🔐 Data Privacy

Analyzer Pro Max is designed around **local dataset analysis**.

Uploaded datasets are processed within the application's Streamlit session rather than being intentionally sent to an external data-processing service.

This makes the application particularly useful when working with datasets that should remain within the user's local analytical environment.

> **Note:** Actual privacy and data-retention behavior ultimately depends on how and where the Streamlit application is deployed.

---

# 🎯 Use Cases

Analyzer Pro Max can be useful for:

* Data quality assessment
* Dataset exploration
* Data profiling
* Variable discovery
* Dataset reconciliation
* ETL preparation
* Join-key identification
* Risk-data analysis
* Fraud-data exploration
* Feature discovery for machine-learning projects
* Cross-system data validation


---

# 🤝 Contributing

Contributions, issues, suggestions, and feature requests are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes.
4. Commit your changes.
5. Open a Pull Request.

---

# 📄 License

This project is provided for educational, analytical, and development purposes, no real user data was used.



## ⭐ Support the Project

If Analyzer Pro Max is useful to you, consider giving the repository a ⭐ on GitHub.

> **Turn raw tables into relationships, relationships into signals, and signals into decisions.**
>
> *Because sometimes the most interesting story in a dataset is the column nobody bothered to compare.*
