from github import Auth, Github


def create_github(token):
    return Github(auth=Auth.Token(token))
