import pandas as pd
from joblib import load
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

def get_cluster_labels(data):
    # Load the KMeans Clustering algorithm
    kmeans = load('KMeans_NodeClustering.joblib')
    
    df = pd.DataFrame(data)

    # One-hot encode the 'Type' column
    #type_dummies = pd.get_dummies(df['Type'], prefix='Type')

    # Drop the original 'Type' column and concatenate the one-hot encoded columns
    df_encoded = pd.concat([df.drop('Node', axis=1)], axis=1)

    # Convert DataFrame to numpy array
    X = df_encoded.values

    # Standardize the data to have a mean of ~0 and a variance of 1
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Determine the cluster labels of each point
    labels = kmeans.predict(X_scaled)

    # Add the cluster labels as a column to the original DataFrame
    df_encoded['Cluster'] = labels

    return df_encoded['Cluster'].values

# Example usage:
# Assuming df is your DataFrame
data = [
#     {'Node': 'VEC-Master', 'RAM (GB)': 4, 'Storage (GB)': 20, 'CPU (Cores)': 2,'Type_Cache':0,'Type_Compute': 1,'Type_Storage':0,'Security Score (0-10)': 8},
    {'Node': 'VEC_VEN1', 'RAM (GB)': 0.5, 'Storage (GB)': 8, 'CPU (Cores)': 1,'Type_Cache':0,'Type_Compute': 1,'Type_Storage':1, 'Security Score (0-10)': 8},
    {'Node': 'VEC_VEN2', 'RAM (GB)': 1, 'Storage (GB)': 12, 'CPU (Cores)': 1,'Type_Cache':0,'Type_Compute': 1,'Type_Storage':0, 'Security Score (0-10)': 8},
    {'Node': 'VEC_VEN3', 'RAM (GB)': 2, 'Storage (GB)': 16, 'CPU (Cores)': 1,'Type_Cache':0,'Type_Compute': 1,'Type_Storage':1, 'Security Score (0-10)': 8},
    {'Node': 'VEC_VEN4', 'RAM (GB)': 4, 'Storage (GB)': 12, 'CPU (Cores)': 2,'Type_Cache':0,'Type_Compute': 1,'Type_Storage':0, 'Security Score (0-10)': 8},
    {'Node': 'VEC_VEN5', 'RAM (GB)': 4, 'Storage (GB)': 30, 'CPU (Cores)': 2,'Type_Cache':0,'Type_Compute': 1,'Type_Storage':0, 'Security Score (0-10)': 8}
]

result_cluster = get_cluster_labels(data)
print(result_cluster)
