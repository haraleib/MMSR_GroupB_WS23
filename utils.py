import json
import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt


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
    # Create our pickled_state directory on-the-fly if it doesn't exist
    os.makedirs("pickled_state", exist_ok=True)

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


def plot_ret_sys_dict(
        ret_sys_dict: dict[str, float],
        xlabel: str,
        ylabel: str,
        color: str
) -> None:
    # Extract retrieval system names and coverage values
    sorted_dict = {k: v for k, v in sorted(ret_sys_dict.items(), key=lambda tup: tup[1], reverse=True)}

    ret_sys_names = list(sorted_dict.keys())
    coverage_values = list(sorted_dict.values())

    # Create a bar plot
    fig, ax = plt.subplots(figsize=(12, 7), dpi=200)

    # Remove top, right and left borders
    ax.spines["top"].set(visible=False)
    ax.spines["right"].set(visible=False)

    # Add grid lines where the values end (horizontal lines)
    ax.grid(visible=True, color="lightgrey", ls=":")

    # Remove black ticks (we have a grid)
    # ax.tick_params(bottom=False, left=False)

    # Plot
    ax.barh(
        y=ret_sys_names,
        width=coverage_values,
        color=color,
        ec="black",
        lw=0.75,
        zorder=3
    )

    # Add labels and title
    ax.set_xlabel(xlabel, labelpad=8, fontsize=12, color="#111111")
    ax.set_ylabel(ylabel, labelpad=8, fontsize=12, color="#111111")
    ax.set_title(f"{xlabel} by {ylabel}", pad=12, fontsize=13, color="#000000", weight="bold")

    # Display the values on the bars
    for index, x in enumerate(coverage_values):
        ax.annotate(
            xy=(x, index),
            text=f"{x:.3f}".rstrip("0").rstrip("."),
            xytext=(-8, 0),
            textcoords="offset points",
            size=11,
            color="white",
            ha="right",
            va="center",
            weight="bold"
        )

    # Show the plot
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


def df_to_latex_table(df: pd.DataFrame) -> None:
    lines: list[str] = []
    columns = ["song", "artist", "similarity"]

    print("  \\begin{tabular}{llr}")

    # Print table header
    print("    \\toprule")
    # Capitalize columns
    print("    " + " & ".join(["\\textbf{" + c.capitalize() + "}" for c in columns]) + " \\\\")
    print("    \\midrule")

    # Print table body rows
    for index, row in df.iterrows():
        values: list[str] = []
        for col in columns:
            if col in row:
                if col == "similarity":
                    values.append(f"{row[col]:.4f}".rstrip("0").rstrip("."))
                else:
                    values.append(str(row[col]).replace("&", "\\&"))

        lines.append("    " + " & ".join(values))

    print(" \\\\\n".join(lines) + " \\\\")
    print("    \\bottomrule")
    print("  \\end{tabular}")

def write_song_df_to_json_file(path: str, id_information: pd.DataFrame, id_url: pd.DataFrame, id_genres: pd.DataFrame) -> None:
    songs = []
    for index, row in id_information.iterrows():
        ytId = id_url.loc[id_url['id'] == row['id']]['url'].values[0].split('=')[1]
        genres = id_genres.loc[id_genres['id'] == row['id']]['genre'].values[0]
        genres = json.loads(genres.replace("'", "\""))
        songs.append({'id': row['id'], 'artist': row['artist'], 'song': row['song'], 'ytId': ytId, 'genres': genres})
    with open(path, 'w') as outfile:
        json.dump(songs, outfile)
