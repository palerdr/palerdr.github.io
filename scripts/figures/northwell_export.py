"""Export the fold assignments behind the Kaggle figure on the Northwell write-up.

The Northwell retrieval work stays at method level (see the header of
src/content/projects/northwell.md), so this script exports nothing from it. The
one data figure on that page comes from the intern Kaggle competition
(Spaceship Titanic, repo https://github.com/palerdr/spaceship-titanic at
b07fdff). The script reruns that repo's two validation splitters on the
competition's train.csv and keeps the fold of each passenger in the first eight
travel groups of two or more passengers, in file order.

Run from the site root. With Kaggle credentials and the competition rules
accepted, the script loads train.csv the way the repo does:

    uv run --with pandas --with 'scikit-learn>=1.9' --with kagglehub \
        python scripts/figures/northwell_export.py

With a local copy of train.csv (805,421 bytes, 8,693 rows x 14 columns):

    uv run --with pandas --with 'scikit-learn>=1.9' \
        python scripts/figures/northwell_export.py --train /path/to/train.csv

Writes scripts/figures/data/northwell/group_folds.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedGroupKFold

OUT = Path(__file__).resolve().parent / "data" / "northwell" / "group_folds.json"

# conf/config.yaml: n_splits: 5, n_repeats: 5, seed: 42.
N_SPLITS = 5
N_REPEATS = 5
SEED = 42
# The figure shows this many groups, the first ones in file order.
N_GROUPS = 8


def load_train(path: str | None) -> tuple[pd.DataFrame, Path]:
    """code/data.py load_competition_data: train.csv from the kagglehub cache."""
    if path is None:
        import kagglehub

        path = str(Path(kagglehub.competition_download("spaceship-titanic")) / "train.csv")
    return pd.read_csv(path), Path(path)


def fold_of_each_row(splitter, y: pd.Series, groups: pd.Series | None, n_rows: int) -> np.ndarray:
    """Fold (1-based) in which each row is the validation row.

    code/experiment.py eval_cv iterates splitter.split(X, y, groups). Both
    splitters here read only y, groups and the row count, so the feature matrix
    does not change the folds. RepeatedStratifiedKFold yields N_SPLITS * N_REPEATS
    splits; the first N_SPLITS form its first repeat, one partition of the rows.
    """
    fold = np.zeros(n_rows, dtype=int)
    for k, (_, val_idx) in enumerate(splitter.split(np.zeros(n_rows), y, groups)):
        if k == N_SPLITS:
            break
        fold[val_idx] = k + 1
    return fold


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", help="path to the competition train.csv")
    args = parser.parse_args()

    train, path = load_train(args.train)
    # eda.ipynb cell 1 prints shape : (8693, 14) for the repo's copy.
    assert train.shape == (8693, 14), train.shape

    # code/features.py build_dataset: y = train[TARGET].astype(int), TARGET = "Transported".
    y = train["Transported"].astype(int)
    # code/features.py build_dataset: groups = PassengerId.str.split("_").str[0] (gggg of gggg_pp).
    groups = train["PassengerId"].str.split("_").str[0]

    # code/experiment.py make_splitter, group_cv: true (the setting the write-up describes).
    grouped = StratifiedGroupKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    # code/experiment.py make_splitter, group_cv: false (the plain split it replaces).
    plain = RepeatedStratifiedKFold(n_splits=N_SPLITS, n_repeats=N_REPEATS, random_state=SEED)

    fold_grouped = fold_of_each_row(grouped, y, groups, len(train))
    fold_plain = fold_of_each_row(plain, y, None, len(train))

    size = groups.map(groups.value_counts())
    shown = groups[size > 1].drop_duplicates().head(N_GROUPS).tolist()
    rows = train.index[groups.isin(shown)]

    passengers = [
        {
            "passenger_id": train.at[i, "PassengerId"],
            "group": groups[i],
            "fold_plain": int(fold_plain[i]),
            "fold_grouped": int(fold_grouped[i]),
        }
        for i in rows
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(
            {
                "source": {
                    "repo": "https://github.com/palerdr/spaceship-titanic",
                    "commit": "b07fdff",
                    "train_csv_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "scikit_learn": sklearn.__version__,
                    "n_splits": N_SPLITS,
                    "seed": SEED,
                },
                "passengers": passengers,
            },
            indent=1,
        )
        + "\n"
    )
    print(f"wrote {OUT} ({len(passengers)} passengers in {len(shown)} groups)")


if __name__ == "__main__":
    main()
