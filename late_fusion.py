#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
from typing import Tuple
from retrieval import Retrieval

def late_fusion_score(df1: pd.DataFrame, df2: pd.DataFrame, d1_weight: float, d2_weight: float) -> pd.DataFrame:

    # Rename the 'similarity' column
    df_1 = df1.rename(columns={'similarity': 'similarity_d1'})
    df_2 = df2.rename(columns={'similarity': 'similarity_d2'})

    # Merge DataFrames on 'id'
    merged_df = pd.merge(df_1[['id', 'similarity_d1']], df_2, on='id')

    # Assuming the scores are already normalized between 0 and 1
    normalized_d1_scores = merged_df['similarity_d1'].values
    normalized_d2_scores = merged_df['similarity_d2'].values

    # Aggregate scores
    aggregated_scores = d1_weight * normalized_d1_scores + d2_weight * normalized_d2_scores

    # Add the aggregated scores to the DataFrame
    merged_df['aggregated_score'] = aggregated_scores

    # Sort DataFrame based on aggregated scores
    sorted_lf_score = merged_df.sort_values(by='aggregated_score', ascending=False)
    return sorted_lf_score

def late_fusion_rank(df1: pd.DataFrame, df2: pd.DataFrame, d1_weight: float, d2_weight: float) -> pd.DataFrame:

    # Rename the 'similarity' column
    df_1 = df1.rename(columns={'similarity': 'similarity_d1'})
    df_2 = df2.rename(columns={'similarity': 'similarity_d2'})

    # Merge DataFrames on 'id'
    merged_df = pd.merge(df_1[['id', 'similarity_d1']], df_2, on='id')

    # Assuming the scores are already normalized between 0 and 1
    normalized_d1_scores = merged_df['similarity_d1'].values
    normalized_d2_scores = merged_df['similarity_d2'].values

    # Convert similarity scores to ranks using pandas Series
    d1_ranks = pd.Series(normalized_d1_scores).rank(ascending=False)
    d2_ranks = pd.Series(normalized_d2_scores).rank(ascending=False)

    # Rank-level fusion: Combine the ranks using weighted sum
    aggregated_ranks = d1_weight * d1_ranks + d2_weight * d2_ranks

    # Add the aggregated ranks to the DataFrame
    merged_df['aggregated_rank'] = aggregated_ranks

    # Sort DataFrame based on aggregated ranks
    sorted_lf_rank = merged_df.sort_values(by='aggregated_rank')
    return sorted_lf_rank

def perform_late_fusion(df1: pd.DataFrame, df2: pd.DataFrame, method: str, d1_weight: float, d2_weight: float) -> pd.DataFrame:

    if method == 'score':
        return late_fusion_score(df1, df2, d1_weight, d2_weight)
    elif method == 'rank':
        return late_fusion_rank(df1, df2, d1_weight, d2_weight)
    else:
        raise ValueError("Invalid fusion method. Use 'score' or 'rank'.")


# In[ ]:





# In[ ]:




