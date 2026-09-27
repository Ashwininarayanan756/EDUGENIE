import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_all():
    print("--- 1. Testing GET / (Home) ---")
    r = client.get("/")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    assert "Welcome to EduGenie" in r.text
    assert "qaForm" in r.text
    assert "explainForm" in r.text
    assert "summaryForm" in r.text
    assert "quizForm" in r.text
    assert "recommendForm" in r.text
    print("[PASS] GET / passed")

    print("\n--- 2. Testing GET /health ---")
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    print("[PASS] GET /health passed:", data)

    print("\n--- 3. Testing GET & POST /qa ---")
    r = client.get("/qa?question=What is the largest ocean?")
    assert r.status_code == 200
    data = r.json()
    assert "answer" in data
    print("[PASS] GET /qa answer snippet:", repr(data["answer"][:100]))

    r_post = client.post("/qa", json={"question": "What is the capital of France?"})
    assert r_post.status_code == 200
    assert "answer" in r_post.json()
    print("[PASS] POST /qa answer snippet:", repr(r_post.json()["answer"][:100]))

    print("\n--- 4. Testing POST & GET /explain ---")
    r = client.post("/explain/", json={"topic": "Binary Search"})
    assert r.status_code == 200
    data = r.json()
    assert "explanation" in data
    print("[PASS] POST /explain/ explanation snippet:", repr(data["explanation"][:100]))

    print("\n--- 5. Testing POST /summarize ---")
    sample_text = (
        "The Industrial Revolution changed the world by shifting it from farming to factories. "
        "New machines, like James Watt's steam engine, made things faster and easier to produce."
    )
    r = client.post("/summarize/", json={"text": sample_text})
    assert r.status_code == 200
    data = r.json()
    assert "summary" in data
    print("[PASS] POST /summarize/ summary snippet:", repr(data["summary"][:100]))

    print("\n--- 6. Testing POST /quiz ---")
    r = client.post("/quiz", json={"text": "Pythagoras theorem"})
    assert r.status_code == 200
    data = r.json()
    assert "quiz" in data
    assert isinstance(data["quiz"], list)
    print(f"[PASS] POST /quiz returned {len(data['quiz'])} questions:")
    for idx, q in enumerate(data["quiz"]):
        print(f"  Q{idx+1}: {q.get('question')} | Answer: {q.get('answer')}")

    print("\n--- 7. Testing GET /learn/recommendations ---")
    r = client.get("/learn/recommendations?topic=SQL")
    assert r.status_code == 200
    data = r.json()
    assert "recommendation" in data
    print("[PASS] GET /learn/recommendations snippet:", repr(data["recommendation"][:100]))

    print("\n========================================")
    print("ALL 7 ENDPOINTS TESTED AND PASSED!")
    print("========================================")

if __name__ == "__main__":
    try:
        test_all()
    except Exception as e:
        print("[FAIL] Test failed:", e)
        sys.exit(1)
