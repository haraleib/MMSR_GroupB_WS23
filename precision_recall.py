from song import songs
from datasets import datasets
import json
from retrieval import Retrieval, SimilarityMeasure
import matplotlib.pyplot as plt

from utils import unpickle_or_compute

retrievals = {
    "random_baseline": lambda n, query: Retrieval(n=n).random_baseline(query),
    "text_tf_idf": lambda n, query: Retrieval(n=n).text_based_similarity(query, "tf_idf", SimilarityMeasure.COSINE),
    "text_bert": lambda n, query: Retrieval(n=n).text_based_similarity(query, "bert", SimilarityMeasure.COSINE),
    "text_word2vec": lambda n, query: Retrieval(n=n).text_based_similarity(query, "word2vec", SimilarityMeasure.COSINE),
    "mfcc_bow": lambda n, query: Retrieval(n=n).retrieve_top_similar_tracks(query, "mfcc_bow"),
    "blf_correlation": lambda n, query: Retrieval(n=n).retrieve_top_similar_tracks(query, "blf_correlation"),
    "ivec256": lambda n, query: Retrieval(n=n).retrieve_top_similar_tracks(query, "ivec256"),
    "musicnn": lambda n, query: Retrieval(n=n).retrieve_top_similar_tracks(query, "musicnn"),
}

class PrecisionRecall:
    def __init__(self, genres):
        self._genres = genres

    def plot(self):
        # calculate average precision and recall @ k across all tracks for each retrieval method
        # plot precision and recall @ k for each retrieval method
        data = []
        for retrieval_name, retrieval in retrievals.items():
            print(f"Calculating precision and recall for {retrieval_name}")
            precision_at_k, recall_at_k = unpickle_or_compute(f"precision_recall_{retrieval_name}.pickle", lambda: self._calculate_precision_recall(retrieval))
            print(precision_at_k)
            print(recall_at_k)
            data.append((retrieval_name, precision_at_k, recall_at_k))

        self._draw_plot(data)

    def _draw_plot(self, data):
        for (retrieval_name, precision_at_k, recall_at_k) in data:
            x, y = [], []
            for k in range(1, 101):
                x.append(recall_at_k[k])
                y.append(precision_at_k[k])
            plt.plot(x, y, label=retrieval_name)
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.xlim(0, 0.02)
        plt.ylim(0, 1)
        plt.title("Precision-Recall Curve")
        plt.legend() 
        plt.show()


    def _calculate_precision_recall(self, retrieval):
        precision_at_k = {}
        recall_at_k = {}
        i = 0
        for song in self._genres.get_song_ids_with_genre_info():
            retrieved_songs = retrieval(100, song)
            retrieved_songs = list(retrieved_songs["id"])

            nr_relevant_songs = self._genres.get_relevant_song_counts(song)

            relevant_until_k = 0
            for k in range(1, 101):
                if self._genres.song_is_relevant(song, retrieved_songs[k - 1]):
                    relevant_until_k += 1
                
                precision_at_k[k] = precision_at_k.get(k, 0) + relevant_until_k / k
                recall_at_k[k] = recall_at_k.get(k, 0) + relevant_until_k / nr_relevant_songs
            i += 1
            if i % 100 == 0:
                print(f"Processed {i} songs")


        # calculate average precision and recall @ k across all tracks
        for k in range(1, 101):
            precision_at_k[k] /= len(self._genres.get_song_ids_with_genre_info())
            recall_at_k[k] /= len(self._genres.get_song_ids_with_genre_info())
        
        return precision_at_k, recall_at_k
        
