# Google Scholar to BibTeX Converter API

A Flask API that converts Google Scholar publications to BibTeX format using SerpAPI.

## Features
- Convert Google Scholar profile to BibTeX format
- RESTful API endpoints
- Docker support
- Health check endpoint

## Prerequisites
- Docker (for containerized deployment)
- SerpAPI key (get one at https://serpapi.com/)

## Quick Start

### Using Docker

1. Clone the repository:
```bash
git clone https://github.com/jshinodea/scholar_to_bibtex
cd scholar_to_bibtex
```

2. Create a `.env` file:
```bash
SERPAPI_KEY=your_api_key_here
```

3. Build and run the Docker container:
```bash
docker build -t scholar_to_bibtex .
docker run -p 5000:5000 --env-file .env scholar_to_bibtex
```
4. Get a .bib file from the API:
```bash
curl -X POST http://localhost:5000/convert -H "Content-Type: application/json" -d "{\"scholar_url\": \"PUT URL HERE\"}" --output citations.bib
``` 

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

## API Endpoints

### Convert Scholar Profile to BibTeX
```
POST /convert
Content-Type: application/json

{
    "scholar_url": "https://scholar.google.com/citations?user=AUTHOR_ID"
}
```

### Health Check
```
GET /health
```

## Development

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)