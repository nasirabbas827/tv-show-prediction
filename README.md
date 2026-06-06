# tv_show_prediction_final  

A Django‑based web application that predicts TV‑show outcomes (e.g., episode ratings, winner forecasts) using machine‑learning models. The project also demonstrates a simple blockchain implementation to ensure the integrity of user votes and comments.

---  

## Overview  

`tv_show_prediction_final` combines data science and web development to provide:

* **Predictive analytics** – Train and serve models that forecast TV‑show metrics.  
* **Interactive UI** – Django admin and custom views for managing shows, candidates, and votes.  
* **Data integrity** – A lightweight blockchain stored in the database guarantees that votes cannot be tampered with.  

The repository contains the full Django project (`myapp`) together with migration history, forms, and utility code. The accompanying `Project File.docx` outlines the methodology, data sources, and evaluation results.

---  

## Features  

| Feature | Description |
|---------|-------------|
| **Model training & inference** | Scripts (inside `myapp`) load historic show data, train a scikit‑learn model, and expose a `/predict/` endpoint. |
| **User voting** | Authenticated users can cast votes on episode predictions. Votes are written to a simple blockchain (`blockchain.py`). |
| **Comment sentiment analysis** | Comments are stored with an automatically generated sentiment label (positive/negative/neutral). |
| **Admin dashboard** | Full CRUD for Shows, Candidates, Profiles, and Blockchain entries via Django admin. |
| **REST‑style API** | JSON endpoints for predictions, votes, and comment retrieval. |
| **Database migrations** | 16 migration files track schema evolution from the initial model to the latest `profile_age` field. |
| **Documentation** | High‑level project description and results are in `Project File.docx`. |

---  

## Tech Stack  

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.9, Django 4.x |
| **Machine Learning** | scikit‑learn, pandas, NumPy |
| **Blockchain (toy)** | Custom Python implementation (`myapp/blockchain.py`) |
| **Database** | SQLite (default) – can be swapped for PostgreSQL |
| **Frontend** | Django templates + Bootstrap 5 (optional) |
| **Testing** | Django test framework, pytest (optional) |
| **Version Control** | Git (GitHub) |

---  

## Installation  

1. **Clone the repository**  

   ```bash
   git clone https://github.com/your-username/tv_show_prediction_final.git
   cd tv_show_prediction_final
   ```

2. **Create and activate a virtual environment**  

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**  

   The project uses a `requirements.txt` file (create it if missing) that should contain at least:

   ```text
   Django>=4.0
   pandas
   numpy
   scikit-learn
   ```

   Install with:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**