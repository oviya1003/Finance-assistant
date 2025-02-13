# Personal Finance Assitant

![WhatsApp Image 2025-02-13 at 22 01 11](https://github.com/user-attachments/assets/178d21c1-06fe-42c7-a2ae-112cc15c2005)

## Project Overview

This project is an AI-powered financial advisor that helps users make informed investment decisions based on their financial data and risk tolerance. It includes a Streamlit web app, a fine-tuned T5 model for Q&A, and investment suggestion algorithms.

------------



## Features

- **Streamlit Web App (app.py)**:
    - Collects user income, expenditure, and savings data.
    - Provides risk-based investment recommendations.
    - Displays financial charts (income vs. expenditure vs. savings).
    - Fetches real-time stock data from Alpha Vantage.
    - Includes an FAQ section with financial guidance.

- **Fine-Tuned T5 Model (fine_tune_t5.py):**
    - Uses a T5 model trained on a financial Q&A dataset.
    - Provides investment and financial advice based on user queries.
    - Investment Advisor Logic (investment_advisor.py):
    - Loads financial datasets.
    - Processes user financial data and risk tolerance.
    - Generates investment growth predictions.

- **Model Testing & Deployment:**
    - `trail.py:` Loads and tests the T5 question-answering model.
    - `Untitled-1.py:` Loads the fine-tuned model for generating responses.
      
![WhatsApp Image 2025-02-13 at 22 01 13](https://github.com/user-attachments/assets/813863db-8f14-4a9a-b1e7-bfb67d11fdb6)

	

------------



## Installation

1. Clone the repository:

```bash
git clone <repo_link>
cd project_directory
```

2 . Install dependencies:
`pip install streamlit pandas plotly transformers datasets requests alpha_vantage`

3 . Set up API keys (for Alpha Vantage stock data retrieval).

------------



## Usage

 - Run the Streamlit App:

`streamlit run app.py`

- Fine-tune the T5 model:

`python fine_tune_t5.py`

- Test the model:

`python trail.py`

------------



## Data Requirements

- Ensure datasets (e.g., `FINAL_DATASET.xlsx and FINQ&A.csv)` are in the correct path.
- The app dynamically loads financial data and risk-based returns.

------------



## Future Enhancements

- Expand dataset with more financial insights.
- Improve model responses with more training data.
- Integrate additional APIs for real-time financial data analysis.
