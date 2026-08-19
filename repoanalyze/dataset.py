import csv
import os
import time

from dotenv import load_dotenv

from client import create_github

WEEKDAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

DATASET_COLUMNS = [
    "Id",
    "Merged",
    "CreatedAt",
    "TitleLength",
    "BodyLength",
    "Additions",
    "Deletions",
    "ChangedFiles",
    "Commits",
    "Draft",
    "Labels",
    "IsBot",
    "IssueComments",
    "ReviewComments",
    "CreatedHour",
    "CreatedDay",
]

TRAIN_COLUMNS = [
    "Id",
    "Merged",
    "TitleLength",
    "BodyLength",
    "Additions",
    "Deletions",
    "ChangedFiles",
    "Commits",
    "Draft",
    "Labels",
    "IsBot",
    "IssueComments",
    "ReviewComments",
    "CreatedHour",
    "CreatedDay",
]

TEST_COLUMNS = [
    "Id",
    "TitleLength",
    "BodyLength",
    "Additions",
    "Deletions",
    "ChangedFiles",
    "Commits",
    "Draft",
    "Labels",
    "IsBot",
    "IssueComments",
    "ReviewComments",
    "CreatedHour",
    "CreatedDay",
]


def write_csv(path, rows, columns):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            out = {}
            for col in columns:
                out[col] = row[col]
            writer.writerow(out)


def wait_if_needed(g):
    remaining = g.get_rate_limit().resources.core.remaining
    if remaining < 50:
        print("rate limit is low. wait 60 seconds")
        time.sleep(60)


def created_at_key(row):
    return row["CreatedAt"]


def create_dataset(repo, size, output_dir=None):
    load_dotenv()
    token = os.environ["GITHUB_API_TOKEN"]
    g = create_github(token)
    repository = g.get_repo(repo)

    if output_dir is None:
        package_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(os.path.dirname(package_dir), "data")

    rows = []
    pulls = repository.get_pulls(state="closed", sort="created", direction="desc")
    for summary in pulls:
        wait_if_needed(g)
        print("fetching PR", summary.number, len(rows) + 1, "/", size)
        pr = repository.get_pull(summary.number)

        title = pr.title
        if title is None:
            title = ""
        body = pr.body
        if body is None:
            body = ""

        is_bot = 0
        if pr.user is not None:
            if pr.user.type == "Bot" or pr.user.login.endswith("[bot]"):
                is_bot = 1

        created = pr.created_at
        row = {
            "Id": pr.number,
            "Merged": int(pr.merged),
            "CreatedAt": created.isoformat(),
            "TitleLength": len(title),
            "BodyLength": len(body),
            "Additions": pr.additions,
            "Deletions": pr.deletions,
            "ChangedFiles": pr.changed_files,
            "Commits": pr.commits,
            "Draft": int(pr.draft),
            "Labels": len(list(pr.labels)),
            "IsBot": is_bot,
            "IssueComments": pr.comments,
            "ReviewComments": pr.review_comments,
            "CreatedHour": created.hour,
            "CreatedDay": WEEKDAYS[created.weekday()],
        }
        rows.append(row)
        if len(rows) >= size:
            break

    rows_sorted = sorted(rows, key=created_at_key)
    split_at = int(size * 0.8)
    train_rows = rows_sorted[:split_at]
    test_rows = rows_sorted[split_at:]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    write_csv(os.path.join(output_dir, "dataset.csv"), rows_sorted, DATASET_COLUMNS)
    write_csv(os.path.join(output_dir, "train.csv"), train_rows, TRAIN_COLUMNS)
    write_csv(os.path.join(output_dir, "test.csv"), test_rows, TEST_COLUMNS)
    print("wrote", len(rows_sorted), "rows to", os.path.abspath(output_dir))
    print("train", len(train_rows), "test", len(test_rows))
