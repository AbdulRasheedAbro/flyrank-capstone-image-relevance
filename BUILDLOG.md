# BUILDLOG

Keep this log honest and chronological.

## Entry 1 — Architecture and scaffolding
- Designed FastAPI + PostgreSQL + Ollama architecture.
- Added persistent models for images, posts, jobs, suggestions, and cost logs.
- Added schema validation and mismatch guard.

## Entry 2 — AI integration
- Added local Ollama vision and embedding clients.
- Added retries and cost attribution.
- Added deterministic mock mode for tests only.

## Entry 3 — Matching and review
- Added cosine ranking, mismatch guard, no-confident-match path, and review endpoints.

## Entry 4 — Evaluation
- Add your actual dataset size, categories, model versions, precision, and acceptance-probe outputs here.

## AI assistance disclosure
AI assistance was used during development. The final author should verify, understand, test, and be able to explain every submitted component.
