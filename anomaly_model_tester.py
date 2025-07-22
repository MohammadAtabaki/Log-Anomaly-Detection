import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import IsolationForest

# ✅ Load trained model
def load_model(path="output/isolation_forest_model.joblib"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Model not found at {path}")
    return joblib.load(path)

# ✅ Create test samples (custom or synthetic)
def generate_test_samples():
    """
    Returns a small set of test cases:
    - Normal: low ratio, common subtask
    - Anomalies: high ratio, 100% Unnamed Task
    """
    samples = [
            # Normal example
            {'total_time_sec': 1.5, 'max_subtask_percent': 99, 'sum_other_subtask_time': 0.01, 'ratio_other_to_max': 0.006},
            # Anomaly - high other time
            {'total_time_sec': 1.2, 'max_subtask_percent': 60, 'sum_other_subtask_time': 1.1, 'ratio_other_to_max': 1.833},
            # Normal - max_subtask_percent is 100 with Unnamed
            {'total_time_sec': 2.0, 'max_subtask_percent': 100, 'sum_other_subtask_time': 0.0, 'ratio_other_to_max': 0.0},
            # Normal case
            {'total_time_sec': 0.5, 'max_subtask_percent': 95, 'sum_other_subtask_time': 0.03, 'ratio_other_to_max': 0.01},
            # Edge case - high ratio but short total
            {'total_time_sec': 0.2, 'max_subtask_percent': 80, 'sum_other_subtask_time': 0.1, 'ratio_other_to_max': 0.5}
        ]
    
    return pd.DataFrame(samples)

# ✅ Run prediction
def test_model_on_samples(model, test_df):
    """
    Test the trained Isolation Forest model on new data and return the results.
    """
    # List of features used during training
    feature_columns = ['total_time_sec', 'max_subtask_percent', 'sum_other_subtask_time', 'ratio_other_to_max']
    
    # Ensure the columns in the test data match those used during training
    missing_columns = [col for col in feature_columns if col not in test_df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns in test data: {missing_columns}")

    # Select only the features for prediction, ensuring the correct order
    X_test = test_df[feature_columns]

    # Make predictions
    predictions = model.predict(X_test)
    scores = model.decision_function(X_test)

    # Add predictions and scores to the dataframe
    test_df['prediction'] = predictions
    test_df['anomaly_score'] = scores

    return test_df


