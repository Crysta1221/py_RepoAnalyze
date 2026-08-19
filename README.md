# Pull Request Merge Prediction

Predict whether a closed GitHub pull request was merged (`1`) or rejected (`0`).

## Files

| File | Description |
| --- | --- |
| `data/dataset.csv` | Full labeled table. Every closed PR, including `Merged` and `CreatedAt`. |
| `data/train.csv` | Training set (older 80% by `CreatedAt`). Includes `Merged`. |
| `data/test.csv` | Test set (newer 20%). Does **not** include `Merged`. Predict this column. |

## Data dictionary

| Variable | Definition | Key |
| --- | --- | --- |
| `Id` | Pull request number | Unique row id. Do not use as a feature. |
| `Merged` | Whether the pull request was merged | `0` = rejected, `1` = merged |
| `CreatedAt` | When the pull request was opened (UTC) | Only in `dataset.csv`. Used for the train/test split. |
| `TitleLength` | Character length of the PR title |  |
| `BodyLength` | Character length of the PR description | `0` if empty |
| `Additions` | Lines added |  |
| `Deletions` | Lines deleted |  |
| `ChangedFiles` | Number of files changed |  |
| `Commits` | Number of commits on the PR |  |
| `Draft` | Whether the PR was a draft | `0` = no, `1` = yes |
| `Labels` | Number of labels on the PR |  |
| `IsBot` | Whether the author is a bot | `0` = no, `1` = yes |
| `IssueComments` | Conversation comments on the PR |  |
| `ReviewComments` | Inline review comments on the diff |  |
| `CreatedHour` | Hour of day the PR was opened | `0`–`23` (UTC) |
| `CreatedDay` | Weekday the PR was opened | `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, `sunday` |

Missing numeric values are left blank. Binary fields are `0` / `1`.

## How to Use
1. create `.env` file with `GITHUB_API_TOKEN`(For example, you can see `.env.example`)
2. Set variables for `repoanalyze/gen_dataset.py`(Set `REPO`) and run it.
3. Generated `test.csv` and `test.csv` are saved in `data/`.
4. Run `main.ipynb`.

This repository uses `uv`, so you have to run `uv sync` first.