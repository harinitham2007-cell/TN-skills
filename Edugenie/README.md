# EduGenie - Gemini 3.8 Flash

EduGenie is an AI-powered educational learning assistant built using:

- Python
- FastAPI
- HTML
- CSS
- JavaScript
- Google Gemini 3.8 Flash

## Features

- Ask educational questions
- Explain topics
- Summarize text
- Generate quizzes
- Personalized learning recommendations

## Project Structure

EduGenie/

├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── gemini_service.py
│   ├── local_explainer.py
│   └── services.py

├── templates/
│   └── index.html

├── static/
│   ├── style.css
│   └── app.js

├── tests/
│   └── test_api.py

├── scripts/
│   └── test_api.ps1

├── .vscode/
│   └── settings.json

├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

## Installation

Open the EduGenie folder in VS Code.

Open the terminal.

Create the virtual environment:

```powershell
python -m venv .venv