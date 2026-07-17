# IIT Roorkee Summer Training — Machine Learning & Agentic AI

This repository contains all coursework, assignments, and projects completed during the **Summer Training Programme on Machine Learning & Agentic AI**, organized by the **Electronics & ICT Academy (E&ICT), IIT Roorkee**.

It spans classical machine learning, applied deep learning, and agentic AI systems — covering the full workflow from data preprocessing and model tuning to multi-agent orchestration and neural network design.

## 📂 Repository Structure

```
iitr-summer-training/
├── decision-tree-xgboost/       # Project 1: Decision Tree & XGBoost on Movie Data
│   ├── regression/               # Decision Tree Regressor + GridSearchCV + pruning
│   ├── classification/           # Decision Tree Classifier + GridSearchCV + pruning
│   └── xgboost/                  # XGBRegressor / XGBClassifier benchmarking
├── crewai-retail-analytics/     # Project 2: Multi-Agent Retail Analytics Crew
│   ├── agents/                   # Agent role/goal/tool definitions
│   ├── tasks/                    # Task chaining and orchestration logic
│   └── data/                     # Sample retail sales dataset
├── resume-jd-matching/          # Project 3: Siamese BiLSTM Resume-JD Matcher
│   ├── notebooks/                # Model architecture, training, evaluation
│   └── data/                     # Resume / job description pairs
├── nlp-assignment/              # NLP assignment (internship deliverable)
├── peer-review/                 # Notes from reviewing peer submissions
└── README.md
```

> Folder names above are indicative — see individual directories for exact contents and per-project README/notebook details.

## 🧪 Projects

### 1. Decision Tree & XGBoost on Movie Data
Regression and classification models built on a movie dataset, progressively improved via **GridSearchCV** hyperparameter tuning and **cost-complexity pruning**, then benchmarked against an **XGBoost** ensemble. Demonstrates the overfitting-to-generalization journey from a single unconstrained tree to a tuned/pruned tree to a gradient-boosted ensemble.

**Key techniques:** Decision Trees, GridSearchCV, ccp_alpha pruning, XGBoost, feature importance analysis

### 2. Retail Analytics Crew (CrewAI)
A multi-agent analytics assistant built with **CrewAI**, where a Data Analyst agent computes statistics/trends from retail sales data using a pandas-based tool, and a Reporting agent synthesizes the findings into a business-readable report. Built as an original architecture to explore agent role design, tool grounding, and task chaining.

**Key techniques:** Multi-agent orchestration, tool-grounded LLM agents, sequential task chaining

### 3. Resume–Job Description Matching (Siamese BiLSTM)
A deep learning model that predicts whether a resume matches a job description, using a **Siamese network** with shared-weight **BiLSTM** encoders to embed both texts into a common space. Resolves Keras 3 serialization constraints for shared-layer architectures and addresses class imbalance via class weighting.

**Key techniques:** Siamese networks, BiLSTM, Keras 3, class-weighted training, text similarity classification

## 🛠️ Tech Stack

`Python` · `pandas` · `NumPy` · `scikit-learn` · `XGBoost` · `TensorFlow / Keras 3` · `CrewAI` · `Matplotlib` · `Jupyter Notebook`

## 🚀 Getting Started

```bash
git clone https://github.com/TheRoyBar/iitr-summer-training.git
cd iitr-summer-training
pip install -r requirements.txt   # if present in a given project folder
```

Each project folder can be run independently — open the relevant notebook in Jupyter or run the provided scripts.

## 👤 Author

**Shubham Ghosh Roy**
AI/ML Student — MAKAUT | IIT Guwahati (Online) | Summer Intern, E&ICT Academy, IIT Roorkee
GitHub: [@TheRoyBar](https://github.com/TheRoyBar) · Kaggle: [groyshubham](https://www.kaggle.com/groyshubham)

## 📄 License

This repository is shared for educational and portfolio purposes. Feel free to explore and reference with attribution.
