# Administering Information Retrieval Ranking with ML Strategies and Insights

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-6.0.6-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ML Engine](https://img.shields.io/badge/ML-Gensim%20%7C%20Scikit--Learn-orange.svg)](https://scikit-learn.org/)

An advanced **Model-View-Template (MVT)** search portal built with **Python/Django** designed to retrieve and rank unstructured text documents. The system uses a **Natural Language Processing (NLP)** pipeline to clean texts, extracts semantic weights using **Latent Dirichlet Allocation (LDA) Topic Modeling**, and performs accuracy audits using a **Support Vector Machine (SVM)** classifier.

---

## 📖 Table of Contents
- [Executive Summary](#-executive-summary)
- [System Architecture](#-system-architecture)
- [Machine Learning & NLP Pipeline](#-machine-learning--nlp-pipeline)
- [Technology Stack](#-technology-stack)
- [Workflows & Roles](#-workflows--role-based-workflows)
- [Installation & Local Setup](#-installation--local-setup)
- [Directory Structure](#-directory-structure)
- [Future Enhancements](#-future-enhancements)

---

## 💡 Executive Summary

Classic keyword matching search engines retrieve documents by binary matching, leading to search-result clutter or zero-relevance rankings. This project introduces a double-ML approach to document retrieval:
1. **Unsupervised semantic indexing** calculates real-value relevance weightages for each document by parsing word clusters into topic probabilities using LDA.
2. **Supervised performance auditing** trains a linear SVM on the collected database weights to evaluate how accurately the search portal separates relevant and irrelevant documents.

---

## 🏗️ System Architecture

The application implements a 3-tier Django MVT layout:

```
[User / Admin / Vendor Interface] 
               │
               ▼  (HTTP Request)
     [URL Route Dispatcher]
               │
               ▼
       [Django Controller Views] ◄───► [Form Validation Engine]
               │
               ├─► [NLP Preprocessor (NLTK/Inflect)]
               ├─► [Topic Mixture Engine (Gensim LDA)]
               ├─► [Supervised Auditor (Scikit-Learn SVM)]
               │
               ▼  (ORM / Raw SQL Queries)
    [MySQL / SQLite Database] ◄───► [Filesystem Storage (media/files/pdfs/)]
```

---

## 🧠 Machine Learning & NLP Pipeline

### 1. NLP Processing Block
* Converts text to lowercase and strips special characters using regex models.
* Standardizes integer digit sequences to word strings using `inflect` (e.g. `10` to `ten`).
* Tokenizes sentences and removes standard English stopwords.
* Normalizes words to their base dictionary lemma using the **WordNet Lemmatizer**.

### 2. LDA Semantic Weightage (User-Side)
* Processes token lists into document-term bag-of-words corpora.
* Fits an unsupervised **Gensim LdaModel** (`num_topics=4`, `passes=20`).
* Sums the document topic probability distributions to compute a final relevance weight score.

### 3. Support Vector Machine (Admin-Side)
* Queries calculated weightages from the `wgt` database table.
* Splits weights into high-relevance and low-relevance targets using the median weight.
* Splits the dataset into 80/20 train/test configurations and fits a **Linear Support Vector Classifier (SVC)**.
* Evaluates categorizations and outputs classification reports (Precision, Recall, F1-Score) and a Confusion Matrix.

---

## 🛠️ Technology Stack

* **Core Backend**: Python, Django 6.0+
* **Database Layer**: Database-agnostic configuration (seamless fallback to SQLite if local MySQL port `3306` is closed)
* **NLP Suite**: NLTK, Inflect
* **ML Engines**: Gensim, Scikit-Learn
* **Data Diagnostics**: Pandas, NumPy
* **Frontend styling**: Custom modern dark-mode stylesheet (`style.css`) implementing glassmorphic card overlays, glow effects, responsive inputs, and smooth fade-in animations.

---

## 👥 Role-Based Workflows

### 📂 1. Document Vendor
* **Signup & Login**: Register a vendor account and wait for administrator activation.
* **Upload Document**: Upload English plain text files (`.txt`) directly to the system directory.

### 🔍 2. End User
* **Signup & Login**: Create an activated user account.
* **Search portal**: Enter keywords. The portal queries the database index for filename matches and scans file content.
* **Relevance Rank**: Click **Calculate Weightage** on search results to trigger the NLP & LDA pipeline and view the document's relevance weight score.

### 👑 3. System Administrator
* **Secure Login**: Access the console using `admin` / `admin` credentials.
* **User/Vendor Activations**: View logs of pending accounts and activate them with random 8-digit keys.
* **Diagnostic Console**: Audit index files and check SVM classifier precision and confusion matrices.

---

## 💻 Installation & Local Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/danishsyed-dev/Administering-Information-Retrieval-Ranking-with-ML-Strategies-and-Insights.git
cd Administering-Information-Retrieval-Ranking-with-ML-Strategies-and-Insights
```

### Step 2: Configure Virtual Environment & Dependencies
The project uses the `predict_env` environment for dependencies:
```powershell
# Create local virtual env
python -m venv predict_env

# Activate (Windows PowerShell)
.\predict_env\Scripts\Activate.ps1

# Install ML and web packages
pip install django nltk gensim scikit-learn pandas numpy inflect mysql-connector-python
```

### Step 3: Run Database Migrations
Generate database schemas:
```powershell
python manage.py makemigrations user vendor
python manage.py migrate
```

### Step 4: Run Development Server
```powershell
python manage.py runserver
```
Navigate to **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

---

## 📂 Directory Structure

```
├── predict_env/                 # Local virtual environment (ignored in Git)
├── informationretrive/          # Core Django project configuration folder
│   ├── settings.py              # Configuration with MySQL/SQLite fallback check
│   ├── urls.py                  # Main router matching path calls to view actions
│   └── wsgi.py                  # WSGI config
├── information/                 # Admin controllers (approvals, accuracy checker)
├── user/                        # User registration, forms, and weight logic
├── vendor/                      # Vendor registrations, document uploads, and search queries
├── assets/
│   ├── templates/               # Glassmorphic HTML pages (Base, AdminBase, logins, weights)
│   └── static/                  # Static styles (custom style.css)
├── media/                       # Uploaded text document destination directory
├── manage.py                    # Django command-line utility
└── README.md                    # Repository documentation
```

---

## 🔮 Future Enhancements
* **Cryptographic Hashing**: Apply secure PBKDF2/bcrypt password hashing before DB writes (current implementation updates passwords as plain text).
* **True SVM-PSO Optimization**: Implement a Particle Swarm Optimization (PSO) algorithm to dynamically seek and tune SVM hyperparameters ($C$ and $\gamma$).
* **Asynchronous Jobs**: Integrate Redis & Celery to run NLP text cleaning and LDA fittings asynchronously in the background.
* **PDF Parse Integration**: Add a binary reader (`pdfminer` or `PyPDF2`) to accept uploads of true binary PDF documents.
