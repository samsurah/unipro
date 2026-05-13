import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from datetime import datetime

class SegmentationService:
    @staticmethod
    def calculate_rfm(df: pd.DataFrame):
        # Expected columns: CustomerID, TransactionDate, TransactionAmount
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        reference_date = df['TransactionDate'].max() + pd.Timedelta(days=1)
        
        rfm = df.groupby('CustomerID').agg({
            'TransactionDate': lambda x: (reference_date - x.max()).days,
            'CustomerID': 'count',
            'TransactionAmount': 'sum'
        }).rename(columns={
            'TransactionDate': 'Recency',
            'CustomerID': 'Frequency',
            'TransactionAmount': 'Monetary'
        })
        return rfm

    @staticmethod
    def cluster_customers(rfm: pd.DataFrame, n_clusters=3):
        # Log transformation to handle skewness
        rfm_log = np.log1p(rfm)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        rfm['Cluster'] = kmeans.fit_predict(rfm_log)
        
        # Map clusters to meaningful names
        # We'll calculate the mean RFM for each cluster to identify them
        cluster_means = rfm.groupby('Cluster').mean()
        
        # Logic to identify segments:
        # High Frequency/High Monetary -> Loyalists
        # High Recency (Low Recency value) but Low F/M -> New/Window Shoppers
        # Low Recency (High Recency value) -> Lapsed
        
        # Sort clusters by Frequency + Monetary (desc) to find Loyalists
        rank = (cluster_means['Frequency'] + cluster_means['Monetary']).sort_values(ascending=False)
        loyalists_cluster = rank.index[0]
        lapsed_cluster = cluster_means['Recency'].idxmax()
        
        # The remaining one is Window Shoppers
        all_clusters = set(range(n_clusters))
        window_shoppers_cluster = list(all_clusters - {loyalists_cluster, lapsed_cluster})[0] if len(all_clusters) > 2 else list(all_clusters - {loyalists_cluster})[0]

        mapping = {
            loyalists_cluster: 'High-value loyalists',
            lapsed_cluster: 'Lapsed customers',
            window_shoppers_cluster: 'Window shoppers'
        }
        
        rfm['Segment'] = rfm['Cluster'].map(mapping)
        return rfm

    @staticmethod
    def generate_sample_data(n=100):
        np.random.seed(42)
        customer_ids = np.arange(1, n + 1)
        data = []
        for cid in customer_ids:
            # Different profiles
            profile = np.random.choice(['loyal', 'window', 'lapsed'], p=[0.2, 0.5, 0.3])
            
            if profile == 'loyal':
                num_tx = np.random.randint(10, 50)
                recency_range = (1, 30)
            elif profile == 'window':
                num_tx = np.random.randint(1, 5)
                recency_range = (1, 60)
            else: # lapsed
                num_tx = np.random.randint(1, 3)
                recency_range = (180, 365)
            
            for _ in range(num_tx):
                days_ago = np.random.randint(*recency_range)
                date = (datetime.now() - pd.Timedelta(days=days_ago)).strftime('%Y-%m-%d')
                amount = np.random.uniform(10, 500)
                data.append([cid, date, amount])
                
        return pd.DataFrame(data, columns=['CustomerID', 'TransactionDate', 'TransactionAmount'])

