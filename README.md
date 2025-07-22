# 🔍 Log Analysis Project

This project performs structured analysis on JSON-based SQL Server logs to extract meaningful patterns, performance metrics, and anomalies using Python.

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
- `task2_anomaly_features.py` – Extract the meaningful features for anomaly detection and feaure engineering based on the result of task 2  
- `anomaly_detection.py` – Train the Isolation Forest model for the detecting the anomalies based on the extracted feaures  
- `anomaly_model_tester.py` – Test the trained model based on the generated data    
- `main.py` – Pipeline runner script  
- `requirements.txt` – Python dependency list  
- `.gitignore` – Files/folders to exclude from version control  


---

## 🚀 How to Run

1. **Clone the repository**:

    ```bash
    git clone https://gitlab.internal.omniaplace.net/internship/data-analysis/log-analysis-project.git
    cd log-analysis-project
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

## ✅ Anomaly Detection (Isolation Forest)

The project includes **anomaly detection** to identify irregular patterns in the stopwatch execution data:

- **Model**: Isolation Forest (an unsupervised machine learning algorithm)
- **Objective**: Detect anomalies based on stopwatch execution breakdowns (e.g., subtasks taking disproportionate time, anomalous task patterns)
- **Features** used:
  - `total_time_sec`: Total execution time for a stopwatch.
  - `max_subtask_percent`: The percentage of time for the most time-consuming subtask.
  - `sum_other_subtask_time`: Total time for all subtasks except the main one.
  - `ratio_other_to_max`: Ratio of non-main subtask time to the max subtask time.
  
### Steps:
1. **Train Isolation Forest**: Model is trained using the above features and saved as `isolation_forest_model.pkl`.
2. **Detect Anomalies**: For each stopwatch record, the model predicts whether it's an anomaly (`-1`) or normal (`1`).
3. **Outputs**:
   - `output/anomaly_results.csv`: Contains all logs with their anomaly scores and predictions.
   - `output/anomalies_detected.csv`: Contains only the detected anomalies.

### Example of Anomaly Results:

| total_time_sec | max_subtask_percent | sum_other_subtask_time | ratio_other_to_max | prediction | anomaly_score |
|----------------|---------------------|-------------------------|--------------------|------------|----------------|
| 1.5            | 99                  | 0.01                    | 0.006              | 1          | 0.083069       |
| 1.2            | 60                  | 1.10                    | 1.833              | -1         | -0.102871      |

### Visualizations:
- Anomaly score distribution is plotted to visually identify the threshold where anomalies start appearing.
- A scatter plot shows **normal vs. anomalous tasks**, with color coding based on predictions.

---

## 📦 Output Files

Saved under the `output/` directory:
- CSV results from each task
- Plots for visual insights (PNG or displayed inline)

---

## 🛠 Dependencies

Major Python libraries:

- `pandas`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `joblib`

Install all dependencies using:

```bash
pip install -r requirements.txt


