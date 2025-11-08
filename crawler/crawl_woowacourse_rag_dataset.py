import requests

def fetch_java_repos():
    url = "https://api.github.com/orgs/woowacourse-precourse/repos?per_page=100"
    res = requests.get(url)
    repos = res.json()
    return [r for r in repos if r["name"].startswith("java-")]
