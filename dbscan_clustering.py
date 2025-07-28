import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os
import numpy as np
import joblib


def run_dbscan_clustering(csv_file="output/preprocessed_clustering_features.csv", eps=0.5, min_samples=5):
    """
    Perform DBSCAN clustering on the preprocessed feature data.
    """
    # ✅ Step 1: Load preprocessed feature data
    df = pd.read_csv(csv_file)
    print(f"✅ Loaded data from {csv_file}, shape: {df.shape}")

    # ✅ Step 2: Load the stopwatch features to add `trace_id` and `stopwatch_name`


    # ✅ Step 3: Select features for clustering
    feature_columns = [col for col in df.columns if col.startswith('embed_')]  # Using embedding columns
    feature_columns += ['total_time_sec', 'max_subtask_percent', 'sum_other_subtask_time', 'ratio_other_to_max']  # Original features
    X = df[feature_columns]
    detail_columns = ['trace_id', 'stopwatch_name']  # Keep these for later use

    # ✅ Step 4: Hyperparameter tuning using GridSearch (search for best eps and min_samples)
    param_grid = {'eps': [0.2,0.3,0.4, 0.5,0.6, 0.7,0.8], 'min_samples': [1, 3, 5, 7, 10, 12, 15]}
    best_score = -1
    best_params = {'eps': eps, 'min_samples': min_samples}
    
    for eps_val in param_grid['eps']:
        for min_samples_val in param_grid['min_samples']:
            dbscan = DBSCAN(eps=eps_val, min_samples=min_samples_val)
            labels = dbscan.fit_predict(X)
            
            # Evaluate clustering performance using Silhouette Score (for DBSCAN, values range from -1 to 1)
            if len(set(labels)) > 1:  # Ensure at least two clusters were formed
                score = silhouette_score(X, labels)
                if score > best_score:
                    best_score = score
                    best_params = {'eps': eps_val, 'min_samples': min_samples_val}

    print(f"Best hyperparameters: eps={best_params['eps']}, min_samples={best_params['min_samples']}")
    
    # ✅ Step 5: Apply DBSCAN with the best parameters
    dbscan = DBSCAN(eps=best_params['eps'], min_samples=best_params['min_samples'])
    df['cluster'] = dbscan.fit_predict(X)  # Cluster the data

    # ✅ Step 6: Merge the DBSCAN results with the original `stopwatch_features` to add trace_id, stopwatch_name, and other relevant columns

    

    # ✅ Step 7: Save clustering results to CSV
    os.makedirs("output", exist_ok=True)
    df.to_csv("output/dbscan_clustering_results.csv", index=False)
    print(f"✅ Clustering results saved to output/dbscan_clustering_results.csv")

    # ✅ Step 8: Save the DBSCAN model 
    os.makedirs("output", exist_ok=True)
    dbscan_info = {'eps': best_params['eps'], 'min_samples': best_params['min_samples'], 'labels': dbscan.labels_}
    joblib.dump(dbscan_info, "output/dbscan_model.joblib")
    print(f"✅ DBSCAN model saved to output/dbscan_model.joblib")

    if 'ground_truth_label' in df.columns:
        ari = adjusted_rand_score(df['ground_truth_label'], df['cluster'])
        print(f"Adjusted Rand Index (ARI): {ari}")
    else:
        print(f"Silhouette Score for DBSCAN: {best_score}")
    

    return df
def plot_dbscan_clusters(df):
        

    # ✅ Step 9: Visualize the clusters (2D visualization)
    plt.figure(figsize=(10, 6))
    plt.scatter(df['total_time_sec'], df['max_subtask_percent'], c=df['cluster'], cmap='viridis')
    plt.title('DBSCAN Clustering of Logs Based on Execution Features')
    plt.xlabel('Total Time (sec)')
    plt.ylabel('Max Subtask Percent')
    plt.colorbar(label='Cluster')
    plt.tight_layout()


    # ✅ Step 10: Show the final number of clusters
    # After running DBSCAN and assigning the 'cluster' label to the dataframe
    # Step 1: Find unique cluster labels
    unique_clusters = df['cluster'].unique()


    # Step 2: Count the number of unique clusters
    num_clusters = len(unique_clusters)

    print(f"✅ Final number of clusters: {num_clusters}")
    print(f"Unique clusters found: {unique_clusters}")

    # Step 3: Show the number of data points in each cluster
    cluster_counts = df['cluster'].value_counts()
    print("Number of data points in each cluster:")
    print(cluster_counts)

    # Save the plot
    os.makedirs("output/figures", exist_ok=True)
    plt.savefig("output/figures/dbscan_clustering_plot_with_pca.png")
    print(f"🖼️ Clustering plot saved to output/figures/dbscan_clustering_plot_with_pca.png")

    # Show the plot
    plt.show()

    



