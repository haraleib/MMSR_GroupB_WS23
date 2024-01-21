import pandas as pd
from typing import Literal


class LateFusion:
    def __init__(
            self,
            df1: pd.DataFrame,
            df2: pd.DataFrame,
            df1_weight: float,
            df2_weight: float,
            method: Literal["score", "rank"]
    ):
        self.df1 = df1
        self.df2 = df2

        self.d1_weight = df1_weight
        self.d2_weight = df2_weight

        self.method = method
        self.df = self._late_fusion()

    def _late_fusion(self) -> pd.DataFrame:
        # Rename the "similarity" column
        df_1 = self.df1.rename(columns={"similarity": "similarity_d1"})
        df_2 = self.df2.rename(columns={"similarity": "similarity_d2"})

        # Merge DataFrames
        merged_df = pd.merge(df_1, df_2, how="outer")
        merged_df.fillna(0.0, inplace=True)

        # Assuming the scores are already normalized between 0 and 1
        normalized_d1_scores = merged_df["similarity_d1"].values
        normalized_d2_scores = merged_df["similarity_d2"].values

        if self.method == "score":
            # Aggregate scores
            aggregated_scores = self.d1_weight * normalized_d1_scores + self.d2_weight * normalized_d2_scores

            # Add the aggregated scores to the DataFrame
            merged_df["aggregated_score"] = aggregated_scores

            # Sort DataFrame based on aggregated scores
            return merged_df.sort_values(by="aggregated_score", ascending=False)
        elif self.method == "rank":
            # Convert similarity scores to ranks using pandas Series
            d1_ranks = pd.Series(normalized_d1_scores).rank(ascending=False)
            d2_ranks = pd.Series(normalized_d2_scores).rank(ascending=False)

            # Rank-level fusion: Combine the ranks using weighted sum
            aggregated_ranks = self.d1_weight * d1_ranks + self.d2_weight * d2_ranks

            # Add the aggregated ranks to the DataFrame
            merged_df["aggregated_rank"] = aggregated_ranks

            # Sort DataFrame based on aggregated ranks
            return merged_df.sort_values(by="aggregated_rank")
        else:
            raise ValueError("Invalid fusion method. Use 'score' or 'rank'.")
