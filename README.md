# 🔍 Log Anomaly Detection

This project performs structured analysis on JSON-based SQL Server logs to extract meaningful patterns, performance metrics, anomalies, and clusters using Python.

This project is a **modular log anomaly detection pipeline** for analyzing structured and semi-structured system logs. It combines **feature engineering, clustering, and anomaly detection techniques** (such as Isolation Forest and DBSCAN) to identify unusual patterns in event traces.

It was developed during my internship at **eResult** as a proof-of-concept for a **scalable, explainable, and data-driven workflow** in log analysis. The system is designed to be **local-first, transparent, and easily extendable** to new log formats and anomaly detection methods.

---

## 📁 Project Structure

### `log_analysis_project/`

- `data/` – Raw JSON log files  
- `output/` – Auto-generated analysis outputs (CSV, plots)  
- `test_data/` – Place new log files here for testing the trained models  
- `test_result/` – All outputs from the test pipeline are saved here  
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
- `test_pipeline.py` – Script for running the pipeline on new logs using trained models  
- `requirements.txt` – Python dependency list  
- `.gitignore` – Files/folders to exclude from version control  

---

## 🚀 How to Run

1. **Clone the repository**:

    ```bash
    git clone https://github.com/MohammadAtabaki/Log-Anomaly-Detection.git
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

## 🆕 How to Test New Logs

After you have trained your models with `main.py`, you can analyze new logs without retraining:

1. **Place new log files** in the `test_data/` directory.

2. **Run the test pipeline**:

    ```bash
    python test_pipeline.py
    ```

- The script will:
    - Parse and clean the new logs
    - Run all analysis and feature engineering steps
    - Use the trained models (from the `output/` directory) to predict anomalies and clusters
    - Save all results and plots in the `test_result/` directory
    - Print a summary of anomalies detected by each model and their overlap

**You do NOT need to retrain the models for new logs—just use the test pipeline!**

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

## 🚨 Anomaly Detection

### `task2_anomaly_features.py`
- **Purpose:** Preprocesses stopwatch subtask breakdowns to build a feature table for anomaly detection.
- **Preprocessing:** Extracts features such as `total_time_sec`, `max_subtask_percent`, `sum_other_subtask_time`, and `ratio_other_to_max` from the stopwatch details. This step is essential before running the anomaly detection model.

### `anomaly_detection.py`
- **Model:** Isolation Forest (unsupervised)
- **Objective:** Detect anomalies based on the preprocessed stopwatch execution features (from `task2_anomaly_features.py`).
- **Features Used:**
  - `total_time_sec`
  - `max_subtask_percent`
  - `sum_other_subtask_time`
  - `ratio_other_to_max`
- **Outputs:**
  - `output/anomaly_results.csv`: All logs with anomaly scores and predictions.
  - `output/anomalies_detected.csv`: Only the detected anomalies.

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

## 🔄 Anomaly Comparison

### `anomaly_detection_vs_dbscan.py`
- **Purpose:** Compares anomalies detected by DBSCAN clustering and Isolation Forest.
- **Objective:**  
  - Shows overlap and unique detections between both methods.
  - Provides a preview of the number of anomalies detected by each method and both.
- **Result & Outcome:**  
  - Prints the count of anomalies detected only by DBSCAN, only by Isolation Forest, and by both.
  - Saves a comparison CSV and a bar plot visualizing the results in `output/figures/dbscan_vs_isolation_forest_comparison_plot.png`.
  - Example: If DBSCAN detects 19 anomalies and Isolation Forest detects 18, the comparison will show how many are unique to each and
---

## 📦 Output Files

Saved under the `output/` directory:
- CSV results from each task
- Plots for visual insights (PNG or displayed inline)
- Model files (`.joblib`, `.pkl`)
- Cluster and anomaly comparison results

Saved under the `test_result/` directory:
- CSV results from each task
- Plots for visual insights (PNG or displayed inline)
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



