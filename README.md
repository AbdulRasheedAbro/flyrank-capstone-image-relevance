# FlyRank Capstone — AI Image Understanding & Content Matching Engine

## What this project does

This backend analyzes an image library, stores structured visual metadata and embeddings, semantically matches images to blog posts, and applies a mismatch guard before recommending an image.

It is designed around the capstone acceptance probes:
- schema-valid vision output
- low-confidence flagging
- retryable background processing
- AI cost attribution
- semantic ranking
- mismatch rejection with a human-readable reason
- explicit "No confident match" behavior
- persistence and indexes
- review/approve/reject API
- evaluation script for Top-1 precision

## Architecture

```text
Image files
    |
    v
Background batch job
    |
    +--> Vision model (Ollama/LLaVA)
    |       |
    |       +--> schema validation
    |       +--> confidence flag
    |
    +--> embedding model (Ollama/all-MiniLM)
    |
    v
PostgreSQL
    |
Blog post --> embedding --> cosine ranking --> mismatch guard
                                             |
                              +--------------+--------------+
                              |                             |
                           accepted                 rejected / no match
                              |                             |
                         suggestion                   reason + review API
```

## Requirements

- Python 3.11+
- Docker Desktop
- Ollama model container (provided by compose)
- A set of licensed images from Unsplash/Pexels or another permitted source

## Quick start

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
docker compose up -d
python -m app.db.init_db
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs`.

Pull the local models:

```bash
docker exec -it flyrank-ollama ollama pull llava
docker exec -it flyrank-ollama ollama pull all-minilm
```

For deterministic unit tests without AI/network calls:

```bash
set MOCK_AI=true
pytest -q
```

## API workflow

1. `POST /images` for each image path.
2. `POST /posts` for each blog post.
3. `POST /jobs/process-images` to run vision + embedding batch processing.
4. Poll `GET /jobs/{job_id}`.
5. `GET /posts/{post_id}/images` to rank and guard candidates.
6. Inspect `GET /suggestions/{suggestion_id}/why`.
7. Review with `/approve` or `/reject`.

## Dataset

The repository intentionally does not redistribute third-party images. Add only images you are permitted to use to `data/images/`.

The capstone asks for a realistic corpus of 40+ images across 4+ categories and an evaluation set of 10+ labeled posts. Keep a manifest such as:

```text
data/images/
  animals/
  vehicles/
  food/
  places/
```

Record source/license information in `EVIDENCE.md`.

## Evaluation

Create `data/eval/eval_results.json` using the example format and run:

```bash
python scripts/evaluate.py --input data/eval/eval_results.json
```

The reported Top-1 precision should be copied into the README and EVIDENCE.md after the real dataset run.

## Acceptance test checklist

- [ ] Batch processing creates schema-valid vision metadata.
- [ ] At least one deliberately ambiguous/low-confidence image is flagged.
- [ ] Fox article ranks fox above wolf/dog in the real evaluation set.
- [ ] Forced wolf-for-fox case is rejected with an animal mismatch explanation.
- [ ] No suitable image returns `NO_CONFIDENT_MATCH`.
- [ ] Evaluation script reports Top-1 precision.
- [ ] Cost logs contain every vision/embedding operation.
- [ ] 40+ permitted images across 4+ categories are included locally.
- [ ] 10+ labeled evaluation posts are included.
- [ ] README and EVIDENCE contain actual run results, not placeholders.
- [ ] Public GitHub repository contains no secrets.

## Scope note

The capstone requirements call for real image data and real evaluation evidence. This repository supplies the complete backend implementation and test harness, but the final submission must use the student's own permitted dataset and record the actual model/evaluation outputs.
