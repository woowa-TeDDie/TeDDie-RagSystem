# TeDDie-RagSystem

이 프로젝트는 우아한테크코스 프리코스 과제들의 `README.md` 파일을 기반으로 한 RAG(Retrieval-Augmented Generation) 시스템입니다. GitHub API를 사용하여 특정 조직의 리포지토리에서 `README.md` 파일을 크롤링하고, 이 데이터를 기반으로 FAISS 인덱스를 구축하여 유사도 검색을 수행합니다.

## ✨ 주요 기능

### 📖 크롤러 (`crawler/CrawlWoowacourseRagDataset.py`)
- 특정 GitHub 조직(`woowacourse-precourse`)에 속한 리포지토리 중 `java-`로 시작하는 모든 리포지토리를 가져옵니다.
- 각 리포지토리의 `README.md` 파일 내용을 크롤링합니다.
- 크롤링한 데이터를 `jsonl` 형식의 파일(`woowacourse_rag_dataset.jsonl`)로 저장합니다.

### 🤖 RAG 시스템 (`rag/`)
RAG 시스템은 데이터를 로드하고, 임베딩하며, 검색하는 역할을 하는 여러 모듈로 구성되어 있습니다. `WoowacourseRAG` 클래스가 이 모든 과정을 관리하는 인터페이스 역할을 합니다.

#### 1. 문서 로더 (`rag/Loader.py`)
- **역할**: `woowacourse_rag_dataset.jsonl` 파일에서 데이터를 로드합니다.
- **주요 기능**:
    - `load()`: JSONL 파일을 읽어 각 줄을 파싱하고, 문서 객체의 리스트를 반환합니다.

#### 2. 임베더 (`rag/Embedder.py`)
- **역할**: 텍스트 데이터를 수치형 벡터(임베딩)로 변환합니다.
- **주요 기능**:
    - `SentenceTransformer` 모델(`paraphrase-multilingual-MiniLM-L12-v2`)을 사용하여 임베딩을 생성합니다.
    - `encode()`: 여러 텍스트를 한 번에 임베딩합니다.
    - `encode_single()`: 단일 텍스트를 임베딩합니다.

#### 3. 검색 엔진 (`rag/SearchEngine.py`)
- **역할**: FAISS를 사용하여 구축된 벡터 인덱스를 관리하고, 유사도 검색을 수행합니다.
- **주요 기능**:
    - `build()`: 문서 임베딩을 사용하여 FAISS 인덱스(`IndexFlatL2`)를 구축합니다.
    - `search()`: 주어진 쿼리를 임베딩하고, 인덱스에서 가장 유사한 `top_k`개의 문서를 찾습니다.
    - `save()`: 구축된 인덱스를 파일로 저장합니다.
    - `load()`: 파일에서 인덱스를 로드합니다.

## ✅ 기능 체크리스트

### 크롤러 (`CrawlWoowacourseRagDataset.py`)
- [x] `fetch_java_repos()`: `woowacourse-precourse` 조직의 `java-` 시작 리포지토리 목록 가져오기
- [x] `fetch_readme()`: 리포지토리 이름으로 `README.md` 파일 내용 가져오기
- [x] `save_jsonl()`: 크롤링된 데이터를 `jsonl` 파일로 저장

### RAG 시스템 (`rag/`)
- **`DocumentLoader`**
    - [x] `__init__()`: JSONL 파일 경로 설정
    - [x] `load()`: 파일 시스템에서 문서를 로드하고 리스트로 반환
- **`Embedder`**
    - [x] `__init__()`: `SentenceTransformer` 모델 로드
    - [x] `encode()`: 텍스트 목록을 임베딩 벡터로 변환
    - [x] `encode_single()`: 단일 텍스트를 임베딩 벡터로 변환
- **`FaissSearchEngine`**
    - [x] `__init__()`: 임베더와 문서를 받아 초기화
    - [x] `build()`: 문서로부터 FAISS 인덱스 구축
    - [x] `search()`: 쿼리에 대한 유사 문서 검색
    - [x] `save()`: 인덱스를 파일에 저장
    - [x] `load()`: 파일로부터 인덱스 로드
- **`WoowacourseRAG` (Facade)**
    - [x] `__init__()`: 로더, 임베더, 검색 엔진 컴포넌트 초기화
    - [x] `build_index()`: 전체 인덱싱 파이프라인 실행
    - [x] `search()`: 검색 기능 제공
    - [x] `save_index()` / `load_index()`: 인덱스 저장/로드 기능 제공

## ⚙️ 설치

프로젝트를 실행하기 위해 필요한 라이브러리는 `requirements.txt` 파일에 명시되어 있습니다. 다음 명령어를 사용하여 설치할 수 있습니다.

```bash
pip install -r requirements.txt
```

## 🚀 사용법

### 1. 데이터 크롤링

RAG 시스템을 사용하기 전에 먼저 데이터를 크롤링해야 합니다. 다음 스크립트를 실행하세요.

```bash
python -m crawler.CrawlWoowacourseRagDataset
```

스크립트가 성공적으로 실행되면 프로젝트 루트 디렉토리에 `woowacourse_rag_dataset.jsonl` 파일이 생성됩니다.

### 2. RAG 시스템 사용

`WoowacourseRAG` 클래스는 내부의 복잡한 과정을 추상화하여 간단한 인터페이스를 제공합니다.

```python
from rag.RagSearch import WoowacourseRAG

# 1. RAG 시스템 초기화
rag = WoowacourseRAG()

# 2. 인덱스 구축 (시간이 다소 소요될 수 있습니다)
# 이전에 인덱스를 구축하고 저장한 경우, 이 단계를 건너뛸 수 있습니다.
print("인덱스를 구축합니다...")
rag.build_index()
print("인덱스 구축 완료!")

# 3. 구축된 인덱스 저장
rag.save_index("faiss_index.bin")
print("인덱스가 'faiss_index.bin' 파일로 저장되었습니다.")

# 4. (선택) 저장된 인덱스 로드
# 새로운 세션에서 인덱스를 다시 구축하지 않고 사용하려면 아래와 같이 로드합니다.
# rag.load_index("faiss_index.bin")
# print("저장된 인덱스를 로드했습니다.")

# 5. 검색 수행
query = "숫자 야구 게임의 규칙을 알려주세요."
results = rag.search(query, top_k=3)

# 6. 검색 결과 출력
print(f"\n'{query}'에 대한 검색 결과:")
for result in results:
    print(f"- 리포지토리: {result['repo']} (유사도: {result['similarity_score']:.4f})")
    print(f"  URL: {result['url']}")
    # print(f"  내용: {result['text'][:100]}...") # 전체 내용을 보려면 주석 해제
```