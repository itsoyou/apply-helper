# Apply Helper

Apply Helper is an AI-powered application that assists users in analyzing resumes and job descriptions. Built with Flask and OpenAI's Assistant API, it provides an interactive interface where users can: 
- Upload their resume (PDF format) and Job description
- Ask questions about their resume or job descriptions
- Get sample cover letter and interview questions
- Get AI-powered insights and suggestions

## Credit

Thanks to Women Tech Makers for the Generative AI course. This is a project is inspired from https://github.com/WTMBerlin/generative-ai-course.git

## Features

- 📄 PDF Resume Upload
- 💬 Interactive Q&A Interface
- 🤖 AI-Powered Analysis
- 💌 Cover Letter Examples
- 👩‍💼 Expected Interview Questions
- 📝 Markdown-Formatted Outputs

### Technical Stack

- Backend: Python/Flask
- Frontend: HTML, CSS, JavaScript
- AI: OpenAI Assistant API
- Document Processing: PDF parsing
- UI: Responsive design with markdown support

## Requirements

- Python 3.8+
- Flask
- OpenAI API Key

## Installation

1. Clone the repository

```
git clone https://github.com/itsoyou/apply-helper.git
```

2. Create and activate virtual environment

```
python -m venv .venv
source .venv/bin/activate # On Windows: .venv\Scripts\activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

## Required Environment Variables

Create a `.env` file in the root directory with the following variables:

- `OPENAI_API_KEY`: Your OpenAI API key

## Running the Application

1. Set up the environment variables. Create a `.flaskenv` file in the root directory with the following variables:

- `FLASK_APP`: apply_helper/app.py
- `FLASK_DEBUG`: Set to 1 for development mode

2. Install the package in development mode

```
pip install -e .
```

3. Run the Flask application

```
flask run
```

The application will be available at `http://127.0.0.1:5000`


## Project Structure

```
apply-helper/
├── apply_helper/
│ ├── init.py
│ ├── app.py
│ ├── assistant.py
│ ├── config.py
│ ├── routes.py
│ └── templates/
│   └── index.html
├── uploads/
├── .env
├── .flaskenv
├── requirements.txt
└── setup.py
```

## Usage

1. Open the application in your web browser
2. Upload your resume (PDF format)
3. Type your question in the text area
4. Click "Help me" to get AI-powered responses
5. View the formatted response in the chat-like interface
