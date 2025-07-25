# 🔍 Log Analysis Project

This project performs structured analysis on JSON-based SQL Server logs to extract meaningful patterns, performance metrics, anomalies, and clusters using Python.

---

## 📁 Project Structure

### `log_analysis_project/`

- `data/` – Raw JSON log files  
- `output/` – Auto-generated analysis outputs (CSV, plots)  
- `load_and_parse.py` – Module for loading and flattening JSON logs  
- `preprocess.py` – Cleans and prepares logs for analysis  
- `global_stats.py` – **Task 1**: Field count and hierarchy analysis  
- `stopwatch.py` – **Task 2**: Stopwatch execution time analysis  
- `large_array_check.py` – **Task 3**: Oversized JSON array detection  
- `eda.py` – Extra visualizations and insights  
- `task2_anomaly_features.py` – Extract meaningful features for anomaly detection and feature engineering based on the result of task 2  
- `feature_engineering.py` – Embeds categorical features (e.g., stopwatch names) and applies dimensionality reduction for clustering and anomaly detection  
- `dbscan_clustering.py` – Performs DBSCAN clustering on engineered features to identify groups and outliers in the log data  
- `anomaly_detection.py` – Train the Isolation Forest model for detecting anomalies based on the extracted features  
- `anomaly_detection_vs_dbscan.py` – Compares anomalies detected by DBSCAN clustering and Isolation Forest, providing a summary of overlap and unique detections  
- `anomaly_model_tester.py` – Test the trained model based on the generated data  
- `main.py` – Pipeline runner script  
- `requirements.txt` – Python dependency list  
- `.gitignore` – Files/folders to exclude from version control  

---

## 🚀 How to Run

1. **Clone the repository**:

    ```bash
    git clone https://gitlab.internal.omniaplace.net/internship/data-analysis/log-analysis-project.git
    cd log-analysis_project
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Prepare input files**:
    - Place your `.json` log files into the `data/` directory.

4. **Run the analysis pipeline**:

    ```bash
    python main.py
    ```

---

## 📌 Tasks & Functionality

### ✅ Task 1: Field Occurrence Analysis

- Extracts and counts values of the following fields:
  - `CommandID`
  - `EventID`
  - `FieldID`
  - `FileTypeID`
- Two analysis modes:
  - **Flat**: Ignores where the field appears in the JSON structure.
  - **Hierarchy-Aware**: Counts based on exact JSON paths.
- Output:
  - `output/task1_flat_counts.csv`
  - `output/task1_hierarchy_counts.csv`
  - Multiple visual bar plots for ranked field combinations.

### ✅ Task 2: Stopwatch Execution Breakdown

- Detects all `StopWatch` entries with trace ID.
- Extracts:
  - Stopwatch name
  - Subtask breakdown
  - Execution time and percentage
- Visualizes:
  - Histogram of total execution time
  - Top 15 subtasks by percentage
- Output:
  - `output/task2_stopwatch_details.csv`

### ✅ Task 3: Oversized Array Detection

- Scans embedded JSON in messages labeled:
- Flags and reports array-type fields with length > 500.
- Output:
- `output/task3_oversized_arrays.csv`

---

## 📊 Exploratory Data Analysis (EDA)

- Summarizes structure and value distribution of columns.
- Charts:
- Logs per day and per hour
- Frequency of log levels
- Most common logger classes
- Keyword extraction from messages (using `CountVectorizer`)

---

## 🧩 Feature Engineering & Clustering

### `feature_engineering.py`
- **Purpose:** Transforms raw stopwatch features and categorical columns (like `stopwatch_name`) into numerical vectors using sentence embeddings and PCA for dimensionality reduction.
- **Objective:** Prepares data for clustering and anomaly detection by standardizing features and reducing complexity.

### `dbscan_clustering.py`
- **Purpose:** Applies DBSCAN clustering to the engineered features to discover natural groupings and outliers in the log data.
- **Objective:** Identifies clusters of similar log events and flags anomalies as points not belonging to any cluster (`cluster = -1`).
- **Result & Outcome:**  
  - The number of clusters and the count of data points in each cluster are reported.
  - Outliers (anomalies) are highlighted for further analysis.
  - Visualizations are saved in `output/figures/` showing cluster assignments in both feature and PCA-reduced spaces.

---

## 🚨 Anomaly Detection & Comparison

### `anomaly_detection.py`
- **Model:** Isolation Forest (unsupervised)
- **Objective:** Detect anomalies based on stopwatch execution breakdowns (e.g., subtasks taking disproportionate time, anomalous task patterns)
- **Features Used:**
  - `total_time_sec`
  - `max_subtask_percent`
  - `sum_other_subtask_time`
  - `ratio_other_to_max`
- **Outputs:**
  - `output/anomaly_results.csv`: All logs with anomaly scores and predictions.
  - `output/anomalies_detected.csv`: Only the detected anomalies.

### `anomaly_detection_vs_dbscan.py`
- **Purpose:** Compares anomalies detected by DBSCAN clustering and Isolation Forest.
- **Objective:**  
  - Shows overlap and unique detections between both methods.
  - Provides a preview of the number of anomalies detected by each method and both.
- **Result & Outcome:**  
  - Prints the count of anomalies detected only by DBSCAN, only by Isolation Forest, and by both.
  - Saves a comparison CSV and a bar plot visualizing the results in `output/figures/dbscan_vs_isolation_forest_comparison_plot.png`.
  - Example: If DBSCAN detects 19 anomalies and Isolation Forest detects 18, the comparison will show how many are unique to each and how many overlap.

---

## 📦 Output Files

Saved under the `output/` directory:
- CSV results from each task
- Plots for visual insights (PNG or displayed inline)
- Model files (`.joblib`, `.pkl`)
- Cluster and anomaly comparison results

---

## 🛠 Dependencies

Major Python libraries:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `joblib`
- `sentence-transformers`

Install all dependencies using:

```bash
pip install -r requirements.txt
```


