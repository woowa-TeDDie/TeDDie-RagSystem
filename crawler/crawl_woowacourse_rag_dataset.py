import json
import requests
from tqdm import tqdm

ORGANIZATION = "woowacourse-precourse"
OUTPUT = "woowacourse_rag_dataset.jsonl"

def fetch_java_repos():
    url = f"https://api.github.com/orgs/{ORGANIZATION}/repos?per_page=100"
    res = requests.get(url)
    res.raise_for_status()
    repos = res.json()
    return [r["name"] for r in repos if r["name"].startswith("java-")]

def fetch_readme(repo_name: str) -> str | None:
    base = f"https://raw.githubusercontent.com/{ORGANIZATION}"
    urls = [f"{base}/{repo_name}/main/README.md",
            f"{base}/{repo_name}/master/README.md"]

    for url in urls:
        res = requests.get(url)
        if res.status_code == 200:
            return res.text.strip()
    return None

def save_jsonl(records, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

def main():
    repos = fetch_java_repos()
    dataset = []

    for repo in tqdm(repos, desc="README 수집 중"):
        readme = fetch_readme(repo)
        if not readme:
            continue
        dataset.append({
            "repo": repo,
            "text": readme,
            "url": f"https://github.com/{ORGANIZATION}/{repo}"
        })

    save_jsonl(dataset, OUTPUT)
    print(f"\n✅ 총 {len(dataset)}개의 README 파일이 {OUTPUT}에 저장되었습니다.")

if __name__ == "__main__":
    main()
