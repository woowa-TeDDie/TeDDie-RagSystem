import pytest
import sys, os

from crawler.crawl_woowacourse_rag_dataset import fetch_java_repos

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_fetch_java_repos_returns_list():
    repos = fetch_java_repos()
    assert isinstance(repos, list)

def test_repo_name_starts_with_java_prefix():
    repos = fetch_java_repos()
    assert all(repo["name"].startswith("java-") for repo in repos)
