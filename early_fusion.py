import pandas as pd
from sklearn.decomposition import PCA
from datasets import LocalDataset


class EarlyFusion:
    def __init__(self, d1: LocalDataset, d2: LocalDataset, n_components: float):
        self.d1 = d1
        self.d2 = d2

        if n_components <= 1.0:
            n_components = int(min(len(d1.df.columns), len(d2.df.columns)) * n_components)

        self.n_components = n_components

        print(f"[Early Fusion] Down-projecting '{d1.name}' and '{d2.name}' with PCA to {n_components} components")
        self.df = self._early_fusion()

    def get_pca_df(self, dataset: LocalDataset) -> pd.DataFrame:
        pca = PCA(n_components=self.n_components)

        features = dataset.df.drop("id", axis=1)
        new_df = pd.DataFrame(
            data=pca.fit_transform(features),
            columns=[f"{dataset.name}_{i+1}" for i in range(self.n_components)]
        )

        # We need to reset the index, otherwise insertion statement won't work
        new_df.index = dataset.df.index
        new_df.insert(0, "id", dataset.df["id"])

        return new_df

    def _early_fusion(self) -> pd.DataFrame:
        pca1 = self.get_pca_df(self.d1)
        pca2 = self.get_pca_df(self.d2)
        return pd.merge(pca1, pca2, on="id")

    # def save(self) -> None:
    #    # Save the result to a TSV file
    #    output_filename = f"early_fusion_{self.d1.name}_{self.d2.name}_{self.n_components}"
    #    self.df.to_csv(output_filename, sep="\t", index=False)
