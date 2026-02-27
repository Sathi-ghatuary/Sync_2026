"""
Quick test script for the Title Verification API endpoints.
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test health endpoint."""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_database_stats():
    """Test database stats endpoint."""
    print("\n=== Testing Database Stats ===")
    response = requests.get(f"{BASE_URL}/database/stats")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_verify_title():
    """Test title verification endpoint."""
    print("\n=== Testing Title Verification ===")
    
    test_cases = [
        {"title": "Daily Sandhya", "description": "Periodicity + cross-language test"},
        {"title": "Times of India Daily", "description": "Combination + periodicity test"},
        {"title": "Hindu Indian Express", "description": "Combination test"},
        {"title": "Crime Daily News", "description": "Disallowed word test"},
        {"title": "The News Today", "description": "Disallowed prefix test"},
        {"title": "Morning Herald", "description": "Should pass (new unique title)"},
        {"title": "The Times of India", "description": "Semantic similarity test"},
    ]
    
    for case in test_cases:
        title = case["title"]
        print(f"\nTesting: {title}")
        print(f"Description: {case['description']}")
        
        response = requests.post(
            f"{BASE_URL}/verify",
            json={"title": title}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Status: ✓ PASSED")
            print(f"  Similarity Score: {data['similarity_score']}")
            print(f"  Verification Probability: {data['verification_probability']}")
            if data['violations']:
                print(f"  Violations: {len(data['violations'])}")
                for v in data['violations']:
                    print(f"    - [{v['rule']}] {v['message']}")
            if data['similar_titles']:
                print(f"  Similar Titles: {', '.join(data['similar_titles'][:2])}")
        else:
            print(f"  Status: ✗ FAILED - {response.status_code}")
            print(f"  Error: {response.text}")

def test_application_submission():
    """Test application submission endpoint."""
    print("\n=== Testing Application Submission ===")
    
    payload = {
        "title": "Evening News Digest",
        "user_email": "publisher@example.com"
    }
    
    print(f"Submitting title: {payload['title']}")
    print(f"User email: {payload['user_email']}")
    
    response = requests.post(
        f"{BASE_URL}/application",
        json=payload
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Status: ✓ APPLICATION RECORDED")
        print(f"Application ID: {data['application_id']}")
        print(f"Title: {data['title']}")
        print(f"Status: {data['status']}")
        print(f"Similarity Score: {data['similarity_score']}")
        print(f"Verification Probability: {data['verification_probability']}")
        return data['application_id']
    else:
        print(f"Status: ✗ FAILED - {response.status_code}")
        print(f"Error: {response.text}")
        return None

def test_user_applications(email: str):
    """Test retrieving user applications."""
    print(f"\n=== Testing User Applications Retrieval ===")
    print(f"Fetching applications for: {email}")
    
    response = requests.get(f"{BASE_URL}/applications/{email}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Status: ✓ SUCCESS")
        print(f"Total applications: {len(data['applications'])}")
        for app in data['applications']:
            print(f"  - ID: {app['id'][:8]}... | Title: {app['submitted_title']} | Status: {app['status']}")
    else:
        print(f"Status: ✗ FAILED - {response.status_code}")

if __name__ == "__main__":
    print("=" * 60)
    print("TITLE VERIFICATION API - TEST SUITE")
    print("=" * 60)
    
    # Test basic endpoints
    test_health()
    test_database_stats()
    
    # Test verification
    test_verify_title()
    
    # Test application submission
    app_id = test_application_submission()
    
    # Test retrieving applications
    if app_id:
        test_user_applications("publisher@example.com")
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETE")
    print("=" * 60)
    print("\nAPI Documentation available at: http://127.0.0.1:8000/docs")
