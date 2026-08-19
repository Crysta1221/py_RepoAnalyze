import os
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from dotenv import load_dotenv
from github import Auth, Github

# 次のいずれか:
#   spring-projects/spring-framework
#   opensearch-project/OpenSearch
#   apache/lucene
REPO = "apache/lucene"

load_dotenv()
token = os.environ["GITHUB_API_TOKEN"]
g = Github(auth=Auth.Token(token))
repo = g.get_repo(REPO)

# 今日を含む直近7日分の日付を用意する
today = datetime.now().date()
days = []
counts = {}
for i in range(7):
    day = today - timedelta(days=6 - i)
    days.append(day)
    counts[day] = 0

start = datetime(days[0].year, days[0].month, days[0].day)

# GitHub の Issues API は Pull Request も含むので、Issue だけ数える
issues = repo.get_issues(state="all", sort="created", direction="desc")
for issue in issues:
    created = issue.created_at.replace(tzinfo=None)
    if created < start:
        break
    if issue.pull_request is not None:
        continue
    counts[created.date()] += 1

print(REPO)
for day in days:
    print(day, counts[day])

labels = []
values = []
for day in days:
    labels.append(str(day))
    values.append(counts[day])

plt.bar(labels, values)
plt.title(REPO + " : Issue reports (last 7 days)")
plt.xlabel("Date")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("issue-counts.png")
plt.show()
