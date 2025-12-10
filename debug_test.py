from fastapi.testclient import TestClient
from app.main import app
import sys

try:
    print("Initializing TestClient...")
    with TestClient(app) as client:
        print("Application started.")
        response = client.get("/health")
        print(f"Response: {response.status_code} {response.json()}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
