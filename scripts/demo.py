import os
os.environ.setdefault("MOCK_AI", "true")
from app.config import settings
print("Demo mode:", settings.mock_ai)
print("Use the API and tests for the full workflow.")
