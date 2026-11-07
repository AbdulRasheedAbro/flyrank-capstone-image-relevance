# Final Submission Checklist

Before submitting to FlyRank:

1. Add 40+ permitted images across 4+ categories.
2. Add 10+ labeled evaluation posts with expected image filenames.
3. Run the real Ollama models, not mock mode.
4. Run the full batch.
5. Run all acceptance probes.
6. Run the evaluation and record actual Top-1 precision.
7. Record real cost logs (local Ollama should be $0).
8. Fill EVIDENCE.md with real commands/results and image licenses.
9. Update BUILDLOG.md with the actual work chronology.
10. Review README and architecture.
11. Run `pytest -q`.
12. Remove `.env`, secrets, local database files, and credentials.
13. Push the complete public repository to GitHub.
14. Submit the public repository URL in the capstone portal.
