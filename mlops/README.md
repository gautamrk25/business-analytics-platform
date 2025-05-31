# ML Governance Platform (Aegis)

A comprehensive platform for managing ML model lifecycle on Google Cloud's Vertex AI, emphasizing governance, reproducibility, and best practices.

## Features

- Model Registration and Documentation
- Model Validation and Testing
- Bias and Fairness Checks
- Explainability Integration
- Data Validation
- Approval Workflows

## Prerequisites

- Python 3.9+
- Google Cloud Platform account with Vertex AI enabled
- Google Cloud credentials configured

## Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd phoenix-mlops
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the development server:
```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## Development

- Frontend: HTMX + Tailwind CSS
- Backend: FastAPI
- Cloud Integration: Google Cloud Vertex AI

## Testing

Run tests with:
```bash
pytest
```

## License

[License Type] - See LICENSE file for details
