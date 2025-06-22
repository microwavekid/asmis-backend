# ASMIS Backend

Backend service for the ASMIS (Agentic Sales Meeting Intelligence System) application, built with FastAPI.

## Features

- RESTful API endpoints
- File upload handling for transcripts (.txt, .docx, .pdf)
- Health check endpoint
- Secure file storage with timestamp-based naming

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/microwavekid/asmis-backend.git
cd asmis-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

## API Endpoints

### Health Check
- `GET /health`
- Returns service health status

### File Upload
- `POST /upload-transcript`
- Accepts file uploads (.txt, .docx, .pdf)
- Files are saved to the `uploads` directory with timestamp prefixes
- Returns success/error messages in JSON format

## Development

The application uses FastAPI for the backend service. Key files:
- `app/main.py`: Main application file with route definitions
- `requirements.txt`: Python dependencies

## License

[Your chosen license] test
test2
