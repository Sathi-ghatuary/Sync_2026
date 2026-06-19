# Title Similarity & Compliance Validation Backend

This is the FastAPI backend for the **PRGI Title Verification System**. It provides title verification, compliance checking, and a complete database solution for managing press publication titles across India.

## Features

✅ **Title Verification**: Real-time similarity detection using phonetic algorithms and semantic embeddings
✅ **Compliance Checks**: Enforces rules for disallowed words, prefixes, suffixes, periodicity, and combinations
✅ **Database Management**: ChromaDB-backed storage for 160,000+ titles
✅ **Application Tracking**: Records all title applications with email tracking
✅ **CSV Ingestion**: Bulk import titles from CSV files via API or CLI
✅ **Statistics & Analytics**: Real-time database metrics and application tracking
✅ **Cross-Language Support**: Detects similar meanings across languages
✅ **CORS Enabled**: Ready to connect with React frontend

## Quick Start

### 1. Setup Python Environment

```bash
# Create virtual environment with Python 3.10 or 3.11
py -3.11 -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Or activate (Windows CMD)
.\.venv\Scripts\activate.bat
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Seed Database with Sample Data (Optional)

```bash
python -m app.scripts.seed
```

### 4. Start the Server

```bash
python -m uvicorn app.main:app --reload
```

Server runs at: `http://127.0.0.1:8000` (configurable via `API_URL` environment variable)
API Docs: `http://127.0.0.1:8000/docs` (Swagger UI)

---

## API Endpoints

### Health Check
```
GET /health
```
Returns: `{"status": "ok", "message": "..."}`

### Verify Title
```
POST /verify
Content-Type: application/json

{
  "title": "My New Publication"
}
```
Returns:
```json
{
  "title": "My New Publication",
  "similarity_score": 0.25,
  "verification_probability": 0.75,
  "violations": [],
  "similar_titles": []
}
```

### Submit Application
```
POST /application
Content-Type: application/json

{
  "title": "Morning Herald Daily",
  "user_email": "publisher@example.com"
}
```
Returns application ID and status (approved/rejected)

### Get User Applications
```
GET /applications/{user_email}
```

### Database Statistics
```
GET /database/stats
```
Returns counts of titles, applications, and statuses

### Get Title Count
```
GET /database/titles/count
```

### Ingest CSV File
```
POST /database/ingest/csv
Content-Type: multipart/form-data

[Upload CSV file]
```

CSV Format: One title per row, first column used
Example:
```csv
The Times of India
The Indian Express
The Hindu
Hindustan Times
```

### Bulk Ingest Titles
```
POST /database/ingest/bulk
Content-Type: application/json

{
  "titles": [
    "Title One",
    "Title Two",
    "Title Three"
  ]
}
```

### Reset Database
```
GET /database/reset
```
⚠️ WARNING: Deletes all data

---

## CLI Commands

### Seed Sample Data
```bash
python -m app.scripts.seed
```

### Ingest CSV File from CLI
```bash
python -m app.scripts.ingest_csv path/to/titles.csv [column_index] [delimiter]
```

Examples:
```bash
# Basic usage (uses first column, comma delimiter)
python -m app.scripts.ingest_csv prgi_titles.csv

# Specify column index (0-based)
python -m app.scripts.ingest_csv data.csv 1

# Custom delimiter (tab-separated)
python -m app.scripts.ingest_csv data.tsv 0 $'\t'
```

---

## Database Setup

### Option 1: Using Sample Data (for testing)
```bash
python -m app.scripts.seed
```

### Option 2: Upload Your CSV
1. Start the server
2. Use the `/database/ingest/csv` endpoint to upload your CSV
3. Or use the CLI: `python -m app.scripts.ingest_csv your_titles.csv`

### Option 3: Bulk API Load
```bash
curl -X POST "$BASE_URL/database/ingest/bulk" \
  -H "Content-Type: application/json" \
  -d '{"titles": ["Title 1", "Title 2", "Title 3"]}'
```

---

## Testing the API

### Test with cURL

```bash
# Simple verification
curl -X POST "$BASE_URL/verify" \
  -H "Content-Type: application/json" \
  -d '{"title": "Daily Sandhya"}'

# Application submission
curl -X POST "$BASE_URL/application" \
  -H "Content-Type: application/json" \
  -d '{"title": "Morning Herald", "user_email": "user@example.com"}'

# Get database stats
curl "$BASE_URL/database/stats"

# Upload CSV
curl -X POST "$BASE_URL/database/ingest/csv" \
  -F "file=@titles.csv"
```

### Using Postman/Insomnia
1. Import the endpoints from Swagger UI: `$BASE_URL/docs`
2. All endpoints are documented with examples

### Acceptance Test Suite
```bash
python -m unittest tests.test_acceptance -v
```

### Benchmark (Latency + Concurrency)
```bash
# Warmed benchmark for SLA validation
python -m app.scripts.benchmark --requests 100 --workers 10 --warmup 5 --target-ms 2000
```

---

## Verification Rules

The system enforces the following rules:

1. **Disallowed Words**: police, crime, corruption, cbi, cid, army
2. **Disallowed Prefixes**: the, india, samachar, news
3. **Disallowed Suffixes**: the, india, samachar, news
4. **No Combinations**: Rejects titles combining existing titles
5. **No Periodicity**: Rejects titles adding daily/weekly/monthly/morning/evening to existing titles
6. **Cross-Language**: Detects similar meanings in other languages (e.g., "Pratidin" vs "Daily")

---

## File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app and endpoints
│   ├── config.py              # Configuration settings
│   ├── models.py              # Data models
│   ├── schemas.py             # Pydantic schemas
│   ├── db/
│   │   ├── __init__.py
│   │   ├── chroma_client.py   # ChromaDB client
│   │   ├── manager.py         # Database manager
│   │   └── schema.py          # Database schema
│   ├── services/
│   │   ├── __init__.py
│   │   └── verifier.py        # Title verification logic
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── phonetic.py        # Phonetic matching
│   │   └── text_processing.py # Text utilities
│   └── scripts/
│       ├── __init__.py
│       ├── seed.py            # Database seeding
│       └── ingest_csv.py      # CSV ingestion
├── requirements.txt
├── README.md
└── chroma_db/                 # ChromaDB storage (auto-created)
```

---

## Performance Notes

- **Verification**: < 500ms per title
- **Database**: Handles 160,000+ titles efficiently
- **Batch Ingestion**: 512 titles per batch
- **Response Times**: API responses typically < 2 seconds

---

## Frontend Integration

The backend is CORS-enabled and ready to connect with your React frontend.

```javascript
// Example React request (use import.meta.env.VITE_API_URL in production)
const response = await fetch(`${BASE_URL}/verify`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: 'My Title' })
});
const data = await response.json();
```

---

## Troubleshooting

### ChromaDB Initialization Errors
- Clear `chroma_db/` folder and restart server
- Ensure Python 3.10 or 3.11 (not 3.14)

### Module Not Found Errors
- Verify virtual environment is activated
- Run `pip install -r requirements.txt`

### CSV Upload Fails
- Ensure CSV is UTF-8 encoded
- Titles should be in the first column
- Check file size (large files may timeout)

---

## Configuration

Edit `app/config.py` to customize:
- Disallowed words/prefixes/suffixes
- Embedding model
- ChromaDB settings

---

## License

© 2026 Press Registrar General of India (PRGI)

---

## Support

For issues or feature requests, contact the development team.

