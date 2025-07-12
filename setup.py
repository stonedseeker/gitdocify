from setuptools import setup, find_packages

setup(
    name="gitdocify",
    version="1.0.0",
    description="AI-powered documentation generator for codebases",
    author="Vaibhav Singh Chandel",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "click>=8.0.0",
        "pathspec>=0.11.0",
        "tiktoken>=0.5.0",
        "filelock",
        "fsspec",
        "packaging",
        "pyyaml",
        "Pillow",
        "torch",
        "numpy",
        "pandas>=1.2",
        "python-dateutil>=2.7",
        "joblib>=1.2.0",
    ],
    entry_points={
        "console_scripts": [
            "gitdocify=src.main:generate_docs",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    keywords="documentation, ai, openai, codebase, markdown, generator",
    project_urls={
        "Bug Reports": "https://github.com/stonedseeker/gitdocify/issues",
        "Source": "https://github.com/stonedseeker/gitdocify",
    },
)
