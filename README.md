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

Install all dependencies using:

```bash
pip install -r requirements.txt


