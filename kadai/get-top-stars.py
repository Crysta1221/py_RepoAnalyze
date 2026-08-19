import os

from dotenv import load_dotenv
from github import Auth, Github

load_dotenv()
token = os.environ["GITHUB_API_TOKEN"]
g = Github(auth=Auth.Token(token))

repos = g.search_repositories(query="stars:>1", sort="stars", order="desc")

rank = 1
for repo in repos:
    print(rank,".", "★", repo.stargazers_count, repo.full_name)
    rank += 1
    if rank > 10:
        break
