from fastapi.testclient import TestClient
from main import app # Import a FastAPI app from main.py

# Create a client to interact with the app
client = TestClient(app)

def test_generate_code_and_test_endpoint():
    """
    Tests the main endpoint to ensure it returns a successful response
    and the expected data structure.
    """
    # 1. Define the request payload
    payload = {"prompt": "Create a Python function to add two numbers"}

    # 2. Send a POST request to the endpoint
    response = client.post("/generate-code-and-test", json=payload)

    # 3. Assert the response is successful (HTTP 200 OK)
    assert response.status_code == 200

    # 4. Parse the JSON response
    data = response.json()

    # 5. Assert that the response contains the expected keys
    assert "functional_code" in data
    assert "test_code" in data
    assert "message" in data

    # 6. Assert that the generated code is not empty
    assert data["functional_code"] is not None
    assert len(data["functional_code"]) > 0
    assert data["test_code"] is not None
    assert len(data["test_code"]) > 0

def test_root_endpoint():
    """Tests the root endpoint '/'."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Automated Factory is running"}