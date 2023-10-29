import pandas as pd


def read_tsv(file):
    return pd.read_csv(file, sep='\t')

def prompt_song_query(id_information):
    song_title = artist_name = None
    while(True):
        # Allow the user to input the song title and artist name
        song_title = input("Enter the song title: ")
        artist_name = input("Enter the artist name: ")

        # Create a query song dictionary
        query_song = {'song': song_title , 'artist': artist_name}

        query_song_mask = (id_information['song'] == query_song['song']) & (id_information['artist'] == query_song['artist'])
        filtered_data = id_information[query_song_mask]
        if len(filtered_data) == 1:
            return query_song
        else:
            print("Query must match 1 song, but matched the following song(s):")
            print(filtered_data)

def text_based_similarity(query_song, N, id_information, id_lyrics_representation, similarity_measure):
    query_song_mask = (id_information['song'] == query_song['song']) & (id_information['artist'] == query_song['artist'])
    song_id = id_information[query_song_mask].iloc[0]["id"] # get the id column of the first row that matches the query

    representation_query = id_lyrics_representation[(id_lyrics_representation['id'] == song_id)]
    representation_query = representation_query.loc[:, representation_query.columns != 'id'] # representation of the query song

    representation_all = id_lyrics_representation.loc[:, id_lyrics_representation.columns != 'id'] # representation of all songs

    similarity = similarity_measure(X=representation_all, Y=representation_query)
    representation_with_similarity = id_lyrics_representation.copy()
    representation_with_similarity.insert(1, "similarity", similarity) # insert the similarity score into the representation df
    representation_with_similarity = representation_with_similarity.sort_values('similarity', ascending=False).iloc[1:(N+1)] # sort by similarity and select top N results (excluding the query, which should be at index 0)
    
    filtered = id_information.loc[id_information['id'].isin(representation_with_similarity['id'])]
    # sort the filtered dataframe by the order of the representation_with_similarity dataframe
    # include the similarity column in the sort so that the filtered dataframe is sorted by similarity
    filtered = filtered.merge(representation_with_similarity, on='id', suffixes=("", "_")).sort_values('similarity', ascending=False)

    return filtered[['id', 'similarity', 'song', 'artist']]

