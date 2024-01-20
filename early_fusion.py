#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.decomposition import PCA

class EarlyFusionLibrary:
    def __init__(self):
        pass

    def early_fusion_and_save(self, df1, df2, output_filename='datasets/id_early_fusion_mmsr.tsv'):
        df1_pca = pd.DataFrame(PCA(n_components=0.8).fit_transform(df1.iloc[:, 1:]))
        df1_pca["id"] = df1["id"]

        df2_pca = pd.DataFrame(PCA(n_components=0.8).fit_transform(df2.iloc[:, 1:]))
        df2_pca["id"] = df2["id"]

        fused_df = pd.concat([df1_pca.set_index('id'), df2_pca.set_index('id')], axis=1).reset_index()

        # Save the result to a TSV file
        fused_df.to_csv(output_filename, sep='\t', index=False)

