# Indonesian Hate Speech Detection and Lexical Normalization

## Overview

This project implements a comprehensive system for hate speech classification in Indonesian Twitter text, integrating **Lexical Normalization** to handle non-standard language. The system has been optimized using a **Complement Naive Bayes** algorithm to effectively address class imbalance and improve detection robustness.

## Project Description

Hate speech detection in Indonesian social media is complex due to the prevalence of informal language, abbreviations, and varied slang. This project addresses these challenges by implementing an advanced natural language processing (NLP) pipeline that standardizes irregular text forms before applying machine learning classification.

### Key Objectives

1. Develop a robust lexical normalization pipeline for informal Indonesian text.
2. Implement an optimized classification model using Complement Naive Bayes.
3. Mitigate topic bias through strategic feature filtering to ensure objective hate speech detection.

## Pipeline Architecture

The project follows a structured 6-stage NLP pipeline:

```
1. Pre-processing
   ├── Sentence Segmentation
   ├── Tokenization
   ├── Text Cleaning (URL, Mention, Hashtags removal)
   └── Lowercase Conversion

2. Lexical Normalization
   ├── Slang/Non-standard Word Normalization
   └── Abbreviation Expansion

3. Text Refining
   ├── Stopword Removal (General & Topic-Specific)
   └── Stemming (Sastrawi Morphological Analysis)

4. Text Representation
   ├── Binary TF-IDF Vectorization
   └── N-Gram Extraction (Unigrams and Bigrams)

5. Classification
   ├── Complement Naive Bayes Model
   └── Manual Sample Weighting for toxic keywords

6. Interface
   ├── FastAPI Backend
   └── React/Vite Frontend
```

## Technologies and Libraries

- **Python 3.12+** - Core programming language
- **NLTK** - Tokenization and sentence segmentation
- **Sastrawi** - Indonesian-specific stemming and stopword removal
- **Scikit-learn** - TF-IDF vectorization and Complement Naive Bayes implementation
- **FastAPI** - Backend API for model serving
- **React & Vite** - Modern frontend for the interactive web interface
- **Pandas & NumPy** - Data manipulation and numerical computing

## Installation

### Prerequisites

- Python 3.12 or higher
- Node.js and npm (for the web interface)

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/ElloRabyndra/indo-hate-speech-normalization.git
cd indo-hate-speech-normalization
```

2. Install Python dependencies:
```bash
pip install nltk Sastrawi scikit-learn pandas numpy uvicorn fastapi
```

## Usage

### Research and Analysis
The core research is documented in `main.ipynb`. You can run this notebook to review the data processing, model training, and evaluation metrics:
```bash
jupyter notebook main.ipynb
```

### Web Interface
To run the interactive web application:

1. Start the Backend API:
```bash
cd web
python -m uvicorn api.index:app --port 8000
```

2. Start the Frontend Dev Server:
```bash
cd web
npm install
npm run dev
```
Open your browser at `http://localhost:5173` to test the model in real-time.

## Project Structure

```
indo-hate-speech-normalization/
├── main.ipynb                 # Research and experimental notebook
├── data/                      # Dataset and processed data artifacts
├── files/                     # Project diagrams and confusion matrices
├── web/                       # Full-stack web application
│   ├── api/                   # FastAPI backend and trained models
│   └── src/                   # React frontend source code
└── README.md                  # Project documentation
```

## Evaluation Metrics

The optimized model demonstrates improved objectivity and reliable classification performance:

- **Accuracy**: ~79.38%
- **Precision (HS)**: ~76.51%
- **Recall (HS)**: ~73.83%
- **F1-Score (HS)**: ~75.15%

The metrics reflect the system's performance in identifying genuine hate speech by eliminating spurious correlations related to specific political topics or entities.

---
