# Evidence

Fill this file with real outputs from your machine before submission.

## Environment

- OS:
- Python:
- Docker:
- Ollama:
- Vision model:
- Embedding model:

## Acceptance probe 1 — schema-valid vision output

Command:
```text
...
```

Result:
```text
...
```

## Acceptance probe 2 — semantic ranking

Input post:
```text
...
```

Top results:
```text
...
```

## Acceptance probe 3 — mismatch guard

Expected:
`fox`

Candidate:
`gray wolf`

Result:
```text
REJECTED — Animal category mismatch: expected fox, detected wolf
```

## Acceptance probe 4 — no confident match

Result:
```text
NO_CONFIDENT_MATCH — ...
```

## Acceptance probe 5 — evaluation

Command:
```text
python scripts/evaluate.py --input data/eval/eval_results.json
```

Result:
```text
Top-1 precision: ...
```

## Acceptance probe 6 — cost tracking

Show a sample query/output proving every vision and embedding call is logged.

## Dataset/license evidence

For every external image source, record:
- filename
- source URL
- license/permission
- date collected

Do not commit secrets, API keys, or credentials.
