import pytest
import sys, os

from crawler.CrawlWoowacourseRagDataset import fetch_java_repos, fetch_readme

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_fetch_java_repos_returns_list():
    repos = fetch_java_repos()
    assert isinstance(repos, list)

def test_repo_name_starts_with_java_prefix():
    repos = fetch_java_repos()
    assert all(repo["name"].startswith("java-") for repo in repos)

def test_fetch_readme_returns_string():
    content = fetch_readme("java-lotto-6")
    assert isinstance(content, str)
    assert "과제 진행" in content or "기능 요구" in content