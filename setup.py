from setuptools import setup, find_packages

setup(
    name="teddi_rag_system",
    version="0.1.0",
    description="TeDDie RAG Core System (Document Loader, Embedder, FAISS Search)",
    author="Hwang SoonGyu",
    packages=find_packages(include=["rag", "rag.*", "crawler", "crawler.*"]),
    python_requires=">=3.10",
    install_requires=[
        "faiss-cpu",
        "sentence-transformers",
        "numpy",
    ],
)