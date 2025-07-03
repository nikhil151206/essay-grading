# Automatic Essay Grading Using BERT and Cosine Similarity

This project is an **Automatic Essay Grading System** that leverages BERT embeddings and cosine similarity to evaluate student essays against a set of key points and a customizable rubric. It features both a Flask API backend and a user-friendly Streamlit web interface.

## Features
- Grade essays automatically using state-of-the-art NLP (BERT)
- Compare essays to key points and rubric criteria
- Customizable rubric and key points
- Instant feedback and scoring
- Streamlit web app for easy interaction

## Tech Stack
- Python 3.12+
- [HuggingFace Transformers](https://huggingface.co/transformers/)
- Flask (backend API)
- Streamlit (frontend UI)
- scikit-learn, numpy, pandas

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/nikhil151206/essay-grading.git
cd essay-grading
```

### 2. Install dependencies
It is recommended to use a virtual environment (e.g., `venv` or `conda`).

```bash
pip install -r requirements.txt
```

**Note:** If you encounter issues with NumPy 2.x, downgrade to NumPy 1.x:
```bash
pip install 'numpy<2'
```

### 3. Run the Streamlit App
```bash
streamlit run streamlit_app.py
```
Visit [http://localhost:8501](http://localhost:8501) in your browser.

### 4. (Optional) Run the Flask Backend
```bash
python main.py
```

## Usage
- Enter your essay, key points (one per line), and rubric in the Streamlit app.
- Click the "Grade Essay" button to get instant feedback and scores.

## Example Key Points Format
```
Importance of time management
Balancing studies, hobbies, and responsibilities
Effects of poor time management (stress, late submissions)
Benefits of planning and following a schedule
Discipline and organization from routines
Making a daily to-do list
Time management helps in future success
```

## License
This project is for educational purposes.

---

For questions or contributions, feel free to open an issue or pull request! 