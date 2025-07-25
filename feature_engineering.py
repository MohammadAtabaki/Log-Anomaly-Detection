import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer
import os

def load_data(file_path="output/task2_stopwatch_features.csv"):
    """
    Load the stopwatch features dataset for further analysis and preprocessing.
    """
    df = pd.read_csv(file_path)
    print(f"✅ Loaded data from {file_path}, shape: {df.shape}")
    return df


def preprocess_data(df):
    """
    Preprocess the data: normalize numeric features, apply sentence transformer to `stopwatch_name`, 
    and create any additional features.
    """
    # ✅ Step 1: Normalize numeric features
    feature_columns = ['total_time_sec', 'max_subtask_percent', 'sum_other_subtask_time', 'ratio_other_to_max']
    X = df[feature_columns]
    additional_columns = ['trace_id', 'stopwatch_name']  # Keep these for later use
    # Standardizing the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    df_normalized = pd.DataFrame(X_scaled, columns=feature_columns)
    df_normalized[additional_columns] = df[additional_columns]



    # ✅ Step 2: Embed `stopwatch_name` using Sentence Transformers
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Use pre-trained model from SentenceTransformers
    embeddings = model.encode(df['stopwatch_name'].tolist())  # Convert `stopwatch_name` into embeddings

    # Add the embeddings to the dataframe as new features
    embedding_columns = [f'embed_{i}' for i in range(embeddings.shape[1])]
    embedding_df = pd.DataFrame(embeddings, columns=embedding_columns)
    

    pca = PCA(n_components=50)
    df_with_pca = pca.fit_transform(embedding_df)

    
    # Convert the PCA output to a DataFrame
    df_with_pca = pd.DataFrame(df_with_pca, columns=[f'PCA_{i+1}' for i in range(df_with_pca.shape[1])])

    

    # Concatenate original data with embeddings
    df_preprocessed = pd.concat([df_normalized, df_with_pca], axis=1)


    print(f"✅ Preprocessed data shape: {df_preprocessed.shape}")
    return df_preprocessed

def save_preprocessed_data(df, output_path="output/preprocessed_clustering_features.csv"):
    """
    Save the preprocessed features to a CSV file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Preprocessed data saved to {output_path}")


def process():
    """
    Load, preprocess, and save the features.
    """
    # Load data
    df = load_data()

    # Preprocess data
    df_preprocessed = preprocess_data(df)

    # Save the processed data
    save_preprocessed_data(df_preprocessed)



