#!/usr/bin/env python3
"""
Test script to demonstrate API functionality
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_conversation_logging():
    """Test logging conversations via API"""
    print("Testing conversation logging API...")
    
    # Sample conversations to log
    conversations = [
        {
            "question": "How do I use the image classifier?",
            "response": "To use the image classifier, simply upload an image file and our AI will analyze it and provide predictions about what objects or categories are present in the image.",
            "feedback": "positive",
            "session_id": "session_001"
        },
        {
            "question": "What file formats are supported?",
            "response": "We support common image formats including JPG, PNG, GIF, and BMP files. The maximum file size is 10MB.",
            "feedback": "positive",
            "session_id": "session_002"
        },
        {
            "question": "Is my data secure?",
            "response": "Yes, all uploaded images are processed securely and deleted after analysis. We do not store your personal images.",
            "feedback": "neutral",
            "session_id": "session_003"
        },
        {
            "question": "Why is the prediction accuracy low?",
            "response": "Prediction accuracy can vary based on image quality, lighting conditions, and the complexity of the subject. Try uploading a clearer image with better lighting.",
            "feedback": "negative",
            "session_id": "session_004"
        },
        {
            "question": "Can I process multiple images at once?",
            "response": "Currently, our system processes one image at a time. Batch processing is a feature we're working on for future releases.",
            "feedback": "positive",
            "session_id": "session_005"
        }
    ]
    
    for i, conv in enumerate(conversations):
        try:
            response = requests.post(f"{BASE_URL}/api/log_conversation", 
                                   json=conv, 
                                   headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                print(f"✓ Logged conversation {i+1}: {conv['question'][:50]}...")
            else:
                print(f"✗ Failed to log conversation {i+1}: {response.status_code}")
        except Exception as e:
            print(f"✗ Error logging conversation {i+1}: {e}")
        
        # Add small delay between requests
        time.sleep(0.5)

def test_faq_api():
    """Test FAQ retrieval API"""
    print("\nTesting FAQ API...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/faqs")
        if response.status_code == 200:
            faqs = response.json()
            print(f"✓ Retrieved {len(faqs)} FAQs")
            for faq in faqs:
                print(f"  - {faq['question'][:50]}...")
        else:
            print(f"✗ Failed to retrieve FAQs: {response.status_code}")
    except Exception as e:
        print(f"✗ Error retrieving FAQs: {e}")

def test_individual_faq_api():
    """Test individual FAQ retrieval"""
    print("\nTesting individual FAQ API...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/faq/1")
        if response.status_code == 200:
            faq = response.json()
            print(f"✓ Retrieved FAQ: {faq['question']}")
            print(f"  Category: {faq['category']}")
            print(f"  Answer: {faq['answer'][:100]}...")
        else:
            print(f"✗ Failed to retrieve FAQ: {response.status_code}")
    except Exception as e:
        print(f"✗ Error retrieving FAQ: {e}")

if __name__ == "__main__":
    print("🚀 Testing Team10 Admin Dashboard APIs")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    try:
        # Test basic connectivity
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✓ Server is running and accessible")
        else:
            print("✗ Server connectivity issues")
            exit(1)
    except Exception as e:
        print(f"✗ Cannot connect to server: {e}")
        exit(1)
    
    # Run API tests
    test_conversation_logging()
    test_faq_api()
    test_individual_faq_api()
    
    print("\n🎉 API testing completed!")
    print("Check the dashboard at http://127.0.0.1:5000 to see the results.")