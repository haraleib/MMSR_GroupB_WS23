import pandas as pd
import pickle


def read_tsv(file: str) -> pd.DataFrame:
    return pd.read_csv(file, sep="\t")


def pickle_file(path: str, data):
    with open(path, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def unpickle_file(path: str):
    try:
        with open(path, 'rb') as handle:
            return pickle.load(handle)
    except FileNotFoundError:
        return None


# only executes the compute_function if the file does not exist, otherwise unpickles the file
def unpickle_or_compute(path: str, compute_function):
    path = f"pickled_state/{path}"

    data = unpickle_file(path)
    if data is None:
        print(f"  --> No pickled data file found. Performing on-the-fly data computation and saving to '{path}' for "
              f"later (re-)use.")

        data = compute_function()
        pickle_file(path, data)
    else:
        print(f"  --> Loading pickled data from {path}")

    return data
