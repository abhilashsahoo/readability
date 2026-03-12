# Readability

A simple REST API that analyzes text or web page content and returns readability scores using multiple standard metrics.

**Author:** Abhilash Sahoo  
**License:** MIT

---

## Features

- **Text or URL input** — Send plain text or a URL; the API fetches and extracts paragraph content from the page.
- **Multiple readability metrics** — Flesch Reading Ease, SMOG Index, Flesch–Kincaid Grade Level, Coleman–Liau Index, Automated Readability Index, Dale–Chall, Linsear Write, Gunning Fog.
- **Normalized score** — An average normalized readability score (0–100) for easy comparison.
- **Extra stats** — Reading time, sentence count, character/letter counts, difficult word count, and text standard.

---

## Requirements

- Python 3.8+
- Dependencies in `requirements.txt`

---

## Installation

```bash
git clone https://github.com/yourusername/readability.git
cd readability
pip install -r requirements.txt
```

---

## Usage

### Run locally

```bash
python app.py
```

Server runs at `http://0.0.0.0:8080`.

### API

**Endpoint:** `POST /readability`

**Request body (JSON):**

- **By text:**
  ```json
  { "text": "Your paragraph or article text here." }
  ```
- **By URL:**
  ```json
  { "url": "https://example.com/article" }
  ```

**Example (curl):**

```bash
curl -X POST http://localhost:8080/readability \
  -H "Content-Type: application/json" \
  -d '{"text": "The quick brown fox jumps over the lazy dog."}'
```

**Example response (excerpt):**

```json
{
  "flesch_reading_ease": 94.3,
  "smog_index": 2.1,
  "average_normalized_readability": 85.2,
  "reading_time": 0.2,
  "sentence_count": 1,
  "text_standard": "5th and 6th grade"
}
```

---

## Deployment (Google App Engine)

The project includes `app.yaml` for Google App Engine. Deploy with:

```bash
gcloud app deploy
```

---

## License

This project is open source under the [MIT License](LICENSE).  
Copyright (c) Abhilash Sahoo.
