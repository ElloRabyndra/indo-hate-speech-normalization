# Indonesian Hate Speech Normalization

## Overview

This project implements **Lexical Normalization** on Indonesian Twitter texts to improve hate speech classification accuracy. The implementation includes a complete natural language processing (NLP) pipeline specifically designed for handling informal Indonesian language commonly found in social media.

## Project Description

Hate speech detection in Indonesian social media is challenging due to the prevalence of informal language, abbreviations, and non-standard word forms. This project addresses these challenges by implementing a comprehensive preprocessing and normalization pipeline before applying machine learning classification.

### Key Objective

To develop and evaluate a lexical normalization approach that transforms informal Indonesian text into standardized forms, thereby improving the performance of hate speech classification models.

## Pipeline Architecture

The project follows a structured 6-stage NLP pipeline:

```
1. Pre-processing
   ├── Sentence Segmentation
   ├── Tokenization
   ├── Text Cleaning
   └── Lowercase Conversion

2. Lexical Normalization
   ├── Non-standard Word Normalization
   └── Abbreviation Expansion

3. Stopword Removal
   └── Indonesian-specific stopwords

4. Stemming
   └── Indonesian morphological analysis

5. Text Representation
   └── TF-IDF Vectorization

6. Classification
   └── Naive Bayes Model
```

## Technologies & Libraries

- **Python 3.x** - Programming language
- **NLTK** - Natural Language Toolkit for tokenization and text processing
- **Sastrawi** - Indonesian NLP library for stemming and stopword removal
- **Scikit-learn** - Machine learning framework for TF-IDF vectorization and Naive Bayes
- **Pandas & NumPy** - Data manipulation and numerical computing
- **Matplotlib & Seaborn** - Data visualization

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/ElloRabyndra/indo-hate-speech-normalization.git
cd indo-hate-speech-normalization
```

2. Install required packages:

```bash
pip install nltk Sastrawi scikit-learn matplotlib seaborn pandas numpy
```

3. The main notebook will automatically download necessary NLTK data (punkt, punkt_tab) during execution.

## Usage

The project is structured as a Jupyter Notebook (`main.ipynb`) that can be run interactively:

1. Open the notebook in Jupyter:

```bash
jupyter notebook main.ipynb
```

2. Execute cells sequentially following the pipeline stages
3. Review output visualizations and classification metrics
4. Analyze model performance on your dataset

## Project Structure

```
indo-hate-speech-normalization/
├── main.ipynb                 # Main implementation notebook
├── README.md                  # Project documentation
├── data/                      # Dataset directory
├── model/                     # Trained model artifacts
├── images/                    # Visualization outputs
└── web/                       # Web interface
```

## References & Resources

### Indonesian NLP Resources

- Sastrawi Documentation
- NLTK Documentation
- Scikit-learn Documentation

### Hate Speech Detection

- Research papers on hate speech classification
- Twitter sentiment analysis techniques
- Indonesian language processing challenges

---
